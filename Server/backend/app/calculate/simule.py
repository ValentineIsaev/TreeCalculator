import threading
from typing import Optional
from dataclasses import dataclass
from enum import Enum

from MathTools.math_tools import roll_angle
from .tree import  Tree
from MathTools import utils, math_tools

@dataclass(frozen=True)
class TreeStaticData:
    wind_speed_break: float
    wind_speed_tipping: float
    wind_speed_separation: float

    tipping_angle: float
    separation_angle: float

    soil_moment: float
    resistance_moment: float

class TreeStates(Enum):
    NORMAL = 'normal' # Стабильное положение
    SEPARATION = 'separation' # Отрыв почвы
    TIPPING = 'tipping' # Опрокинуто
    BREAK = 'break' # Вырвано

@dataclass(frozen=True)
class SimulationTreeData:
    roll_angle: float
    stress: float
    safety_factor: float
    wind_moment: float
    wind_force: float

    tree_status: TreeStates

class Simulator:
    def __init__(self):
        self._wind_speed: float = 0.0
        self._static_data: Optional[TreeStaticData] = None
        self._simulation_data: Optional[SimulationTreeData] = None
        self._tree: Optional[Tree] = None
        self._soil_c: Optional[float] = None

        self._simulation_thread = None
        self._create_simulation_thread()
        self._thread_lock = threading.Lock()

        self._stop_simulation_flag = threading.Event()
        self._stop_simulation_flag.set()
        self._pause_simulation_flag = threading.Event()

    def _simulation(self):
        soil_moment = self._static_data.soil_moment
        while not self._stop_simulation_flag.is_set():
            if self._pause_simulation_flag.is_set():
                self._pause_simulation_flag.wait()
            with self._thread_lock:
                wind_force = math_tools.wind_power(self._wind_speed, self._tree.c_d, self._tree.crown_square)

                angle = math_tools.roll_angle(wind_force, soil_moment, self._soil_c, self._tree.tree_weight,
                                              self._tree.center_gravity_height, self._tree.tree_height)
            wind_moment = math_tools.bending_moment(self._tree.tree_height, wind_force)
            stress, safety_factor =  utils.barrel_strength(self._tree.diameter,
                                                           wind_moment,
                                                           self._tree.max_strength)

            if safety_factor <= 1:
                status = TreeStates.BREAK
            elif self._static_data.separation_angle < angle < self._static_data.tipping_angle:
                status = TreeStates.SEPARATION
            elif angle > self._static_data.tipping_angle:
                status = TreeStates.TIPPING
            else:
                status = TreeStates.NORMAL

            with self._thread_lock:
                self._simulation_data = SimulationTreeData(
                    roll_angle=angle,
                    stress=stress,
                    safety_factor=safety_factor,
                    wind_force=wind_force,
                    wind_moment=wind_moment,
                    tree_status=status
                )

    def _create_simulation_thread(self):
        self._simulation_thread = threading.Thread(target=self._simulation)

    def run(self) -> None:
        """
        Запускает симуляцию
        """
        if self._tree is None or self._soil_c is None or self._static_data is None:
            raise ValueError('Simulation fields is None!')
        self._wind_speed = 0
        self._stop_simulation_flag.clear()
        self._simulation_thread.start()

    def stop(self) -> None:
        """
        Останавливает симуляцию
        """
        self._stop_simulation_flag.set()
        if self._simulation_thread.is_alive():
            self._simulation_thread.join()
        self._simulation_data = None
        self._create_simulation_thread()

    def pause(self) -> None:
        """
        Приостанавливает симуляцию, сохраняя все данные
        """
        if self._pause_simulation_flag.is_set(): self._pause_simulation_flag.clear()
        else: self._pause_simulation_flag.set()

    def set_data(self, tree: Tree, soil_c: float) -> TreeStaticData:
        """
        Установка значений для симуляции
        :param tree: Данные дерева
        :param soil_c: Коэффициент жесткости грунта
        :return: Все статичные значения для дерева, которые не будут меняться в результате симуляции
        """
        self.stop()
        self._tree = tree
        self._soil_c = soil_c

        static_data = TreeStaticData(
            wind_speed_break=utils.max_wind_break(tree.diameter,
                                                  tree.c_d,
                                                  tree.crown_square,
                                                  tree.tree_height,
                                                  tree.max_strength,
                                             ),
            wind_speed_tipping=utils.max_wind_tipping(tree.tree_weight,
                                                      tree.center_gravity_height,
                                                      tree.a,
                                                      tree.b,
                                                      soil_c,
                                                      tree.c_d,
                                                      tree.crown_square,
                                                      tree.tree_height),
            wind_speed_separation=utils.separation_wind_speed(tree.tree_weight,
                                                              soil_c,
                                                              tree.a,
                                                              tree.b,
                                                              tree.center_gravity_height,
                                                              tree.tree_height,
                                                              tree.c_d,
                                                              tree.crown_square),
            tipping_angle=math_tools.tipping_angle(tree.tree_weight,
                                                   tree.center_gravity_height,
                                                   tree.b,
                                                   soil_c),
            separation_angle=math_tools.separation_angle(tree.tree_weight,
                                                         soil_c,
                                                         tree.a,
                                                         tree.b),
            soil_moment=math_tools.tree_sole_moment(tree.a,
                                                    tree.b),
            resistance_moment=math_tools.tree_resistance_moment(tree.diameter)

        )
        self._static_data = static_data
        return static_data

    def get_simulate(self) -> SimulationTreeData:
        """
        Возвращает результат симуляции в реальном времени
        :return: Набор переменных, изменяющихся в симуляции
        """
        with self._thread_lock:
            return self._simulation_data

    def set_wind_speed(self, speed) -> None:
        """
        Установка значения скорости после старта симуляции
        :param speed: Скорость ветра, м/с;
        """
        with self._thread_lock:
            self._wind_speed = speed