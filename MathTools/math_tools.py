import math

AIR = 1.25 # плотность воздуха, 1.25 кг/м^3

def wind_power(v: float,
       c_d: float,
       s: float) -> float:
    """
    wind_power - аэродинамичная сила ветра.
    :param v: Скорость ветра, м/с;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны, м^2
    :return: Сила взаимодействия ветра и кроны дерева, H.
    """

    return c_d*s*AIR*v**2*0.5

def wind_speed(f: float,
               c_d: float,
               s: float) -> float:
    """
    wind_speed (скорость ветра) - зависимость скорости от силы ветра.
    :param f: Сила ветра, H;
    :param c_d: Коэффициент аэродинамичного сопротивления кроны;
    :param s: Площадь вертикальной проекции кроны;
    :return: скорость ветра, м/с.
    """
    return math.sqrt(2*f/(c_d*s*AIR))


def bending_moment(h: float,
                   r: float) -> float:
    """
    bending_moment - (bending moment) изгибающий момент у основания дерева.
    :param h: Высота дерева, м;
    :param r: Сила ветра, Н;
    :return: Изгибающий момент, H*м.
    """
    return r * h

def tree_resistance_moment(d: float) -> float:
    """
    tree_resistance_moment (сопротивление дерева) - зависимость момента сопротивления дерева от его диаметра.
    :param d: Диаметр дерева на высоте груди взрослого человека, м;
    :return: Момент сопротивления сечения дерева, Н*м.
    """

    return math.pi * d**3 * (1/32)

def tree_sole_moment(a: float,
                     b: float) -> float:
    """
    tree_sole_moment (момент подошвы дерева) - момент инерции подошвы дерева.
    :param a: Длина подошвы корней, м;
    :param b: Ширина подошвы корней, м;
    :return: Момент инерции подошвы дерева, H*м.
    """
    return a*b**3/12

def mechanical_tree_stress(r: float,
                           d: float) -> float:
    """
    mechanical_tree_stress (механическая напряженность дерева) - механическая напряженность в крайних волокнах ствола.
    :param r: Момент силы изгиба у основания дерева, H*м;
    :param d: Диаметр дерева на высоте груди взрослого человека, м;
    :return: Механическое напряжение в крайних волокнах ствола, Па.
    """
    return r / tree_resistance_moment(d)

def roll_angle(f: float,
               j: float,
               c: float,
               q: float,
               l: float,
               h: float) -> float:
    """
    roll_angle (прилегающий угол крена) - зависимость угла крена от силы ветра.
    :param f: Сила ветра, H;
    :param j: Момент инерции подошвы дерева, H*м;
    :param c: Коэффициент жесткости грунта;
    :param q: Вес дерева, H;
    :param l: Высота центра тяжести дерева от его основания, м;
    :param h: Высота дерева, м;
    :return: угол крена, градусы;
    """
    return f*h * (1/(c*j-q*l))

def separation_angle(q: float,
                     c: float,
                     a: float,
                     b: float) -> float:
    """
    separation_angle (угол отрыва) - угол, при котором почва дерева начнет отрываться от земли.
    :param q: Вес дерева, H;
    :param c: Коэффициент жесткости грунта;
    :param a: Длина корневой подошвы дерева, м;
    :param b: Ширина корневой подошвы дерева, м;
    :return: Угол отрыва подошвы, градусы.
    """
    return (2 * q) / (c * a**2 * b)

def tipping_angle(q: float,
                  l: float,
                  b: float,
                  c: float) -> float:
    """
    tipping angle (угол опрокидывания) - угол, при котором дерево опрокинется.
    :param q: Вес дерева, Н;
    :param l: Высота центра тяжести от основания дерева, м;
    :param b: Ширина корневой системы дерева, м;
    :param c: Коэффициент жесткости грунта;
    :return: Угол опрокидывания, градусы.
    """
    return (q/(18*l**2*b*c))**(1/3)

def wind_force_by_angle(angle: float,
                        c: float,
                        a: float,
                        b: float,
                        q: float,
                        l: float,
                        h: float):
    """
    wind_force_by_angle (сила ветра из угла) - Зависимость силы ветра от угла крена
    :param angle: Угол крена, градусы;
    :param c: Коэффициент жесткости грунта;
    :param a: Длина корневой системы дерева, м;
    :param b: Ширина корневой системы дерева, м;
    :param q: Вес дерева, H;
    :param l: Высота центра тяжести от основания дерева, м;
    :param h: Высота дерева, м;
    :return: Значение силы ветра, H;
    """
    return angle * ((c*tree_sole_moment(a,b)-q*l)/h)

def tipping_force(c: float,
                  j: float,
                  h: float,
                  alpha: float,
                  q: float,
                  l: float) -> float:
    """
    tipping_force (сила опрокидывания) - сила ветра, при которой случится опрокидывание.
    :param c: Коэффициент жесткости грунта;
    :param j: Момент инерции подошвы дерева, H*м;
    :param h: Высота дерева, м;
    :param alpha: Предельный угол опрокидывания дерева, градусы;
    :param q: вес дерева, Н;
    :param l: высота центра тяжести от основания дерева, м;
    :return: сила ветра, при которой случится опрокидывание дерева, Н.
    """
    return (c*j - q*l)*alpha * (1/h)
