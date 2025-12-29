# tests/test_part5_patterns.py
"""
Тесты для части 5: Паттерны проектирования

Тестирует:
- Singleton (DatabaseConnection)
- Builder (EmployeeBuilder)
- Factory Method (EmployeeFactory)
- Adapter, Decorator, Observer
"""

import pytest
from unittest.mock import Mock
from source_code import (
    Employee,
    Manager,
    Developer,
    DatabaseConnection,
    EmployeeBuilder,
    SalaryAdapter,
    BonusDecorator
)


class TestSingletonPattern:
    """Тесты паттерна Singleton"""
    
    def test_singleton_database_connection(self):
        """Test: Singleton для БД"""
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        
        assert db1 is db2
        assert id(db1) == id(db2)
    
    def test_singleton_connection_state(self):
        """Test: Состояние Singleton сохраняется"""
        db1 = DatabaseConnection()
        db2 = DatabaseConnection()
        
        # Они одинаковые
        assert db1 is db2


class TestBuilderPattern:
    """Тесты паттерна Builder"""
    
    def test_builder_pattern_employee(self):
        """Test: Builder для Employee"""
        emp = (EmployeeBuilder()
              .set_id(1)
              .set_name("John")
              .set_department("IT")
              .set_base_salary(5000)
              .build())
        
        assert emp.id == 1
        assert emp.name == "John"
        assert emp.calculate_salary() == 5000
    
    def test_builder_pattern_developer(self):
        """Test: Builder для Developer"""
        dev = (EmployeeBuilder()
              .set_id(1)
              .set_name("Alice")
              .set_department("DEV")
              .set_base_salary(5000)
              .set_type("developer")
              .set_skills(["Python"])
              .set_seniority("senior")
              .build())
        
        assert isinstance(dev, Developer)
        assert dev.calculate_salary() == 10000
    
    def test_builder_missing_required_field(self):
        """Test: Builder требует обязательные поля"""
        with pytest.raises(ValueError):
            (EmployeeBuilder()
            .set_id(1)
            .set_name("Test")
            # Отсутствует department
            .build())
    
    def test_builder_chaining(self):
        """Test: Цепочка вызовов Builder"""
        builder = EmployeeBuilder()
        emp = (builder
               .set_id(1)
               .set_name("John")
               .set_department("IT")
               .set_base_salary(5000)
               .build())
        
        assert emp is not None


class TestFactoryMethod:
    """Тесты паттерна Factory Method"""
    
    def test_factory_creates_correct_type(self):
        """Test: Factory создает правильный тип"""
        from source_code import EmployeeFactory
        factory = EmployeeFactory()
        
        emp = factory.create_employee(
            "employee",
            id=1,
            name="John",
            department="IT",
            base_salary=5000
        )
        
        assert isinstance(emp, Employee)
        assert not isinstance(emp, Manager)
    
    def test_factory_creates_manager(self):
        """Test: Factory создает Manager"""
        from source_code import EmployeeFactory
        factory = EmployeeFactory()
        
        mgr = factory.create_employee(
            "manager",
            id=1,
            name="John",
            department="MGMT",
            base_salary=5000,
            bonus=1000
        )
        
        assert isinstance(mgr, Manager)


class TestAdapterPattern:
    """Тесты паттерна Adapter"""
    
    def test_salary_adapter(self):
        """Test: Adapter для зарплаты"""
        emp = Employee(1, "John", "IT", 5000)
        adapter = SalaryAdapter(emp)
        
        # Adapter предоставляет другой интерфейс
        assert adapter.get_monthly_salary() > 0


class TestDecoratorPattern:
    """Тесты паттерна Decorator"""
    
    def test_bonus_decorator(self):
        """Test: Decorator для добавления бонуса"""
        emp = Employee(1, "John", "IT", 5000)
        decorated = BonusDecorator(emp, 1000)
        
        salary = decorated.calculate_salary()
        assert salary == 6000
    
    def test_multiple_decorators(self):
        """Test: Несколько Decorators"""
        emp = Employee(1, "John", "IT", 5000)
        decorated = (BonusDecorator(
                      BonusDecorator(emp, 500),
                      1000))
        
        assert decorated.calculate_salary() == 6500


class TestObserverPattern:
    """Тесты паттерна Observer"""
    
    def test_observer_pattern_with_mock(self):
        """Test: Observer с Mock"""
        emp = Employee(1, "John", "IT", 5000)
        observer = Mock()
        
        emp.add_observer(observer)
        emp.notify_observers("salary_changed")
        
        observer.update.assert_called()
        observer.update.assert_called_with(emp, "salary_changed")
    
    def test_multiple_observers(self):
        """Test: Несколько observers"""
        emp = Employee(1, "John", "IT", 5000)
        observer1 = Mock()
        observer2 = Mock()
        
        emp.add_observer(observer1)
        emp.add_observer(observer2)
        emp.notify_observers("status_changed")
        
        observer1.update.assert_called()
        observer2.update.assert_called()