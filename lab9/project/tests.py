"""
UNIT-ТЕСТЫ ДЛЯ РЕФАКТОРИННОГО КОДА (ЛР №9)
Использует pytest для тестирования SOLID принципов
"""

import pytest
from typing import List
from refactored_code import (
    # Валидаторы
    PositiveNumberValidator,
    StringNotEmptyValidator,
    
    # Стратегии зарплаты
    DeveloperSalaryStrategy,
    ManagerSalaryStrategy,
    SalespersonSalaryStrategy,
    
    # Стратегии бонусов
    PerformanceBonusStrategy,
    SeniorityBonusStrategy,
    
    # Классы сотрудников
    Employee,
    Developer,
    Manager,
    Salesperson,
    
    # Репозиторий и компания
    InMemoryEmployeeRepository,
    Company,
)

# ===================== ТЕСТЫ ВАЛИДАТОРОВ =====================

class TestPositiveNumberValidator:
    """Тесты для валидатора положительных чисел"""
    
    @pytest.fixture
    def validator(self):
        return PositiveNumberValidator()
    
    def test_valid_positive_number(self, validator):
        """Должен принять положительное число"""
        assert validator.validate(100) == 100.0
        assert validator.validate(0.5) == 0.5
    
    def test_zero_is_valid(self, validator):
        """Ноль считается положительным"""
        assert validator.validate(0) == 0.0
    
    def test_negative_number_raises_error(self, validator):
        """Должен отклонить отрицательное число"""
        with pytest.raises(ValueError):
            validator.validate(-100)
    
    def test_string_number_conversion(self, validator):
        """Должен конвертировать строку в число"""
        assert validator.validate("50") == 50.0
    
    def test_invalid_string_raises_error(self, validator):
        """Должен отклонить невалидную строку"""
        with pytest.raises(ValueError):
            validator.validate("not_a_number")


class TestStringNotEmptyValidator:
    """Тесты для валидатора непустой строки"""
    
    @pytest.fixture
    def validator(self):
        return StringNotEmptyValidator()
    
    def test_valid_string(self, validator):
        """Должен принять непустую строку"""
        assert validator.validate("John") == "John"
        assert validator.validate("  Alice  ") == "Alice"
    
    def test_empty_string_raises_error(self, validator):
        """Должен отклонить пустую строку"""
        with pytest.raises(ValueError):
            validator.validate("")
    
    def test_whitespace_only_raises_error(self, validator):
        """Должен отклонить строку только из пробелов"""
        with pytest.raises(ValueError):
            validator.validate("   ")
    
    def test_none_raises_error(self, validator):
        """Должен отклонить None"""
        with pytest.raises(ValueError):
            validator.validate(None)


# ==================== ТЕСТЫ СТРАТЕГИЙ ЗАРПЛАТЫ ====================

class TestDeveloperSalaryStrategy:
    """Тесты для зарплаты разработчика (зависит от опыта)"""
    
    @pytest.fixture
    def strategy(self):
        return DeveloperSalaryStrategy()
    
    def test_junior_developer(self, strategy):
        """Junior разработчик: 1x от базовой"""
        assert strategy.calculate(base_salary=1000, seniority="junior") == 1000
    
    def test_middle_developer(self, strategy):
        """Middle разработчик: 1.5x от базовой"""
        assert strategy.calculate(base_salary=1000, seniority="middle") == 1500
    
    def test_senior_developer(self, strategy):
        """Senior разработчик: 2x от базовой"""
        assert strategy.calculate(base_salary=1000, seniority="senior") == 2000
    
    def test_unknown_seniority_defaults_to_junior(self, strategy):
        """Неизвестный уровень = Junior"""
        assert strategy.calculate(base_salary=1000, seniority="unknown") == 1000
    
    def test_calculation_with_different_salaries(self, strategy):
        """Расчет с разными базовыми зарплатами"""
        assert strategy.calculate(base_salary=2000, seniority="senior") == 4000
        assert strategy.calculate(base_salary=3000, seniority="middle") == 4500


class TestManagerSalaryStrategy:
    """Тесты для зарплаты менеджера (базовая + бонус)"""
    
    @pytest.fixture
    def strategy(self):
        return ManagerSalaryStrategy()
    
    def test_salary_without_bonus(self, strategy):
        """Только базовая зарплата"""
        assert strategy.calculate(base_salary=5000) == 5000
    
    def test_salary_with_bonus(self, strategy):
        """Базовая + фиксированный бонус"""
        assert strategy.calculate(base_salary=5000, bonus=1000) == 6000
    
    def test_salary_with_large_bonus(self, strategy):
        """Большой бонус"""
        assert strategy.calculate(base_salary=5000, bonus=3000) == 8000
    
    def test_zero_bonus(self, strategy):
        """Нулевой бонус = только базовая"""
        assert strategy.calculate(base_salary=5000, bonus=0) == 5000


class TestSalespersonSalaryStrategy:
    """Тесты для зарплаты продавца (базовая + комиссия)"""
    
    @pytest.fixture
    def strategy(self):
        return SalespersonSalaryStrategy()
    
    def test_no_sales(self, strategy):
        """Без продаж = только базовая"""
        assert strategy.calculate(base_salary=2000) == 2000
    
    def test_with_sales_default_rate(self, strategy):
        """Продажи с комиссией 10% по умолчанию"""
        result = strategy.calculate(base_salary=2000, total_sales=5000)
        assert result == 2000 + 500  # 2000 + 5000*0.1
    
    def test_with_custom_commission_rate(self, strategy):
        """Пользовательская ставка комиссии"""
        result = strategy.calculate(
            base_salary=2000, 
            commission_rate=0.15, 
            total_sales=5000
        )
        assert result == 2000 + 750  # 2000 + 5000*0.15
    
    def test_high_commission_rate(self, strategy):
        """Высокая комиссия (20%)"""
        result = strategy.calculate(
            base_salary=2000,
            commission_rate=0.20,
            total_sales=10000
        )
        assert result == 2000 + 2000  # 2000 + 10000*0.20


# ==================== ТЕСТЫ СТРАТЕГИЙ БОНУСОВ ====================

class TestPerformanceBonusStrategy:
    """Тесты для бонуса за производительность (10% от базовой)"""
    
    @pytest.fixture
    def strategy(self):
        return PerformanceBonusStrategy()
    
    def test_bonus_calculation(self, strategy):
        """Бонус = 10% от базовой зарплаты"""
        assert strategy.calculate_bonus(base_salary=1000) == 100
        assert strategy.calculate_bonus(base_salary=5000) == 500
    
    def test_zero_salary_zero_bonus(self, strategy):
        """Нулевая зарплата = нулевой бонус"""
        assert strategy.calculate_bonus(base_salary=0) == 0
    
    def test_large_salary_large_bonus(self, strategy):
        """Большая зарплата = большой бонус"""
        assert strategy.calculate_bonus(base_salary=10000) == 1000


class TestSeniorityBonusStrategy:
    """Тесты для бонуса за опыт (зависит от уровня)"""
    
    @pytest.fixture
    def strategy(self):
        return SeniorityBonusStrategy()
    
    def test_junior_bonus(self, strategy):
        """Junior: 5% от базовой"""
        assert strategy.calculate_bonus(base_salary=1000, seniority="junior") == 50
    
    def test_middle_bonus(self, strategy):
        """Middle: 10% от базовой"""
        assert strategy.calculate_bonus(base_salary=1000, seniority="middle") == 100
    
    def test_senior_bonus(self, strategy):
        """Senior: 20% от базовой"""
        assert strategy.calculate_bonus(base_salary=1000, seniority="senior") == 200
    
    def test_unknown_seniority_defaults_to_junior(self, strategy):
        """Неизвестный уровень = Junior (5%)"""
        assert strategy.calculate_bonus(base_salary=1000, seniority="unknown") == 50
    
    def test_bonus_scales_with_salary(self, strategy):
        """Бонус масштабируется с зарплатой"""
        assert strategy.calculate_bonus(base_salary=2000, seniority="senior") == 400
        assert strategy.calculate_bonus(base_salary=5000, seniority="middle") == 500


# ==================== ТЕСТЫ КЛАССОВ СОТРУДНИКОВ ====================

class TestEmployeeBase:
    """Тесты для базового класса Employee"""
    
    @pytest.fixture
    def employee(self):
        from refactored_code import DeveloperSalaryStrategy, PerformanceBonusStrategy
        return Employee(
            name="John Doe",
            department="IT",
            base_salary=5000,
            employee_id=1,
            salary_strategy=DeveloperSalaryStrategy(),
            bonus_strategy=PerformanceBonusStrategy()
        )
    
    def test_employee_creation(self, employee):
        """Сотрудник должен создаться с корректными параметрами"""
        assert employee.name == "John Doe"
        assert employee.base_salary == 5000
        assert employee.id == 1
    
    def test_invalid_name_raises_error(self):
        """Пустое имя должно вызвать ошибку"""
        from refactored_code import DeveloperSalaryStrategy, PerformanceBonusStrategy
        with pytest.raises(ValueError):
            Employee(
                name="",
                department="IT",
                base_salary=5000,
                salary_strategy=DeveloperSalaryStrategy(),
                bonus_strategy=PerformanceBonusStrategy()
            )
    
    def test_invalid_salary_raises_error(self):
        """Отрицательная зарплата должна вызвать ошибку"""
        from refactored_code import DeveloperSalaryStrategy, PerformanceBonusStrategy
        with pytest.raises(ValueError):
            Employee(
                name="John",
                department="IT",
                base_salary=-5000,
                salary_strategy=DeveloperSalaryStrategy(),
                bonus_strategy=PerformanceBonusStrategy()
            )
    
    def test_employee_to_dict(self, employee):
        """Конвертация в словарь"""
        data = employee.to_dict()
        assert data["name"] == "John Doe"
        assert data["id"] == 1
        assert "total_salary" in data


class TestDeveloper:
    """Тесты для класса Developer"""
    
    @pytest.fixture
    def junior_dev(self):
        return Developer(
            name="Alice",
            department="DEV",
            base_salary=2000,
            seniority="junior",
            employee_id=1
        )
    
    @pytest.fixture
    def senior_dev(self):
        return Developer(
            name="Bob",
            department="DEV",
            base_salary=3000,
            seniority="senior",
            employee_id=2
        )
    
    def test_junior_developer_salary(self, junior_dev):
        """Junior разработчик: 2000 * 1.0 + (2000 * 0.05) = 2100"""
        assert junior_dev.calculate_salary() == 2100
    
    def test_senior_developer_salary(self, senior_dev):
        """Senior разработчик: 3000 * 2.0 + (3000 * 0.20) = 6600"""
        assert senior_dev.calculate_salary() == 6600
    
    def test_developer_with_skills(self):
        """Разработчик со скиллами"""
        dev = Developer(
            name="Charlie",
            department="DEV",
            base_salary=2500,
            seniority="middle",
            skills=["Python", "Docker", "Kubernetes"],
            employee_id=3
        )
        # Проверяем что skills есть в to_dict() (если реализовано)
        # или просто проверяем что объект создан
        assert dev.name == "Charlie"
        assert dev.base_salary == 2500
    
    def test_developer_info(self, junior_dev):
        """Информация о разработчике"""
        info = junior_dev.get_info()
        assert "Alice" in info
        assert "2100" in info


class TestManager:
    """Тесты для класса Manager"""
    
    @pytest.fixture
    def manager(self):
        return Manager(
            name="Diana",
            department="MGMT",
            base_salary=5000,
            bonus=2000,
            employee_id=1
        )
    
    def test_manager_salary(self, manager):
        """Manager: 5000 + 2000 + (5000 * 0.1) = 7500"""
        assert manager.calculate_salary() == 7500
    
    def test_manager_without_bonus(self):
        """Manager без бонуса: 4000 + 0 + (4000 * 0.1) = 4400"""
        mgr = Manager(
            name="Eve",
            department="MGMT",
            base_salary=4000,
            bonus=0,
            employee_id=2
        )
        assert mgr.calculate_salary() == 4400
    
    def test_manager_with_large_bonus(self):
        """Manager с большим бонусом"""
        mgr = Manager(
            name="Frank",
            department="MGMT",
            base_salary=6000,
            bonus=3000,
            employee_id=3
        )
        assert mgr.calculate_salary() == 9600  # 6000 + 3000 + 600


class TestSalesperson:
    """Тесты для класса Salesperson"""
    
    @pytest.fixture
    def salesperson(self):
        return Salesperson(
            name="George",
            department="SALES",
            base_salary=2000,
            commission_rate=0.10,
            employee_id=1
        )
    
    def test_salesperson_no_sales(self, salesperson):
        """Salesperson без продаж: 2000 + 0 = 2000"""
        assert salesperson.calculate_salary() == 2000
    
    def test_salesperson_with_sales(self, salesperson):
        """Salesperson с продажами"""
        salesperson.add_sales(5000)
        # 2000 + (5000 * 0.10) = 2500
        assert salesperson.calculate_salary() == 2500
    
    def test_salesperson_with_multiple_sales(self, salesperson):
        """Salesperson с несколькими продажами"""
        salesperson.add_sales(5000)
        salesperson.add_sales(3000)
        # 2000 + (8000 * 0.10) = 2800
        assert salesperson.calculate_salary() == 2800
    
    def test_salesperson_with_high_commission_rate(self):
        """Salesperson с высокой комиссией (20%)"""
        sales = Salesperson(
            name="Helen",
            department="SALES",
            base_salary=2000,
            commission_rate=0.20,
            employee_id=2
        )
        sales.add_sales(10000)
        # 2000 + (10000 * 0.20) = 4000
        assert sales.calculate_salary() == 4000


# ==================== ТЕСТЫ РЕПОЗИТОРИЯ ====================

class TestInMemoryEmployeeRepository:
    """Тесты для репозитория сотрудников в памяти"""
    
    @pytest.fixture
    def repository(self):
        return InMemoryEmployeeRepository()
    
    @pytest.fixture
    def employee(self):
        return Employee(
            name="Test Employee",
            department="IT",
            base_salary=5000,
            employee_id=1,
            salary_strategy=DeveloperSalaryStrategy(),
            bonus_strategy=PerformanceBonusStrategy()
        )
    
    def test_add_employee(self, repository, employee):
        """Должна добавиться"""
        repository.add(employee)
        employees = repository.get_all()
        assert len(employees) == 1
        assert employees[0].name == "Test Employee"
    
    def test_add_multiple_employees(self, repository):
        """Должны добавиться несколько сотрудников"""
        emp1 = Developer("Alice", "DEV", 2000, employee_id=1)
        emp2 = Developer("Bob", "DEV", 3000, employee_id=2)
        
        repository.add(emp1)
        repository.add(emp2)
        
        assert len(repository.get_all()) == 2
    
    def test_get_all_returns_list(self, repository, employee):
        """Должна вернуть список"""
        repository.add(employee)
        employees = repository.get_all()
        assert isinstance(employees, list)
        assert len(employees) == 1


# ==================== ТЕСТЫ КОМПАНИИ ====================

class TestCompany:
    """Тесты для класса Company"""
    
    @pytest.fixture
    def company(self):
        return Company("TechCorp", InMemoryEmployeeRepository())
    
    @pytest.fixture
    def employees(self):
        return [
            Developer("Alice", "DEV", 2000, seniority="junior", employee_id=1),
            Developer("Bob", "DEV", 3000, seniority="senior", employee_id=2),
            Manager("Diana", "MGMT", 5000, bonus=1000, employee_id=3),
        ]
    
    def test_hire_employee(self, company, employees):
        """Должен нанять сотрудника"""
        company.hire_employee(employees[0])
        assert company.get_employee_count() == 1
    
    def test_hire_multiple_employees(self, company, employees):
        """Должен нанять нескольких сотрудников"""
        for emp in employees:
            company.hire_employee(emp)
        assert company.get_employee_count() == 3
    
    def test_calculate_total_salary(self, company, employees):
        """Должна посчитаться общая зарплата"""
        for emp in employees:
            company.hire_employee(emp)
        
        total = company.calculate_total_salary()
        assert total > 0
        
        # Проверка примерно:
        # Alice: 2000 * 1.0 + 100 = 2100
        # Bob: 3000 * 2.0 + 600 = 6600
        # Diana: 5000 + 1000 + 500 = 6500
        # Total: 15200
        assert total == 15200
    
    def test_empty_company(self, company):
        """Пустая компания"""
        assert company.get_employee_count() == 0
        assert company.calculate_total_salary() == 0
    
    def test_get_all_employees(self, company, employees):
        """Должны вернуться все сотрудники"""
        for emp in employees:
            company.hire_employee(emp)
        
        all_emps = company.get_all_employees()
        assert len(all_emps) == 3


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================

class TestIntegration:
    """Интеграционные тесты системы"""
    
    def test_full_workflow(self):
        """Полный рабочий процесс"""
        # Создание компании
        company = Company("StartupCorp", InMemoryEmployeeRepository())
        
        # Найм сотрудников
        dev = Developer(
            name="Alice",
            department="DEV",
            base_salary=4000,
            seniority="senior",
            skills=["Python", "Docker"],
            employee_id=1
        )
        
        manager = Manager(
            name="Bob",
            department="MGMT",
            base_salary=6000,
            bonus=2000,
            employee_id=2
        )
        
        salesperson = Salesperson(
            name="Charlie",
            department="SALES",
            base_salary=2000,
            commission_rate=0.15,
            employee_id=3
        )
        
        company.hire_employee(dev)
        company.hire_employee(manager)
        company.hire_employee(salesperson)
        
        # Добавление продаж
        salesperson.add_sales(10000)
        
        # Проверка
        assert company.get_employee_count() == 3
        
        # Alice: 4000 * 2.0 + 800 = 8800
        # Bob: 6000 + 2000 + 600 = 8600
        # Charlie: 2000 + 1500 = 3500
        # Total: 20900
        assert company.calculate_total_salary() == 20900
    
    def test_different_employee_types_compatibility(self):
        """Все типы сотрудников совместимы (LSP)"""
        employees: List[Employee] = [
            Developer("Alice", "DEV", 2000, employee_id=1),
            Manager("Bob", "MGMT", 5000, employee_id=2),
            Salesperson("Charlie", "SALES", 2000, employee_id=3),
        ]
        
        # Все должны работать одинаково
        total = sum(emp.calculate_salary() for emp in employees)
        assert total > 0
        
        # Все должны иметь info
        for emp in employees:
            info = emp.get_info()
            assert isinstance(info, str)
            assert len(info) > 0


# ==================== ФИКСЧЕРЫ ДЛЯ ПЕРЕИСПОЛЬЗОВАНИЯ ====================

@pytest.fixture(scope="session")
def all_strategies():
    """Все стратегии для тестирования"""
    return {
        "dev": DeveloperSalaryStrategy(),
        "mgr": ManagerSalaryStrategy(),
        "sales": SalespersonSalaryStrategy(),
        "perf_bonus": PerformanceBonusStrategy(),
        "sen_bonus": SeniorityBonusStrategy(),
    }


@pytest.fixture(scope="session")
def sample_company():
    """Компания с примерными сотрудниками"""
    company = Company("SampleCorp", InMemoryEmployeeRepository())
    
    employees = [
        Developer("Alice", "DEV", 2000, seniority="junior", employee_id=1),
        Developer("Bob", "DEV", 3000, seniority="middle", employee_id=2),
        Developer("Charlie", "DEV", 4000, seniority="senior", employee_id=3),
        Manager("Diana", "MGMT", 5000, bonus=1000, employee_id=4),
        Manager("Eve", "MGMT", 6000, bonus=1500, employee_id=5),
        Salesperson("Frank", "SALES", 2000, commission_rate=0.10, employee_id=6),
        Salesperson("Grace", "SALES", 2500, commission_rate=0.15, employee_id=7),
    ]
    
    for emp in employees:
        company.hire_employee(emp)
    
    return company


# ==================== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ ====================

@pytest.mark.parametrize("base_salary,seniority,expected_multiplier,expected_bonus_rate", [
    (1000, "junior", 1.0, 0.05),
    (1000, "middle", 1.5, 0.10),
    (1000, "senior", 2.0, 0.20),
    (2000, "junior", 1.0, 0.05),
    (2000, "senior", 2.0, 0.20),
])
def test_developer_salary_parametrized(base_salary, seniority, expected_multiplier, expected_bonus_rate):
    """Параметризованный тест для зарплаты разработчика"""
    dev = Developer(
        "Test",
        "DEV",
        base_salary,
        seniority=seniority,
        employee_id=1
    )
    
    actual = dev.calculate_salary()
    expected = base_salary * expected_multiplier + base_salary * expected_bonus_rate
    assert actual == expected


@pytest.mark.parametrize("base_salary,bonus,expected", [
    (1000, 0, 1100),        # 1000 + 0 + 100 (10% бонус за производительность)
    (1000, 500, 1600),      # 1000 + 500 + 100
    (5000, 1000, 6500),     # 5000 + 1000 + 500 (ИСПРАВЛЕНО: было 6600)
    (4000, 0, 4400),        # 4000 + 0 + 400
    (2000, 1000, 3200),     # 2000 + 1000 + 300
])
def test_manager_salary_parametrized(base_salary, bonus, expected):
    """Параметризованный тест для зарплаты менеджера"""
    mgr = Manager(
        "Test",
        "MGMT",
        base_salary,
        bonus=bonus,
        employee_id=1
    )
    assert mgr.calculate_salary() == expected


# ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================

class TestEdgeCases:
    """Тесты на граничные случаи"""
    
    def test_zero_salary_employee(self):
        """Сотрудник с нулевой зарплатой"""
        dev = Developer("Test", "DEV", 0, seniority="junior", employee_id=1)
        assert dev.calculate_salary() == 0  # 0 * 1.0 + 0 * 0.05
    
    def test_very_large_salary(self):
        """Очень большая зарплата"""
        mgr = Manager("Test", "MGMT", 999999, bonus=100000, employee_id=1)
        salary = mgr.calculate_salary()
        assert salary == 999999 + 100000 + 99999.9  # base + bonus + perf_bonus
    
    def test_salesperson_no_commission_rate(self):
        """Продавец без комиссии (0%)"""
        sales = Salesperson("Test", "SALES", 3000, commission_rate=0, employee_id=1)
        sales.add_sales(100000)
        assert sales.calculate_salary() == 3000  # Только базовая зарплата


class TestValidationErrors:
    """Тесты на ошибки валидации"""
    
    def test_negative_salary_validation(self):
        """Отрицательная зарплата вызывает ошибку"""
        with pytest.raises(ValueError):
            Developer("Test", "DEV", -1000, employee_id=1)
    
    def test_empty_name_validation(self):
        """Пустое имя вызывает ошибку"""
        with pytest.raises(ValueError):
            Manager("", "MGMT", 5000, employee_id=1)
    
    def test_negative_sales_validation(self):
        """Отрицательные продажи вызывают ошибку"""
        sales = Salesperson("Test", "SALES", 2000, employee_id=1)
        with pytest.raises(ValueError):
            sales.add_sales(-5000)


# ==================== ТЕСТЫ ИНТЕРФЕЙСОВ ====================

class TestInterfaceCompliance:
    """Тесты на соответствие интерфейсам"""
    
    def test_all_employees_are_salary_calculable(self):
        """Все сотрудники реализуют ISalaryCalculable"""
        employees = [
            Developer("A", "DEV", 2000, employee_id=1),
            Manager("B", "MGMT", 5000, employee_id=2),
            Salesperson("C", "SALES", 2000, employee_id=3),
        ]
        
        for emp in employees:
            # Все должны иметь метод calculate_salary
            assert hasattr(emp, 'calculate_salary')
            assert callable(getattr(emp, 'calculate_salary'))
            assert isinstance(emp.calculate_salary(), (int, float))
    
    def test_all_employees_are_info_providable(self):
        """Все сотрудники реализуют IInfoProvidable"""
        employees = [
            Developer("A", "DEV", 2000, employee_id=1),
            Manager("B", "MGMT", 5000, employee_id=2),
            Salesperson("C", "SALES", 2000, employee_id=3),
        ]
        
        for emp in employees:
            # Все должны иметь метод get_info
            assert hasattr(emp, 'get_info')
            assert callable(getattr(emp, 'get_info'))
            info = emp.get_info()
            assert isinstance(info, str)
            assert len(info) > 0
    
    def test_all_employees_are_serializable(self):
        """Все сотрудники реализуют ISerializable"""
        employees = [
            Developer("A", "DEV", 2000, employee_id=1),
            Manager("B", "MGMT", 5000, employee_id=2),
            Salesperson("C", "SALES", 2000, employee_id=3),
        ]
        
        for emp in employees:
            # Все должны иметь метод to_dict
            assert hasattr(emp, 'to_dict')
            assert callable(getattr(emp, 'to_dict'))
            data = emp.to_dict()
            assert isinstance(data, dict)
            assert 'name' in data
            assert 'total_salary' in data


if __name__ == "__main__":
    # Запуск тестов из командной строки
    pytest.main([__file__, "-v", "--tb=short"])
