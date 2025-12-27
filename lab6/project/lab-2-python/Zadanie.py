import time
from functools import reduce, wraps

students = [
    {'name': 'Alice', 'grade': 85, 'age': 20},
    {'name': 'Bob', 'grade': 92, 'age': 22},
    {'name': 'Charlie', 'grade': 78, 'age': 19},
    {'name': 'Diana', 'grade': 95, 'age': 21},
    {'name': 'Eve', 'grade': 88, 'age': 20}
]

def analyze_students(students):
    """Анализ данных студентов"""
    # TODO: Вернуть словарь с:
    grade = list(map(lambda student: student['grade'], students))
    res = {
        "средниq бал" : sum(grade) / len(grade),
        "списком отличников" : list(filter(lambda student: student['grade'] >= 90, students)),
        "общим количеством студентов" : reduce(lambda acc, student: acc + 1, students, 0)
    }
    return res
a = analyze_students(students)
print(a["средниq бал"],a["списком отличников"],a["общим количеством студентов"])


def prime_generator():
    count = 0
    while True:
        yield count
        count += 1


b = prime_generator()
print(next(b))
print(next(b))
print(next(b))
print(next(b))

def logger(func):
    
    """Декоратор для логирования"""
    # TODO: Реализовать логирование имени функции, аргументов и результата

    @wraps(func)
    def vnutri(*args, **kwargs):
        result = func(*args, **kwargs)
        name = func.__name__
        
        args_s = ', '.join(map(repr, args))
        kwargs_s = ', '.join(f"{k}={repr(v)}" for k, v in kwargs.items())
        all_args = ', '.join(filter(None, [args_s, kwargs_s]))
        res = [name, all_args, result]

        return res
    return vnutri

@logger
def greet(name):
    """Функция приветствия"""
    return f"Привет, {name}!"

print(greet("Boris"))