import math

from typing import Optional, TypeAlias

from .tree import Tree, TreeAttrs
from MathTools.utils import wind_load, barrel_strength, max_wind_break, max_wind_tipping, separation_wind_speed
from MathTools.math_tools import wind_power, roll_angle, root_moment, separation_angle, tipping_angle

class EmptyCalculateParam(Exception):
    def __init__(self, e: str):
        self._e = e

    def __str__(self):
        return self._e

tree_param: TypeAlias = Optional[float]
class CalculateManager:
    def __init__(self):
        self._tree: Optional[Tree]= None

    @property
    def tree(self) -> Optional[Tree]:
        return self._tree

    def set_tree(self, tree: Tree):
        self._tree = tree

    def _check_tree_params(self, **tree_params):
        if self._tree is None and any(map(lambda x: x is None, tree_params.values())):
            raise EmptyCalculateParam(f'Tree params is empty: ' +
                             ','.join([f'{name}:{value}' for name, value in tree_params.items()]))

    # -- Ветровая Нагрузка --
    def calculate_wind_load(self,
                  wind_speed: float,
                  c_d: Optional[float],
                  crown_square: Optional[float],
                  tree_height: Optional[float]) -> tuple[float, float]:
        """
        wind_load - Обертка-калькулятор для MathTools.utils.wind_load.
                    Параметры дерева необязательны, если в менеджере указано дерево.
        :param wind_speed: Скорость ветра, м/с;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :param tree_height: Высота дерева, м;
        :return: 1) Сила ветра, действующая на дерево, H;
                 2) Момент силы у основания дерева, H*м.
        """
        self._check_tree_params(c_d=c_d,
                                crown_square=crown_square,
                                tree_height=tree_height)
        if self._tree is not None:
            c_d, crown_square, tree_height = self._tree.get_attrs(TreeAttrs.C_D, TreeAttrs.CROWN_SQUARE,
                                                                  TreeAttrs.TREE_HEIGHT)
        f, m = wind_load(wind_speed, c_d, crown_square, tree_height)
        return round(f, 2), round(m, 2)

    # -- Прочность ствола --
    def calculate_mechanical_strength(self, wind_speed: float,
                                    c_d: tree_param,
                                    crown_square: tree_param,
                                    diameter: tree_param,
                                    max_strength: tree_param) -> tuple[float, float]:
        """
        calculate_mechanical_strength - Обертка-калькулятор для MathTools.utils.barrel_strength.
                                      Параметры дерева не обязательны, если указано дерево.
        :param wind_speed: Скорость ветра, м/с;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :param diameter: Диаметр дерева на высоте груди взрослого человека
        :param max_strength: Максимальная механическая напряженность породы дерева
        :return: Уровень напряженности волокон дерева, запас прочности
        """
        self._check_tree_params(c_d=c_d,
                                crown_square=crown_square,
                                diameter=diameter,
                                max_strength=max_strength)
        if self._tree is not None:
            c_d, crown_square, diameter, max_strength = self._tree.get_attrs(TreeAttrs.C_D, TreeAttrs.CROWN_SQUARE,
                                                                             TreeAttrs.DIAMETER, TreeAttrs.MAX_STRENGTH)

        wind_force = wind_power(wind_speed, c_d, crown_square)
        stress, strength = barrel_strength(diameter, wind_force, max_strength)

        return round(stress, 2), round(strength, 3)

    def calculate_max_wind_speed_break(self,
                             diameter: tree_param,
                             c_d: tree_param,
                             crown_square: tree_param,
                             tree_height: tree_param,
                             max_strength: tree_param) -> float:
        """
        max_wind (максимальный ветер) - Обертка-калькулятор для MathTools.utils.max_wind_break.
                                        Параметры дерева не обязательны, если указано дерево.
        :param diameter: Диаметр дерева на высоте груди взрослого человека, м;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :param tree_height: Высота дерева, м;
        :param max_strength: Предел механической прочности дерева, Па;
        :return: Скорость ветра, при которой произойдет излом дерева, м/с.
        """
        self._check_tree_params(diameter=diameter,
                                c_d=c_d,
                                crown_square=crown_square,
                                tree_height=tree_height,
                                max_strength=max_strength)
        if self._tree is not None:
            diameter, c_d, crown_square, tree_height, max_strength = self._tree.get_attrs(TreeAttrs.DIAMETER,
                                                                                          TreeAttrs.C_D,
                                                                                          TreeAttrs.CROWN_SQUARE,
                                                                                          TreeAttrs.TREE_HEIGHT,
                                                                                          TreeAttrs.MAX_STRENGTH)

        return round(max_wind_break(diameter, c_d, crown_square, tree_height, max_strength), 2)

    # -- Крен и опрокидывание --
    def calculate_roll_angle(self,
                   wind_speed: float,
                   c_soil_hardness: float,
                   c_d: tree_param,
                   a: tree_param,
                   b: tree_param,
                   crown_square: tree_param,
                   tree_weight: tree_param,
                   center_gravity_height: tree_param,
                   tree_height: tree_param) -> float:
        """
        roll_angle (прилегающий угол крена) - Обертка-калькулятор для расчета угла крена при конкретном значении ветра.
                                              Параметры дерева не обязательны, если указано дерево.
        :param wind_speed: Скорость ветра, м/с;
        :param c_soil_hardness: Коэффициент жесткости грунта;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param a: Длина подошвы корней, м;
        :param b: Ширина подошвы корней, м;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :param tree_weight: Вес дерева, H;
        :param center_gravity_height: Высота центра тяжести дерева от его основания, м;
        :param tree_height: Высота дерева, м;
        :return: угол крена, градусы;
        """
        self._check_tree_params(tree_weight=tree_weight,
                                center_gravity_height=center_gravity_height,
                                tree_height=tree_height,
                                c_d=c_d,
                                crown_square=crown_square,
                                a=a,
                                b=b)
        if self._tree is not None:
            (tree_weight, tree_height, center_gravity_height,
             c_d, crown_square, a, b) = self._tree.get_attrs(TreeAttrs.TREE_WEIGHT,
                                                             TreeAttrs.TREE_HEIGHT,
                                                             TreeAttrs.CENTER_GRAVITY_HEIGHT,
                                                             TreeAttrs.C_D,
                                                             TreeAttrs.CROWN_SQUARE,
                                                             TreeAttrs.A,
                                                             TreeAttrs.B)

        wind_force = wind_power(wind_speed, c_d, crown_square)
        sole_moment = root_moment(a, b)

        angle = roll_angle(wind_force, sole_moment, c_soil_hardness, tree_weight,
                          center_gravity_height, tree_height)

        return round(math.degrees(angle), 2)

    def calculate_separation_angle(self,
                                   c_soil_hardness: float,
                                   tree_weight: tree_param,
                                   a: tree_param,
                                   b: tree_param) -> float:
        """
        separation_angle (угол отрыва) - Обертка-калькулятор для MathTools.utils.separation_angle.
                                         Параметры дерева не обязательны, если указано дерево.
        :param tree_weight: Вес дерева, H;
        :param c_soil_hardness: Коэффициент жесткости грунта;
        :param a: Длина корневой подошвы дерева, м;
        :param b: Ширина корневой подошвы дерева, м;
        :return: Угол отрыва подошвы, градусы.
        """
        self._check_tree_params(tree_weight=tree_weight,
                                a=a,
                                b=b)
        if self._tree is not None:
            tree_weight, a, b = self._tree.get_attrs(TreeAttrs.TREE_WEIGHT,
                                                     TreeAttrs.A,
                                                     TreeAttrs.B)

        angle = separation_angle(tree_weight, c_soil_hardness, a, b)

        return round(math.degrees(angle), 2)

    def calculate_tipping_angle(self,
                                c_soil_hardness: float,
                                tree_weight: tree_param,
                                center_gravity_height: tree_param,
                                b: tree_param) -> float:
            """
            tipping angle (угол опрокидывания) - Обертка-калькулятор для MathTools.math_tools.tipping_angle
            :param tree_weight: Вес дерева, Н;
            :param center_gravity_height: Высота центра тяжести от основания дерева, м;
            :param b: Ширина корневой системы дерева, м;
            :param c_soil_hardness: Коэффициент жесткости грунта;
            :return: Угол опрокидывания, градусы.
            """
            self._check_tree_params(tree_weight=tree_weight,
                                    center_gravity_height=center_gravity_height,
                                    b=b)
            if self._tree is not None:
                tree_weight, center_gravity_height, b = self._tree.get_attrs(TreeAttrs.TREE_WEIGHT,
                                                                             TreeAttrs.CENTER_GRAVITY_HEIGHT,
                                                                             TreeAttrs.B)

            angle = tipping_angle(tree_weight, center_gravity_height, b, c_soil_hardness)
            return round(math.degrees(angle), 2)

    def calculate_max_wind_tipping(self,
                                   c_soil_hardness: float,
                                   tree_weight: tree_param,
                                   center_gravity_height: tree_param,
                                   a: tree_param,
                                   b: tree_param,
                                   c_d: tree_param,
                                   crown_square: tree_param,
                                   tree_height: tree_param
                                   ) -> float:
        """
        max_wind_tipping (максимальный ветер опрокидывания) - Обертка-калькулятор для MathTools.utils.max_wind_tipping.
        :param tree_weight: Вес дерева, H;
        :param center_gravity_height: Высота центра тяжести от основания дерева, м;
        :param a: Длина подошвы дерева, м;
        :param b: Ширина подошвы дерева, м;
        :param c_soil_hardness: Коэффициент жесткости грунта;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :param tree_height: Высота дерева, м;
        :return: Максимальная скорость ветра, при которой случится опрокидывание, м/с.
        """
        self._check_tree_params(tree_weight=tree_weight,
                                center_gravity_height=center_gravity_height,
                                a=a,
                                b=b,
                                c_d=c_d,
                                crown_square=crown_square,
                                tree_height=tree_height)
        if self._tree is not None:
            tree_weight, center_gravity_height, a, b, c_d, crown_square, tree_height = self._tree.get_attrs(
                TreeAttrs.TREE_WEIGHT, TreeAttrs.CENTER_GRAVITY_HEIGHT, TreeAttrs.A, TreeAttrs.B, TreeAttrs.C_D,
                TreeAttrs.CROWN_SQUARE, TreeAttrs.TREE_HEIGHT
            )

        return round(max_wind_tipping(tree_weight, center_gravity_height, a, b, c_soil_hardness, c_d,
                                crown_square, tree_height), 2)

    def calculate_separation_wind_speed(self,
                                        tree_weight: tree_param,
                                        c_soil_parameter: float,
                                        a: tree_param,
                                        b: tree_param,
                                        center_gravity_height: tree_param,
                                        tree_height: tree_param,
                                        c_d: tree_param,
                                        crown_square: tree_param):

        """
        calculate_separation_wind_speed (расчет скорости отрыва подошвы) - Калькулятор-обертка для
                                                                           MathTools.utils.separation_wind_speed
        :param tree_weight: Вес дерева, Н;
        :param c_soil_parameter: Коэффициент жесткости грунта;
        :param a: Длина корневой системы дерева, м;
        :param b: Ширина Корневой системы дерева, м;
        :param center_gravity_height: Высота центра тяжести от основания дерева, м;
        :param tree_height: Высота дерева, м;
        :param c_d: Коэффициент аэродинамичного сопротивления кроны;
        :param crown_square: Площадь вертикальной проекции кроны, м^2;
        :return: Скорость ветра, м/с;
        """
        self._check_tree_params(
            tree_weight=tree_weight,
            a=a,
            b=b,
            center_gravity_height=center_gravity_height,
            tree_height=tree_height,
            c_d=c_d,
            crown_square=crown_square
        )
        if self._tree is not None:
            tree_weight, a, b, center_gravity_height, tree_height, c_d, crown_square = self._tree.get_attrs(TreeAttrs.TREE_WEIGHT,
                                                                                                            TreeAttrs.A,
                                                                                                            TreeAttrs.B,
                                                                                                            TreeAttrs.CENTER_GRAVITY_HEIGHT,
                                                                                                            TreeAttrs.TREE_HEIGHT,
                                                                                                            TreeAttrs.C_D,
                                                                                                            TreeAttrs.CROWN_SQUARE)

        return round(separation_wind_speed(tree_weight,
                                     c_soil_parameter,
                                     a,
                                     b,
                                     center_gravity_height,
                                     tree_height,
                                     c_d,
                                     crown_square), 2)
