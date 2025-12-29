# tests/test_part2_hierarchy.py
"""
Тесты для части 2: Наследование

Тестирует:
- Абстрактные классы
- Иерархия классов (Manager, Developer, Salesperson)
- Фабрика
- Полиморфизм
"""

import pytest
from source_code import (
    AbstractEmployee,
    Employee,
    Manager,
    Developer,
    Salesperson,
    EmployeeFactory
)


class TestAbstractEmployee:
    """Тесты абстрактного класса"""
    
    def test_cannot_instantiate_abstract(self):
        """Test: Абстрактный класс нельзя создать"""
        with pytest.raises(TypeError):
            AbstractEmployee(1, "John", "IT", 5000)


class TestManager:
    """Тесты класса Manager"""
    
    def test_manager_salary_calculation(self):
        """Test: Расчет зарплаты менеджера с бонусом"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        salary = manager.calculate_salary()
        assert salary == 6000
    
    def test_manager_get_info_includes_bonus(self):
        """Test: Информация включает бонус"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        info = manager.get_info()
        assert "бонус: 1000" in info
    
    def test_manager_bonus_setter(self):
        """Test: Сеттер для бонуса"""
        manager = Manager(1, "John", "Management", 5000, 1000)
        manager.bonus = 2000
        assert manager.calculate_salary() == 7000


class TestDeveloper:
    """Тесты класса Developer"""
    
    @pytest.mark.parametrize("level,multiplier", [
        ("junior", 1.0),
        ("middle", 1.5),
        ("senior", 2.0),
    ])
    def test_developer_salary_by_level(self, level, multiplier):
        """Test: Зарплата по уровню"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
        salary = dev.calculate_salary()
        assert salary == 5000 * multiplier
    
    def test_developer_add_skill(self):
        """Test: Добавление навыка"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        dev.add_skill("Java")
        assert "Java" in dev.tech_stack
    
    def test_developer_skills_display(self):
        """Test: Отображение навыков"""
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "JavaScript"], "middle")
        info = dev.get_info()
        assert "Python" in info
        assert "JavaScript" in info


class TestSalesperson:
    """Тесты класса Salesperson"""
    
    def test_salesperson_commission_calculation(self):
        """Test: Расчет зарплаты с комиссией"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.1, 150000)
        salary = sp.calculate_salary()
        assert salary == 4000 + (0.1 * 150000)
        assert salary == 19000
    
    def test_salesperson_update_sales(self):
        """Test: Обновление объема продаж"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.1, 100000)
        sp.update_sales(50000)
        assert sp.calculate_salary() == 19000
    
    def test_salesperson_commission_rate(self):
        """Test: Процент комиссии"""
        sp = Salesperson(1, "Bob", "Sales", 4000, 0.15, 100000)
        salary = sp.calculate_salary()
        assert salary == 4000 + (0.15 * 100000)


class TestEmployeeFactory:
    """Тесты фабрики сотрудников"""
    
    def test_factory_create_manager(self):
        """Test: Создание менеджера"""
        factory = EmployeeFactory()
        manager = factory.create_employee(
            "manager",
            id=1,
            name="John",
            department="MGMT",
            base_salary=5000,
            bonus=1000
        )
        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 6000
    
    def test_factory_create_developer(self):
        """Test: Создание разработчика"""
        factory = EmployeeFactory()
        dev = factory.create_employee(
            "developer",
            id=1,
            name="Alice",
            department="DEV",
            base_salary=5000,
            skills=["Python"],
            seniority="senior"
        )
        assert isinstance(dev, Developer)
        assert dev.calculate_salary() == 10000
    
    def test_factory_create_salesperson(self):
        """Test: Создание продавца"""
        factory = EmployeeFactory()
        sp = factory.create_employee(
            "salesperson",
            id=1,
            name="Bob",
            department="SALES",
            base_salary=4000,
            commission_rate=0.1,
            sales_volume=100000
        )
        assert isinstance(sp, Salesperson)
    
    def test_factory_create_employee(self):
        """Test: Создание обычного сотрудника"""
        factory = EmployeeFactory()
        emp = factory.create_employee(
            "employee",
            id=1,
            name="John",
            department="IT",
            base_salary=5000
        )
        assert isinstance(emp, Employee)


class TestPolymorphism:
    """Тесты полиморфизма"""
    
    def test_polymorphic_salary_calculation(self):
        """Test: Полиморфный расчет зарплат"""
        employees = [
            Employee(1, "A", "IT", 5000),
            Manager(2, "B", "MGMT", 5000, 1000),
            Developer(3, "C", "DEV", 5000, ["Python"], "senior"),
        ]
        
        salaries = [emp.calculate_salary() for emp in employees]
        total = sum(salaries)
        
        assert salaries == [5000, 6000, 10000]
        assert total == 21000