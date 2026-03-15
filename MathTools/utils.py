from . import math_tools


def wind_load(v: float,
              c_d: float,
              s: float,
              h: float) -> tuple[float, float]:
    """
    wind_load (ветровая нагрузка) - функция, позволяющая рассчитать силовую нагрузку ветра на дерево
                                    и изгибающий момент в основании ствола.
    :param v: Скорость ветра, м/с;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны, м^2;
    :param h: Высота дерева, м;
    :return: 1) Сила ветра, действующая на дерево, H;
             2) Момент силы у основания дерева, H*м.
    """

    f = math_tools.wind_power(v, c_d, s)
    r = math_tools.bending_moment(h, f)

    return f, r

def barrel_strength(d: float,
                    r: float,
                    max_sigma: float) -> tuple[float, float]:
    """
    barrel_strength - функция, позволяющая рассчитать напряжение в крайних волокнах ствола и сравнить
                      это значение с пределом прочности.
    :param d: Диаметр дерева на высоте груди взрослого человека, м;
    :param r: Момент силы изгиба у основания дерева, H*м;
    :param max_sigma: Предел прочности волокон дерева, Па;
    :return: 1) Напряжение в крайних волокнах ствола, Па;
             2) Отношение напряжения к пределу прочности.
    """

    sigma = math_tools.mechanical_tree_stress(r, d)
    k = sigma / max_sigma

    return sigma, k

def max_wind_break(d: float,
             c_d: float,
             s: float,
             h: float,
             max_sigma: float) -> float:
    """
    max_wind (максимальный ветер) - возвращает значение скорости ветра, при которой случится излом дерева.
    :param d: Диаметр дерева на высоте груди взрослого человека, м;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны, м^2;
    :param h: Высота дерева, м;
    :param max_sigma: Предел механической прочности дерева, Па;
    :return: Скорость ветра, при которой произойдет излом дерева, м/с.
    """
    max_bending_f = (math_tools.tree_resistance_moment(d) * max_sigma) / h
    return math_tools.wind_speed(max_bending_f, c_d, s)

def max_wind_tipping(q: float,
                     l: float,
                     a: float,
                     b: float,
                     c: float,
                     c_d: float,
                     s: float,
                     h: float) -> float:
    """
    max_wind_tipping (максимальный ветер опрокидывания) - расчет предельной скорости ветра,
                                                          при которой дерево опрокинется.
    :param q: Вес дерева, H;
    :param l: Высота центра тяжести от основания дерева, м;
    :param a: Длина подошвы дерева, м;
    :param b: Ширина подошвы дерева, м;
    :param c: Коэффициент жесткости грунта;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны, м^2;
    :param h: Высота дерева, м;
    :return: Максимальная скорость ветра, при которой случится опрокидывание, м/с.
    """
    j = math_tools.tree_sole_moment(a, b)
    alpha = math_tools.tipping_angle(q, l, b, c)
    f = math_tools.tipping_force(c, j, h, alpha, q, l)
    return math_tools.wind_speed(f, c_d, s)

def separation_wind_speed(q: float,
                          c: float,
                          a: float,
                          b: float,
                          l: float,
                          h: float,
                          c_d: float,
                          s: float):
    """
    separation_wind_speed (скорость отрыва) - Скорость ветра, при которой начнется отрыв корневой системы от почвы.
    :param q: Вес дерева, Н;
    :param c: Коэффициент жесткости грунта;
    :param a: Длина корневой системы дерева, м;
    :param b: Ширина Корневой системы дерева, м;
    :param l: Высота центра тяжести от основания дерева, м;
    :param h: Высота дерева, м;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны, м^2;
    :return: Скорость ветра, м/с;
    """
    alpha = math_tools.separation_angle(q, c, a, b)
    f = math_tools.wind_force_by_angle(alpha, c, a, b, q, l ,h)
    return math_tools.wind_speed(f, c_d, s)

def tree_stability(a: float,
                   b: float,
                   c: float,
                   q: float,
                   l: float,
                   h: float) -> bool:
    """
    tree_stability (стабильность дерева) - расчет устойчивости дерева для безветренной погоды.
    :param a: Длина подошвы дерева, м;
    :param b: Ширина подошвы дерева, м;
    :param c: Коэффициент жесткости грунта;
    :param q: Вес дерева, H;
    :param l: Высота центра тяжести от основания дерева;
    :param h: Высота дерева;
    :return: bool - устойчиво ли дерево (True - устойчиво,
                                         False - неустойчиво)
    """
    j = math_tools.tree_sole_moment(a, b)
    alpha = math_tools.roll_angle(0, j, c, q, l, h)

    return abs(alpha) <= 5