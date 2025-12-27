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