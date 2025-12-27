**Лабораторная работа 6. Функциональное программирование. Часть 2. Python и функциональные возможности**

**Цель работы:** Изучить возможности функционального программирования в Python, освоить работу с функциями как объектами первого класса, изучить встроенные функции высшего порядка и научиться применять функциональные подходы в императивном языке.

**Задачи:**
1. Изучить функции как объекты первого класса в Python
2. Освоить встроенные функции высшего порядка: map, filter, reduce
3. Научиться использовать lambda-функции и замыкания
4. Изучить генераторы и списковые включения (comprehensions)
5. Освоить создание и использование декораторов

**Теоретическая часть**

**Функциональное программирование в Python:**
Python поддерживает множество парадигм программирования, включая функциональную. Хотя Python не является чисто функциональным языком, он предоставляет мощные инструменты для работы в функциональном стиле.

**Основные концепции:**
*   **Функции как объекты** - функции можно присваивать переменным, передавать как аргументы и возвращать из других функций
*   **Lambda-функции** - анонимные функции, определяемые в одной строке
*   **Замыкания** - функции, которые запоминают окружение, в котором они были созданы
*   **Декораторы** - функции, которые модифицируют поведение других функций
*   **Генераторы** - функции, которые возвращают итератор и могут приостанавливать свое выполнение

**Встроенные функции высшего порядка:**
*   **map()** - применяет функцию к каждому элементу последовательности
*   **filter()** - фильтрует элементы последовательности по условию
*   **reduce()** - последовательно применяет функцию к элементам для свертки

**Порядок выполнения работы**

**1. Функции как объекты первого класса**

Создайте файл `functions_as_objects.py`:

```python
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
```

**2. Lambda-функции и замыкания**

Создайте файл `lambda_closures.py`:

```python
# Lambda-функции (анонимные функции)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Использование lambda с map
squares = list(map(lambda x: x * x, numbers))
print(f"Квадраты: {squares}")

# Использование lambda с filter
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Четные числа: {even_numbers}")

# Сложные lambda-функции
complex_operation = lambda x: x ** 2 + 2 * x + 1
result = [complex_operation(x) for x in range(5)]
print(f"Результат сложной операции: {result}")

# Замыкания
def create_counter():
    """Создает счетчик с замыканием"""
    count = 0
    
    def counter():
        nonlocal count
        count += 1
        return count
    
    return counter

# Создаем два независимых счетчика
counter1 = create_counter()
counter2 = create_counter()

print("Счетчик 1:", [counter1() for _ in range(3)])
print("Счетчик 2:", [counter2() for _ in range(2)])
```

**3. Функции высшего порядка**

Создайте файл `higher_order.py`:

```python
from functools import reduce

# Данные для работы
students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map - преобразование данных
student_names = list(map(lambda student: student['name'], students))
print(f"Имена студентов: {student_names}")

# filter - фильтрация данных
top_students = list(filter(lambda student: student['grade'] >= 90, students))
print(f"Студенты с оценкой >= 90: {top_students}")

# reduce - свертка данных
product = reduce(lambda x, y: x * y, numbers)
print(f"Произведение чисел от 1 до 10: {product}")

# Комбинирование функций
def process_student_data(students):
    """Обработка данных студентов с использованием ФП"""
    # Цепочка преобразований
    result = list(
        map(lambda s: {
            'name': s['name'].upper(),
            'status': 'Excellent' if s['grade'] >= 90 else 'Good'
        },
        filter(lambda s: s['grade'] >= 80, students))
    )
    return result

processed_data = process_student_data(students)
print(f"Обработанные данные: {processed_data}")
```

**4. Генераторы и списковые включения**

Создайте файл `comprehensions_generators.py`:

```python
# Списковые включения (list comprehensions)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Простые включения
squares = [x * x for x in numbers]
print(f"Квадраты: {squares}")

# Включения с условием
even_squares = [x * x for x in numbers if x % 2 == 0]
print(f"Квадраты четных: {even_squares}")

# Словарные включения
student_dict = {student['name']: student['grade'] for student in students}
print(f"Словарь студентов: {student_dict}")

# Множества (set) включения
unique_ages = {student['age'] for student in students}
print(f"Уникальные возрасты: {unique_ages}")

# Генераторы
def fibonacci_generator(limit):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1

# Использование генератора
print("Числа Фибоначчи:")
fib_gen = fibonacci_generator(10)
for num in fib_gen:
    print(num, end=" ")
print()

# Генераторные выражения
squares_gen = (x * x for x in numbers)
print(f"Генератор квадратов: {list(squares_gen)}")
```

**5. Декораторы**

Создайте файл `decorators.py`:

```python
import time
from functools import wraps

# Простой декоратор
def timer(func):
    """Декоратор для измерения времени выполнения"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# Декоратор с параметрами
def repeat(num_times=2):
    """Декоратор для повторного выполнения функции"""
    def decorator_repeat(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(num_times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator_repeat

# Применение декораторов
@timer
def slow_function():
    """Медленная функция для демонстрации"""
    time.sleep(1)
    return "Готово!"

@repeat(num_times=3)
def greet(name):
    """Функция приветствия"""
    print(f"Привет, {name}!")

# Декоратор для кэширования
def cache(func):
    """Простой декоратор для кэширования"""
    cached_results = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cached_results:
            print(f"Используется кэшированный результат для {args}")
            return cached_results[args]
        result = func(*args)
        cached_results[args] = result
        return result
    return wrapper

@cache
def expensive_operation(x):
    """Дорогая операция"""
    print(f"Вычисление для {x}...")
    time.sleep(0.5)
    return x * x

# Демонстрация работы
print("=== Демонстрация декораторов ===")
slow_function()
greet("Иван")

print("Кэшированные вычисления:")
print(expensive_operation(5))
print(expensive_operation(5))  # Должен использовать кэш
print(expensive_operation(10))
```

**6. Практические задания**

**Задание 1:** Реализуйте функцию для обработки данных о студентах с использованием map, filter и reduce

```python
def analyze_students(students):
    """Анализ данных студентов"""
    # TODO: Вернуть словарь с:
    # - средним баллом
    # - списком отличников (grade >= 90)
    # - общим количеством студентов
    pass
```

**Задание 2:** Создайте декоратор для логирования вызовов функций

```python
def logger(func):
    """Декоратор для логирования"""
    # TODO: Реализовать логирование имени функции, аргументов и результата
    pass
```

**Задание 3:** Реализуйте генератор для бесконечной последовательности простых чисел

```python
def prime_generator():
    """Генератор простых чисел"""
    # TODO: Реализовать генератор, который yields простые числа
    pass
```

**Пример выполнения программы:**

```python
# main.py
from functions_as_objects import *
from lambda_closures import *
from higher_order import *
from comprehensions_generators import *
from decorators import *

def main():
    print("=== Демонстрация функционального программирования в Python ===")
    
    # Функции как объекты
    print("\n1. Функции как объекты:")
    print(f"apply_function(square, 5) = {apply_function(square, 5)}")
    
    # Lambda и замыкания
    print("\n2. Lambda и замыкания:")
    counter = create_counter()
    print(f"Счетчик: {counter()}, {counter()}, {counter()}")
    
    # Функции высшего порядка
    print("\n3. Функции высшего порядка:")
    print(f"Произведение чисел: {product}")
    
    # Генераторы и включения
    print("\n4. Генераторы и включения:")
    print(f"Четные квадраты: {even_squares}")
    
    # Декораторы
    print("\n5. Декораторы:")
    greet("Мария")

if __name__ == "__main__":
    main()
```

**Критерии оценки**

**Удовлетворительно:**
*   Реализованы базовые операции с функциями как объектами
*   Использованы lambda-функции с map и filter
*   Созданы простые списковые включения

**Хорошо:**
*   Корректно реализованы замыкания и функции высшего порядка
*   Использованы генераторы и различные виды включений
*   Созданы простые декораторы
*   Выполнены основные практические задания

**Отлично:**
*   Эффективно использованы комбинации функций высшего порядка
*   Реализованы сложные декораторы с параметрами
*   Созданы эффективные генераторы для работы с большими данными
*   Код хорошо структурирован и документирован
*   Реализованы все практические задания и дополнительные задачи

**Контрольные вопросы**
1.  Что такое функции первого класса и как Python их поддерживает?
2.  В чем разница между lambda-функциями и обычными функциями?
3.  Как работают замыкания и для чего они используются?
4.  Что такое декораторы и как создавать декораторы с параметрами?
5.  Какие преимущества дают генераторы по сравнению со списками?

**Рекомендованная литература**
1.  "Python Tricks: The Book" Dan Bader
2.  "Fluent Python" Luciano Ramalho
3.  Официальная документация Python: Functional Programming HOWTO
4.  "Effective Python: 90 Specific Ways to Write Better Python" Brett Slatkin