# Функции можно присваивать переменным
def square(x):
    return x * x

def cube(x):
    return x * x * x

# Присваивание функции переменной
my_function = square
print(f"square(5) = {square(5)}")
print(f"my_function(5) = {my_function(5)}")

# Функции можно передавать как аргументы
def apply_function(func, value):
    """Применяет функцию к значению"""
    return func(value)

print(f"apply_function(square, 4) = {apply_function(square, 4)}")
print(f"apply_function(cube, 3) = {apply_function(cube, 3)}")

# Функции можно возвращать из функций
def create_multiplier(factor):
    """Создает функцию-умножитель"""
    def multiplier(x):
        return x * factor
    return multiplier

double = create_multiplier(2)
triple = create_multiplier(3)

print(f"double(10) = {double(10)}")
print(f"triple(10) = {triple(10)}")
