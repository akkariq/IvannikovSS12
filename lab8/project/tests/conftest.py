# tests/conftest.py
"""
Конфигурация pytest и глобальные фикстуры для лабораторной работы №8

Содержит:
- Фикстуры для всех частей работы
- Конфигурацию pytest
- Вспомогательные функции тестирования
"""

import pytest
from unittest.mock import Mock

# Импорты из исходного кода
from source_code import (
    Employee,
    Manager,
    Developer,
    Salesperson,
    EmployeeFactory,
    Department,
    Project,
    Company,
    DatabaseConnection,
    EmployeeBuilder
)



# ============================================================================
# ФИКСТУРЫ ЧАСТЬ 1: EMPLOYEE
# ============================================================================

@pytest.fixture
def basic_employee():
    """Фикстура: базовый сотрудник"""
    return Employee(1, "John Doe", "IT", 5000)


@pytest.fixture
def test_employee_data():
    """Фикстура: данные для создания сотрудника"""
    return {
        "id": 1,
        "name": "Alice",
        "department": "HR",
        "base_salary": 4500
    }


# ============================================================================
# ФИКСТУРЫ ЧАСТЬ 2: ИЕРАРХИЯ КЛАССОВ
# ============================================================================

@pytest.fixture
def test_manager():
    """Фикстура: менеджер"""
    return Manager(2, "Jane Smith", "Management", 6000, 1000)


@pytest.fixture
def test_developer():
    """Фикстура: разработчик"""
    return Developer(3, "Bob Johnson", "Development", 5500, ["Python", "JavaScript"], "senior")


@pytest.fixture
def test_salesperson():
    """Фикстура: продавец"""
    return Salesperson(4, "Carol White", "Sales", 4000, 0.1, 100000)


@pytest.fixture
def test_factory():
    """Фикстура: фабрика сотрудников"""
    return EmployeeFactory()


# ============================================================================
# ФИКСТУРЫ ЧАСТЬ 3: МАГИЧЕСКИЕ МЕТОДЫ
# ============================================================================

@pytest.fixture
def test_department():
    """Фикстура: отдел"""
    dept = Department("IT")
    dept.add_employee(Employee(1, "Alice", "IT", 5000))
    dept.add_employee(Employee(2, "Bob", "IT", 5500))
    return dept


@pytest.fixture
def employee_list():
    """Фикстура: список сотрудников"""
    return [
        Employee(1, "Alice", "IT", 5000),
        Employee(2, "Bob", "IT", 5500),
        Employee(3, "Charlie", "IT", 6000)
    ]


# ============================================================================
# ФИКСТУРЫ ЧАСТЬ 4: КОМПОЗИЦИЯ
# ============================================================================

@pytest.fixture
def test_project():
    """Фикстура: проект"""
    return Project(1, "AI Platform", "Development", "2024-12-31")


@pytest.fixture
def test_company():
    """Фикстура: компания"""
    return Company("TechCorp")


@pytest.fixture
def test_company_with_employees():
    """Фикстура: компания с сотрудниками"""
    company = Company("TechCorp")
    company.hire_employee(Employee(1, "Alice", "IT", 5000))
    company.hire_employee(Manager(2, "Bob", "MGMT", 5000, 1000))
    company.hire_employee(Developer(3, "Charlie", "DEV", 5000, ["Python"], "senior"))
    return company


# ============================================================================
# ФИКСТУРЫ ЧАСТЬ 5: ПАТТЕРНЫ
# ============================================================================

@pytest.fixture
def test_database():
    """Фикстура: Singleton база данных"""
    return DatabaseConnection()


@pytest.fixture
def test_builder():
    """Фикстура: Builder"""
    return EmployeeBuilder()


@pytest.fixture
def mock_observer():
    """Фикстура: mock-объект наблюдателя"""
    return Mock()


# ============================================================================
# ГЛОБАЛЬНЫЕ ФИКСТУРЫ
# ============================================================================

@pytest.fixture(scope="session")
def setup_test_environment():
    """Инициализация окружения для всех тестов"""
    print("\n=== Инициализация тестового окружения ===")
    yield
    print("\n=== Завершение тестов ===")


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def create_sample_employees(count=5):
    """Вспомогательная функция: создать список сотрудников"""
    employees = []
    for i in range(1, count + 1):
        if i % 3 == 0:
            employees.append(Manager(i, f"Manager{i}", "MGMT", 5000, 1000))
        elif i % 3 == 1:
            employees.append(Developer(i, f"Dev{i}", "DEV", 5000, ["Python"], "middle"))
        else:
            employees.append(Salesperson(i, f"Sales{i}", "SALES", 4000, 0.1, 50000))
    return employees


def create_sample_department(name="IT", employee_count=3):
    """Вспомогательная функция: создать отдел с сотрудниками"""
    dept = Department(name)
    for i in range(1, employee_count + 1):
        dept.add_employee(Employee(i, f"Employee{i}", name, 5000))
    return dept