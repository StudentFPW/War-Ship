# Игру разработал студент (Leonids Jofe) из школы SkillFactory, курс Full-stack python developer, класс FPW-104

import random


# ----------------------------------------------------------------------------------------------------------------------

class ShotOverMap(Exception):
    def __str__(self):
        return "За поле боя!"


class SameShot(Exception):
    def __str__(self):
        return "Вы уже туда стреляли!"


class Missed(Exception):
    pass


########################################################################################################################

# Это класс, представляющий поле.
class Field:
    def __init__(self, __length=7) -> None:
        self.__length = __length
        # Это способ создать список в одну строку.
        self.field = [['O' for ROW in range(self.__length)] for COLUMN in range(self.__length)]

    def set_ship_on_field_01(self) -> list:
        """
        Эта функция устанавливает корабль на поле.
        """
        # Создание случайных чисел для кораблей.
        _ship_3 = random.randint(1, 2)
        _ship_201 = random.randint(1, 3)
        _ship_202 = random.randint(1, 3)

        # Размещение корабля длины 3 на поле.
        for i in range(3):
            self.field[0][_ship_3 + i] = "■"

        # Он ставит на поле два корабля длины 2.
        for i in range(2):
            self.field[_ship_201 + i][5] = "■"
            self.field[_ship_202 + i][0] = "■"

        # Он ставит на поле 4 корабля длины 1.
        for i in range(4):
            _ship_101 = random.choice([[0, 6], [2, 2], [3, 3], [4, 2], [5, 3], [6, 2], [6, 6], [6, 0]])
            _y, _x = _ship_101
            self.field[_y][_x] = "■"
        return self.field

    def set_ship_on_field_02(self) -> list:
        """
        Эта функция выставляет корабль на поле.
        """
        # Создание случайных чисел для кораблей.
        _ship_3 = random.randint(0, 4)
        _ship_201 = random.randint(1, 5)

        # Размещение корабля длины 3 на поле.
        for i in range(3):
            self.field[_ship_3 + i][6] = "■"

        # Он ставит на поле два корабля длины 2.
        for i in range(2):
            self.field[_ship_201][3 + i] = "■"
            self.field[_ship_201 - 2][3 + i] = "■"

        # Размещение 4 кораблей длины 1 на поле.
        for i in range(4):
            _ship_101 = random.choice([[0, 0], [1, 1], [2, 0], [3, 1], [4, 0], [5, 1], [6, 0]])
            _y, _x = _ship_101
            self.field[_y][_x] = "■"
        return self.field

    def get_field(self):
        return self.field

    def __str__(self):
        _res = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
        for i, _row in enumerate(self.field):
            _res += f"\n{i + 1} | " + " | ".join(_row) + " |"
        return _res


########################################################################################################################

# > Класс, представляющий уставку.
class SetPoint:
    __nr1_obj = 1
    __nr2_obj = 7

    @classmethod
    def __symbol(cls, _arg) -> bool:
        """
        `__symbol` возвращает `True`, если `arg` является символом 1 - 7, `False` в противном случае.

        :param cls: Класс, к которому применяется декоратор.
        :param arg: Аргумент, который нужно проверить.
        """
        return cls.__nr1_obj <= _arg <= cls.__nr2_obj

    def __init__(self, check_y, check_x) -> None:
        self.__row = self.__column = 0
        # Проверка, не находится ли выстрел над картой.
        if self.__symbol(check_y) and self.__symbol(check_x):
            self.__row = check_y - 1
            self.__column = check_x - 1
        else:
            raise ShotOverMap("За поле боя!")

    @property
    def get_y(self) -> int:
        return self.__row

    @property
    def get_x(self) -> int:
        return self.__column


########################################################################################################################

# Корабль имеет размер и местоположение.
class Ship:
    def __init__(self, _empty_y=0, _empty_x=0, _field=None, _enemy=None) -> None:
        if _enemy is None:
            self.__enemy_field = []
        if _field is None:
            self.__fields = []
        self.y = _empty_y
        self.x = _empty_x

    def set_shot_data(self, fill_y, fill_x) -> None:
        self.y = fill_y
        self.x = fill_x

    def set_fields(self, field) -> None:
        self.__fields = field

    def check_field_enemy(self, enemy) -> None:
        self.__enemy_field = enemy

    def fill_empty_field(self) -> list:
        if self.__enemy_field[self.y][self.x] == "■":
            self.__fields[self.y][self.x] = "X"
            return self.__fields
        if self.__enemy_field[self.y][self.x] == "O":
            self.__fields[self.y][self.x] = "T"
            return self.__fields

    def get_shot(self) -> list or Exception:
        if self.__fields[self.y][self.x] == "■":
            self.__fields[self.y][self.x] = "X"
            return self.__fields
        if self.__fields[self.y][self.x] == "O":
            self.__fields[self.y][self.x] = "T"
            raise Missed("мимо!")
        else:
            raise SameShot("Вы уже туда стреляли!")

    def check_ship(self) -> bool:
        """
        Эта функция проверяет, находится ли корабль на карте, остались ли еще корабли.
        """
        true_or_false = True
        for row in range(len(self.__fields)):
            for column in range(len(self.__fields)):
                if self.__fields[row][column] == "■":
                    true_or_false = True
                    return true_or_false
                else:
                    true_or_false = False
        return true_or_false


########################################################################################################################

class GetRandomPoint:
    __array = []

    def __init__(self, _ii_y=0, _ii_x=0, _point=0):
        self.__y = _ii_y
        self.__x = _ii_x
        self.__point = _point

    def get_II_data(self):
        """
        Он создает список кортежей, перемешивает список, а затем присваивает первый кортеж переменным __y и __x.
        """
        for _row in range(1, 7):
            for _column in range(1, 7):
                self.__array.append((_row, _column))
        random.shuffle(self.__array)
        for number in self.__array:
            self.__y, self.__x = number

    def y(self):
        return self.__y

    def x(self):
        return self.__x


########################################################################################################################

if __name__ == "__main__":
    print("                               |-----------------------------------------|")
    print("                               |  Приветствуем вас  |  формат ввода: y x |")
    print("                               |       в игре       |  y - номер строки  |")
    print("                               |     морской бой    |  x - номер столбца |")
    print("                               |-----------------------------------------|")
    print()
    print("---------------------------Игра морской бой началась, пусть победить сильнейший--------------------------")
    print("------------------------ Буквой X помечаются подбитые корабли. Буквой T — промахи -----------------------")
    print()

    # Создание трех экземпляров класса `Field`.
    USER_SHOT_II = Field()
    USER = Field()
    II = Field()

    # Создаем карты с кораблями.
    USER.set_ship_on_field_02()
    II.set_ship_on_field_01()

    # Это объекты класса `Ship`, стрельба и нахождение кораблей.
    SHOT_IN_II_INVISIBLE = Ship()
    SHOT_IN_USER = Ship()
    SHOT_IN_II = Ship()

    # Создание экземпляра класса GetRandomPoint.
    RANDOMVALUE = GetRandomPoint()

    # Приведенный выше код представляет собой игру линкоров.
    while SHOT_IN_II.check_ship():
        print(USER)
        print("↓ Стреляйте по кораблям противника ↓")
        print(USER_SHOT_II)
        print("Ваш ход ↓")
        try:
            y = int(input("Y = "))
            x = int(input("X = "))
        # Отлов ошибки, если пользователь вводит букву вместо цифры.
        except ValueError:
            print("###############################################################################################")
            print("Попробуйте снова !")
            print("###############################################################################################")
        else:
            try:
                USER_SET_SHOT = SetPoint(y, x)
            # Отлов ошибки, если пользователь вводит слишком большое число.
            except ShotOverMap as e:
                print("###############################################################################################")
                print(e, "в этом случае ваш ход не засчитывается :)")
                print("Попробуйте снова !")
                print("###############################################################################################")
            else:
                # Это для пустого поля по которому мы гадаем, где корабли врага ↓.
                SHOT_IN_II_INVISIBLE.set_shot_data(USER_SET_SHOT.get_y, USER_SET_SHOT.get_x)  # Куда мы стреляем.
                SHOT_IN_II_INVISIBLE.set_fields(USER_SHOT_II.get_field())  # В кого мы стреляем.
                SHOT_IN_II_INVISIBLE.check_field_enemy(II.get_field())  # Где проверяем данные
                SHOT_IN_II_INVISIBLE.fill_empty_field()  # Призводим выстрел по пустому полю.

                # Тут мы уже призводим выстрел ↓.
                SHOT_IN_II.set_shot_data(USER_SET_SHOT.get_y, USER_SET_SHOT.get_x)  # Куда мы стреляем.
                SHOT_IN_II.set_fields(II.get_field())  # В кого мы стреляем.
                try:
                    SHOT_IN_II.get_shot()  # Призводим выстрел.
                # Отлов ошибки, если пользователь вводит не попал в корабль.
                except Missed:
                    print("###########################################################################################")
                    print("Вы не попали !")
                    print("###########################################################################################")
                # Отлов ошибки, если пользователь вводит одинаковее данные подряд.
                except SameShot:
                    print("###########################################################################################")
                    print("Вы уже туда стреляли !")
                    print("###########################################################################################")
                finally:
                    # Он проверяет, остались ли у противника корабли.
                    if not SHOT_IN_II.check_ship():  # Проверка кораблей нашего врага.
                        print("Выиграл человек :)")
                        break
                    print("----- ↓ Результат выстрела ↓ -----")
                    print(USER_SHOT_II)
                    print()
                    print("------------------- ↓ Ходил компьютер ↓ -------------------")

                    # Получение случайных координат для компьютера, чтобы стрелять.
                    RANDOMVALUE.get_II_data()

                    II_SET_SHOT = SetPoint(RANDOMVALUE.y(), RANDOMVALUE.x())
                    SHOT_IN_USER.set_shot_data(II_SET_SHOT.get_y, II_SET_SHOT.get_x)  # Куда мы стреляем.
                    SHOT_IN_USER.set_fields(USER.get_field())  # В кого мы стреляем.
                    try:
                        SHOT_IN_USER.get_shot()  # Призводим выстрел.
                    # Отлов ошибки, если компьютер вводит не попал в корабль.
                    except Missed as fail:
                        print(f"---------------- Компьютер выстрелил {fail} ----------------")
                        print()
                    # Проверяет есть ли корабль на карте, остались ли корабли.
                    if not SHOT_IN_USER.check_ship():  # Проверка наших кораблей.
                        print("---------- Вы проиграли!:) -----------")
                        print("Люди проиграли и машины захватили мир!")
                        break

########################################################################################################################
