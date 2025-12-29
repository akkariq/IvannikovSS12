# tests/test_part3_magic_methods.py
"""
Тесты для части 3: Полиморфизм и магические методы

Тестирует:
- Перегрузку операторов (__eq__, __lt__, __add__)
- Магические методы коллекции (__len__, __getitem__, __contains__)
- Итерацию (__iter__)
- Сериализацию (to_dict, from_dict)
"""

import pytest
from source_code import Employee, Department, Developer


class TestMagicMethodsComparison:
    """Тесты операторов сравнения"""
    
    def test_employee_equality_by_id(self):
        """Test: Сравнение по ID"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000)
        emp3 = Employee(2, "Bob", "IT", 5000)
        
        assert emp1 == emp2
        assert emp1 != emp3
    
    def test_employee_less_than(self):
        """Test: Сравнение по зарплате"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        assert emp1 < emp2
        assert not (emp2 < emp1)
    
    def test_employee_less_equal(self):
        """Test: Сравнение меньше или равно"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 5000)
        
        assert emp1 <= emp2


class TestMagicMethodsArithmetic:
    """Тесты арифметических операторов"""
    
    def test_employee_addition(self):
        """Test: Сложение зарплат"""
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        result = emp1 + emp2
        assert result == 11000
    
    def test_sum_employee_list(self):
        """Test: Сумма зарплат списка"""
        employees = [
            Employee(1, "A", "IT", 5000),
            Employee(2, "B", "HR", 6000),
            Employee(3, "C", "FIN", 5500),
        ]
        total = sum([emp.base_salary for emp in employees])
        assert total == 16500


class TestMagicMethodsCollection:
    """Тесты методов коллекции"""
    
    def test_department_len(self):
        """Test: Количество сотрудников"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        assert len(dept) == 0
        dept.add_employee(emp)
        assert len(dept) == 1
    
    def test_department_getitem(self):
        """Test: Доступ по индексу"""
        dept = Department("IT")
        emp1 = Employee(1, "A", "IT", 5000)
        emp2 = Employee(2, "B", "IT", 6000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        assert dept[0].name == "A"
        assert dept[1].name == "B"
    
    def test_department_contains(self):
        """Test: Проверка вхождения"""
        dept = Department("IT")
        emp1 = Employee(1, "A", "IT", 5000)
        emp2 = Employee(2, "B", "IT", 6000)
        
        dept.add_employee(emp1)
        
        assert emp1 in dept
        assert emp2 not in dept


class TestMagicMethodsIteration:
    """Тесты итерации"""
    
    def test_department_iteration(self):
        """Test: Итерация по отделу"""
        dept = Department("IT")
        dept.add_employee(Employee(1, "A", "IT", 5000))
        dept.add_employee(Employee(2, "B", "IT", 6000))
        
        names = [emp.name for emp in dept]
        assert names == ["A", "B"]
    
    def test_developer_skills_iteration(self):
        """Test: Итерация по навыкам"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "senior")
        skills = list(dev.tech_stack)
        assert "Python" in skills
        assert "Java" in skills


class TestSerialization:
    """Тесты сериализации"""
    
    def test_employee_to_dict(self):
        """Test: Сериализация в словарь"""
        emp = Employee(1, "Alice", "IT", 5000)
        data = emp.to_dict()
        
        assert data["id"] == 1
        assert data["name"] == "Alice"
        assert data["department"] == "IT"
        assert data["base_salary"] == 5000
    
    def test_employee_from_dict(self):
        """Test: Десериализация из словаря"""
        original = Employee(1, "Alice", "IT", 5000)
        data = original.to_dict()
        
        restored = Employee.from_dict(data)
        
        assert restored.id == original.id
        assert restored.name == original.name
    
    def test_serialization_roundtrip(self):
        """Test: Двусторонняя сериализация"""
        original = Employee(1, "Alice", "IT", 5000)
        
        # Сериализация
        data = original.to_dict()
        
        # Десериализация
        restored = Employee.from_dict(data)
        
        # Проверка
        assert original == restored