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
