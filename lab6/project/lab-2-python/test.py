import time
from functools import wraps


def timer(func):                    # 1. Декоратор принимает функцию
    @wraps(func)                   # 2. Сохраняем метаданные оригинальной функции
    def wrapper(*args, **kwargs):  # 3. Внутренняя функция-обертка
        # Код ДО вызова оригинальной функции
        start_time = time.time()
        
        # Вызов оригинальной функции
        result = func(*args, **kwargs)
        print(111)
        # Код ПОСЛЕ вызова оригинальной функции
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        
        return result              # 4. Возвращаем результат оригинальной функции
    
    return wrapper                 # 5. Возвращаем функцию-обертку



@timer
def slow_function():
    """Медленная функция для демонстрации"""
    time.sleep(3)
    return "Готово!"


print(slow_function())


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
