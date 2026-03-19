from typing import Optional
from dataclasses import dataclass
from enum import Enum
import math

from .tree import  Tree
from MathTools import utils, math_tools

@dataclass(frozen=True)
class TreeStaticData:
    wind_speed_break: float
    wind_speed_tipping: float
    wind_speed_separation: float

    tipping_angle: float
    separation_angle: float

    root_moment: float
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
    soil_moment: float
    weight_moment: float

    tree_status: TreeStates

class Simulator:
    def __init__(self):
        self._wind_speed: float = 0.0
        self._static_data: Optional[TreeStaticData] = None
        self._simulation_data: Optional[SimulationTreeData] = None
        self._tree: Optional[Tree] = None
        self._soil_c: Optional[float] = None

        self._is_pause = False
        self._is_stop = True
        self._is_run = True

        self._is_tipping = False
        self._is_break = False


    def _calculate_simulation(self):
        if not self._is_pause and not self._is_stop:
            if not self._is_tipping and not self._is_break:
                root_moment = self._static_data.root_moment

                wind_force = math_tools.wind_power(self._wind_speed, self._tree.c_d, self._tree.crown_square)

                angle = math_tools.roll_angle(wind_force, root_moment, self._soil_c, self._tree.tree_weight,
                                              self._tree.center_gravity_height, self._tree.tree_height)
                soil_moment = utils.soil_moment(root_moment, self._soil_c, angle)
                wind_moment = math_tools.bending_moment(self._tree.tree_height, wind_force)
                stress, safety_factor = utils.barrel_strength(self._tree.diameter,
                                                              wind_moment,
                                                              self._tree.max_strength)
                weight_moment = utils.weight_moment(angle, self._tree.tree_weight, self._tree.center_gravity_height)

                if safety_factor >= 1:
                    status = TreeStates.BREAK
                    self._is_break = True
                elif self._static_data.separation_angle < angle < self._static_data.tipping_angle:
                    status = TreeStates.SEPARATION
                elif angle > self._static_data.tipping_angle:
                    status = TreeStates.TIPPING
                    self._is_tipping = True
                else:
                    status = TreeStates.NORMAL

            if self._is_tipping:
                status = TreeStates.TIPPING

                angle = 10_000
                stress = 0
                safety_factor = 0
                soil_moment = 0
                weight_moment = 0
                wind_force = 0
                wind_moment = 0

            if self._is_break:
                angle = 0
                stress = 0
                safety_factor = 0
                wind_force = 0
                wind_moment = 0
                status = TreeStates.BREAK
                soil_moment = 0
                weight_moment = 0

            self._simulation_data = SimulationTreeData(
                roll_angle=round(math.degrees(angle), 2),
                stress=round(stress * 10**-6, 2), # Перевод в Мпа
                safety_factor=round(safety_factor, 2),
                wind_force=round(wind_force, 2),
                wind_moment=round(wind_moment, 2),
                tree_status=status,
                soil_moment=round(soil_moment, 2),
                weight_moment=round(weight_moment, 2)
            )

    def run(self) -> None:
        """
        Запускает симуляцию
        """
        if self._tree is None or self._soil_c is None or self._static_data is None:
            raise ValueError('Simulation fields is None!')
        self._wind_speed = 0

        self._is_stop = False
        self._is_pause = False
        self._is_run = True

        self._calculate_simulation()

    def stop(self) -> None:
        """
        Останавливает симуляцию
        """
        self._is_stop = True
        self._is_run = False
        self._is_pause = False

        self._simulation_data = None
        self._is_break = False
        self._is_tipping = False

    def pause(self) -> None:
        """
        Приостанавливает/запускает симуляцию, сохраняя все данные
        """
        self._is_pause = not self._is_pause
        if not self._is_pause:
            self._calculate_simulation()

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

        wind_speed_break = utils.max_wind_break(tree.diameter,
                                                        tree.c_d,
                                                        tree.crown_square,
                                                        tree.tree_height,
                                                        tree.max_strength)
        wind_speed_tipping = utils.max_wind_tipping(tree.tree_weight,
                                                    tree.center_gravity_height,
                                                    tree.a,
                                                    tree.b,
                                                    soil_c,
                                                    tree.c_d,
                                                    tree.crown_square,
                                                    tree.tree_height)
        wind_speed_separation = utils.separation_wind_speed(tree.tree_weight,
                                                            soil_c,
                                                            tree.a,
                                                            tree.b,
                                                            tree.center_gravity_height,
                                                            tree.tree_height,
                                                            tree.c_d,
                                                            tree.crown_square)
        tipping_angle = math_tools.tipping_angle(tree.tree_weight,
                                                              tree.center_gravity_height,
                                                              tree.b,
                                                              soil_c)
        separation_angle = math_tools.separation_angle(tree.tree_weight,
                                                                    soil_c,
                                                                    tree.a,
                                                                    tree.b)
        root_moment = math_tools.root_moment(tree.a, tree.b)
        resistance_moment = math_tools.tree_resistance_moment(tree.diameter)

        self._static_data = TreeStaticData(
            wind_speed_break=wind_speed_break,
            wind_speed_tipping=wind_speed_tipping,
            wind_speed_separation=wind_speed_separation,
            tipping_angle=tipping_angle,
            separation_angle=separation_angle,
            root_moment=root_moment,
            resistance_moment=resistance_moment,
        )

        return TreeStaticData(
            wind_speed_break=round(wind_speed_break, 2),
            wind_speed_tipping=round(wind_speed_tipping, 2),
            wind_speed_separation=round(wind_speed_separation, 2),
            tipping_angle=round(math.degrees(tipping_angle), 2),
            separation_angle=round(math.degrees(separation_angle), 2),
            root_moment=round(root_moment, 2),
            resistance_moment=round(resistance_moment, 2)

        )

    def get_simulate(self) -> SimulationTreeData:
        """
        Возвращает результат симуляции в реальном времени
        :return: Набор переменных, изменяющихся в симуляции
        """
        return self._simulation_data

    def set_wind_speed(self, speed) -> None:
        """
        Установка значения скорости после старта симуляции
        :param speed: Скорость ветра, м/с;
        """
        self._wind_speed = speed

        if self._is_run:
            print('RUN')
            self._calculate_simulation()