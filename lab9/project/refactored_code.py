"""
ИТОГОВЫЙ КОД РЕФАКТОРИНГА (ЛР №9)
Система учета сотрудников с применением SOLID принципов
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from enum import Enum
import json


# ======================== ВАЛИДАТОРЫ (SRP) ========================

class Validator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


class PositiveNumberValidator(Validator):
    def validate(self, value: Any) -> float:
        num = float(value)
        if num < 0:
            raise ValueError(f"Число должно быть положительным")
        return num


class StringNotEmptyValidator(Validator):
    def validate(self, value: Any) -> str:
        if not value or not str(value).strip():
            raise ValueError("Строка не может быть пустой")
        return str(value).strip()


# ===================== СТРАТЕГИИ ЗАРПЛАТЫ (OCP) =====================

class SalaryStrategy(ABC):
    @abstractmethod
    def calculate(self, **kwargs) -> float:
        pass


class DeveloperSalaryStrategy(SalaryStrategy):
    """Зарплата зависит от опыта"""
    MULTIPLIERS = {"junior": 1.0, "middle": 1.5, "senior": 2.0}

    def calculate(self, base_salary: float, seniority: str = "junior", **kwargs) -> float:
        multiplier = self.MULTIPLIERS.get(seniority, 1.0)
        return base_salary * multiplier


class ManagerSalaryStrategy(SalaryStrategy):
    """Базовая + фиксированный бонус"""

    def calculate(self, base_salary: float, bonus: float = 0, **kwargs) -> float:
        return base_salary + bonus


class SalespersonSalaryStrategy(SalaryStrategy):
    """Базовая + комиссия от продаж"""

    def calculate(self, base_salary: float, commission_rate: float = 0.1,
                  total_sales: float = 0, **kwargs) -> float:
        return base_salary + (total_sales * commission_rate)


# ===================== СТРАТЕГИИ БОНУСОВ =======================

class BonusStrategy(ABC):
    @abstractmethod
    def calculate_bonus(self, base_salary: float, **kwargs) -> float:
        pass


class PerformanceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, base_salary: float, **kwargs) -> float:
        return base_salary * 0.1


class SeniorityBonusStrategy(BonusStrategy):
    RATES = {"junior": 0.05, "middle": 0.10, "senior": 0.20}

    def calculate_bonus(self, base_salary: float, seniority: str = "junior", **kwargs) -> float:
        rate = self.RATES.get(seniority, 0.05)
        return base_salary * rate


# ==================== ИНТЕРФЕЙСЫ (ISP) ====================

class ISalaryCalculable(ABC):
    @abstractmethod
    def calculate_salary(self) -> float:
        pass


class IInfoProvidable(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass


class ISerializable(ABC):
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass


# ==================== ОСНОВНЫЕ КЛАССЫ ====================

class Employee(ISalaryCalculable, IInfoProvidable, ISerializable):
    """Базовый класс сотрудника (рефакторинный)"""

    def __init__(
            self,
            name: str,
            department: str,
            base_salary: float,
            employee_id: int = 0,
            salary_strategy: Optional[SalaryStrategy] = None,
            bonus_strategy: Optional[BonusStrategy] = None
    ):
        # Валидация
        self.__name = StringNotEmptyValidator().validate(name)
        self.__department = department
        self.__base_salary = PositiveNumberValidator().validate(base_salary)
        self.__id = employee_id

        # Стратегии (DIP)
        self._salary_strategy = salary_strategy or SalaryStrategy
        self._bonus_strategy = bonus_strategy or BonusStrategy

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def base_salary(self) -> float:
        return self.__base_salary

    def calculate_salary(self) -> float:
        """Расчет с использованием стратегий"""
        base = self._salary_strategy.calculate(base_salary=self.__base_salary)
        bonus = self._bonus_strategy.calculate_bonus(base_salary=self.__base_salary)
        return base + bonus

    def get_info(self) -> str:
        return f"{self.name} (ID: {self.__id}) - ${self.calculate_salary():.2f}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.__id,
            "name": self.__name,
            "department": self.__department,
            "base_salary": self.__base_salary,
            "total_salary": self.calculate_salary()
        }


class Developer(Employee):
    """Разработчик с учетом опыта"""

    def __init__(
            self,
            name: str,
            department: str,
            base_salary: float,
            seniority: str = "junior",
            skills: Optional[List[str]] = None,
            employee_id: int = 0
    ):
        self.__seniority = seniority
        self.__skills = skills or []

        super().__init__(
            name=name,
            department=department,
            base_salary=base_salary,
            employee_id=employee_id,
            salary_strategy=DeveloperSalaryStrategy(),
            bonus_strategy=SeniorityBonusStrategy()
        )

    @property
    def seniority(self) -> str:
        return self.__seniority

    def calculate_salary(self) -> float:
        return self._salary_strategy.calculate(
            base_salary=self.base_salary,
            seniority=self.__seniority
        ) + self._bonus_strategy.calculate_bonus(
            base_salary=self.base_salary,
            seniority=self.__seniority
        )


class Manager(Employee):
    """Менеджер с бонусом"""

    def __init__(
            self,
            name: str,
            department: str,
            base_salary: float,
            bonus: float = 0,
            employee_id: int = 0
    ):
        self.__bonus = bonus

        super().__init__(
            name=name,
            department=department,
            base_salary=base_salary,
            employee_id=employee_id,
            salary_strategy=ManagerSalaryStrategy(),
            bonus_strategy=PerformanceBonusStrategy()
        )

    def calculate_salary(self) -> float:
        return self._salary_strategy.calculate(
            base_salary=self.base_salary,
            bonus=self.__bonus
        ) + self._bonus_strategy.calculate_bonus(base_salary=self.base_salary)


class Salesperson(Employee):
    """Продавец с комиссией"""

    def __init__(
            self,
            name: str,
            department: str,
            base_salary: float,
            commission_rate: float = 0.1,
            employee_id: int = 0
    ):
        self.__commission_rate = commission_rate
        self.__total_sales = 0.0

        super().__init__(
            name=name,
            department=department,
            base_salary=base_salary,
            employee_id=employee_id,
            salary_strategy=SalespersonSalaryStrategy()
        )

    def add_sales(self, amount: float) -> None:
        self.__total_sales += PositiveNumberValidator().validate(amount)

    def calculate_salary(self) -> float:
        return self._salary_strategy.calculate(
            base_salary=self.base_salary,
            commission_rate=self.__commission_rate,
            total_sales=self.__total_sales
        )


# ==================== КОМПАНИЯ ====================

class IEmployeeRepository(ABC):
    @abstractmethod
    def add(self, employee: Employee) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Employee]:
        pass


class InMemoryEmployeeRepository(IEmployeeRepository):
    """Репозиторий в памяти (DIP)"""

    def __init__(self):
        self._employees: Dict[int, Employee] = {}
        self._next_id = 1

    def add(self, employee: Employee) -> None:
        if employee.id == 0:
            self._employees[self._next_id] = employee
            self._next_id += 1
        else:
            self._employees[employee.id] = employee

    def get_all(self) -> List[Employee]:
        return list(self._employees.values())


class Company:
    """Компания (рефакторинный)"""

    def __init__(self, name: str, repository: Optional[IEmployeeRepository] = None):
        self.__name = name
        self.__repository = repository or InMemoryEmployeeRepository()

    def hire_employee(self, employee: Employee) -> None:
        self.__repository.add(employee)

    def get_all_employees(self) -> List[Employee]:
        return self.__repository.get_all()

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__repository.get_all())

    def get_employee_count(self) -> int:
        return len(self.__repository.get_all())


# ==================== ДЕМОНСТРАЦИЯ ====================

def main():
    print("=" * 70)
    print("ИТОГОВАЯ ДЕМОНСТРАЦИЯ РЕФАКТОРИННОГО КОДА")
    print("=" * 70)

    # Создание сотрудников
    dev = Developer(
        name="Иван Петров",
        department="DEV",
        base_salary=5000,
        seniority="senior",
        skills=["Python", "Docker"],
        employee_id=1
    )

    manager = Manager(
        name="Анна Сидорова",
        department="MGMT",
        base_salary=8000,
        bonus=2000,
        employee_id=2
    )

    salesperson = Salesperson(
        name="Петр Иванов",
        department="SALES",
        base_salary=3000,
        commission_rate=0.15,
        employee_id=3
    )

    # Работа с компанией
    company = Company("TechCorp", InMemoryEmployeeRepository())

    company.hire_employee(dev)
    company.hire_employee(manager)
    company.hire_employee(salesperson)

    salesperson.add_sales(5000)

    # Вывод информации
    print("\n📊 СОТРУДНИКИ:")
    print("-" * 70)
    for emp in company.get_all_employees():
        print(f"✓ {emp.get_info()}")

    print("\n💰 СТАТИСТИКА:")
    print("-" * 70)
    print(f"Всего сотрудников: {company.get_employee_count()}")
    print(f"Общая зарплата: ${company.calculate_total_salary():.2f}")
    print(f"Средняя зарплата: ${company.calculate_total_salary() / company.get_employee_count():.2f}")

    print("\n" + "=" * 70)
    print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)


if __name__ == "__main__":
    main()
