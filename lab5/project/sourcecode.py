import sqlite3
import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import functools


# ==================== БАЗОВЫЕ КЛАССЫ ИЗ ЛР №2 (с дополнениями) ====================
class AbstractEmployee(ABC):
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
        self.__observers = []
        self.__bonus_strategy = None

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def department(self):
        return self.__department

    @property
    def base_salary(self):
        return self.__base_salary

    @id.setter
    def id(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("ID должен быть положительным числом")
        self.__id = value

    @name.setter
    def name(self, value):
        value = str(value)
        if value == "":
            raise ValueError("Имя не может быть пустым")
        self.__name = value

    @department.setter
    def department(self, value):
        value = str(value)
        if value == "":
            raise ValueError("Название отдела не может быть пустым")
        self.__department = value

    @base_salary.setter
    def base_salary(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self.__base_salary = value

    def add_observer(self, observer):
        if observer not in self.__observers:
            self.__observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.__observers:
            observer.update(self, message)

    def set_bonus_strategy(self, strategy):
        self.__bonus_strategy = strategy

    def calculate_bonus(self):
        if self.__bonus_strategy:
            return self.__bonus_strategy.calculate_bonus(self)
        return 0

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
        }


class Employee(AbstractEmployee):
    def calculate_salary(self) -> float:
        return self.base_salary + self.calculate_bonus()

    def get_info(self) -> str:
        return f"Employee {self.id}: {self.name}, Dept: {self.department}, Salary: {self.calculate_salary():.2f}"


class Manager(Employee):
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        super().__init__(id, name, department, base_salary)
        self.__bonus = 0

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self.__bonus = value

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus + self.calculate_bonus()


class Developer(Employee):
    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        skills: List[str],
        seniority: str,
    ):
        super().__init__(id, name, department, base_salary)
        self.__skills = skills
        self.__seniority = seniority

    @property
    def skills(self):
        return self.__skills.copy()

    @property
    def seniority(self):
        return self.__seniority

    def calculate_salary(self) -> float:
        multiplier = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return (
            self.base_salary * multiplier.get(self.seniority, 1.0)
            + self.calculate_bonus()
        )


class Salesperson(Employee):
    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        commission_rate: float,
    ):
        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales = 0

    def update_sales(self, amount: float):
        if amount < 0:
            raise ValueError("Сумма продаж не может быть отрицательной")
        self.__sales += amount
        self.notify_observers(f"Sales updated: {amount}")

    def calculate_salary(self) -> float:
        return (
            self.base_salary
            + (self.__sales * self.__commission_rate)
            + self.calculate_bonus()
        )


class Department:
    def __init__(self, name: str, code: str):
        self.__name = name
        self.__code = code
        self.__employees = []

    @property
    def name(self):
        return self.__name

    @property
    def code(self):
        return self.__code

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название отдела не может быть пустым")
        self.__name = value

    def add_employee(self, employee):
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только объекты AbstractEmployee")
        self.__employees.append(employee)

    def get_employees(self):
        return self.__employees.copy()

    def __len__(self):
        return len(self.__employees)


class Project:
    def __init__(self, id: int, name: str, status: str = "planning"):
        self.__id = id
        self.__name = name
        self.__status = status
        self.__team = []

    def add_team_member(self, employee):
        if employee not in self.__team:
            self.__team.append(employee)

    def change_status(self, new_status):
        self.__status = new_status


class Company:
    def __init__(self, name: str):
        self.__name = name
        self.__departments = []
        self.__projects = []
        self.__employees = []
        self.__next_employee_id = 1

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название компании не может быть пустым")
        self.__name = value

    def _get_next_employee_id(self):
        id = self.__next_employee_id
        self.__next_employee_id += 1
        return id

    def hire_employee(self, employee: AbstractEmployee):
        if employee.id == 0:  # Если ID не задан
            employee.id = self._get_next_employee_id()
        elif employee.id >= self.__next_employee_id:
            self.__next_employee_id = employee.id + 1
        self.__employees.append(employee)

    def fire_employee(self, employee_id):
        self.__employees = [e for e in self.__employees if e.id != employee_id]

    def add_department(self, department):
        if not isinstance(department, Department):
            raise TypeError("Можно добавлять только объекты Department")
        self.__departments.append(department)

    def add_project(self, project):
        if not isinstance(project, Project):
            raise TypeError("Можно добавлять только объекты Project")
        self.__projects.append(project)

    def calculate_total_salary(self):
        return sum(e.calculate_salary() for e in self.__employees)

    def get_employee_count(self):
        return len(self.__employees)

    def get_all_employees(self):
        return self.__employees.copy()


# ==================== ЧАСТЬ 1: ПОРОЖДАЮЩИЕ ПАТТЕРНЫ ====================


# 1.1. Singleton для подключения к БД
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(":memory:", check_same_thread=False)
            self._init_db()
        return self._connection

    def _init_db(self):
        cursor = self._connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                base_salary REAL,
                type TEXT,
                data TEXT
            )
        """
        )
        self._connection.commit()

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None


# 1.2. Factory Method (рефакторинг существующей фабрики)
class EmployeeFactory(ABC):
    @abstractmethod
    def create_employee(
        self, id: int, name: str, department: str, base_salary: float, **kwargs
    ) -> AbstractEmployee:
        pass


class EmployeeConcreteFactory(EmployeeFactory):
    def create_employee(
        self, id: int, name: str, department: str, base_salary: float, **kwargs
    ) -> AbstractEmployee:
        return Employee(id, name, department, base_salary)


class ManagerConcreteFactory(EmployeeFactory):
    def create_employee(
        self, id: int, name: str, department: str, base_salary: float, **kwargs
    ) -> AbstractEmployee:
        return Manager(id, name, department, base_salary)


class DeveloperConcreteFactory(EmployeeFactory):
    def create_employee(
        self, id: int, name: str, department: str, base_salary: float, **kwargs
    ) -> AbstractEmployee:
        skills = kwargs.get("skills", [])
        seniority = kwargs.get("seniority", "junior")
        return Developer(id, name, department, base_salary, skills, seniority)


class SalespersonConcreteFactory(EmployeeFactory):
    def create_employee(
        self, id: int, name: str, department: str, base_salary: float, **kwargs
    ) -> AbstractEmployee:
        commission_rate = kwargs.get("commission_rate", 0.1)
        sp = Salesperson(id, name, department, base_salary, commission_rate)
        initial_sales = kwargs.get("initial_sales", 0)
        if initial_sales > 0:
            sp.update_sales(initial_sales)
        return sp


# 1.3. Abstract Factory для разных типов компаний
class CompanyFactory(ABC):
    @abstractmethod
    def create_company(self, name: str) -> Company:
        pass

    @abstractmethod
    def create_department(self, name: str, code: str) -> Department:
        pass

    @abstractmethod
    def create_employee(self, **kwargs) -> AbstractEmployee:
        pass


class TechCompanyFactory(CompanyFactory):
    def create_company(self, name: str) -> Company:
        company = Company(name)
        # Добавляем стандартные отделы для IT-компании
        company.add_department(self.create_department("Разработка", "DEV"))
        company.add_department(self.create_department("Тестирование", "QA"))
        company.add_department(self.create_department("DevOps", "OPS"))
        return company

    def create_department(self, name: str, code: str) -> Department:
        return Department(name, code)

    def create_employee(self, **kwargs) -> AbstractEmployee:
        emp_type = kwargs.get("type", "developer")
        if emp_type == "developer":
            factory = DeveloperConcreteFactory()
        elif emp_type == "manager":
            factory = ManagerConcreteFactory()
        else:
            factory = EmployeeConcreteFactory()

        return factory.create_employee(
            kwargs.get("id", 0),  # 0 означает "авто-ID"
            kwargs.get("name", "Unnamed"),
            kwargs.get("department", "DEV"),
            kwargs.get("base_salary", 0),
            **kwargs,
        )


class SalesCompanyFactory(CompanyFactory):
    def create_company(self, name: str) -> Company:
        company = Company(name)
        # Добавляем стандартные отделы для sales-компании
        company.add_department(self.create_department("Продажи", "SALES"))
        company.add_department(self.create_department("Маркетинг", "MARKETING"))
        company.add_department(self.create_department("Поддержка", "SUPPORT"))
        return company

    def create_department(self, name: str, code: str) -> Department:
        return Department(name, code)

    def create_employee(self, **kwargs) -> AbstractEmployee:
        emp_type = kwargs.get("type", "salesperson")
        if emp_type == "salesperson":
            factory = SalespersonConcreteFactory()
        elif emp_type == "manager":
            factory = ManagerConcreteFactory()
        else:
            factory = EmployeeConcreteFactory()

        return factory.create_employee(
            kwargs.get("id", 0),  # 0 означает "авто-ID"
            kwargs.get("name", "Unnamed"),
            kwargs.get("department", "SALES"),
            kwargs.get("base_salary", 0),
            **kwargs,
        )


# 1.4. Builder для пошагового создания сотрудников
class EmployeeBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._id = 0  # 0 означает "авто-ID"
        self._name = None
        self._department = None
        self._base_salary = None
        self._type = "employee"
        self._skills = []
        self._seniority = "junior"
        self._commission_rate = 0.1
        self._bonus = 0
        self._initial_sales = 0

    def set_id(self, id: int):
        self._id = id
        return self

    def set_name(self, name: str):
        self._name = name
        return self

    def set_department(self, department: str):
        self._department = department
        return self

    def set_base_salary(self, salary: float):
        self._base_salary = salary
        return self

    def set_type(self, emp_type: str):
        self._type = emp_type
        return self

    def set_skills(self, skills: List[str]):
        self._skills = skills
        return self

    def set_seniority(self, seniority: str):
        self._seniority = seniority
        return self

    def set_commission_rate(self, rate: float):
        self._commission_rate = rate
        return self

    def set_bonus(self, bonus: float):
        self._bonus = bonus
        return self

    def set_initial_sales(self, sales: float):
        self._initial_sales = sales
        return self

    def build(self) -> AbstractEmployee:
        # Проверка обязательных полей
        required_fields = [self._name, self._department, self._base_salary]
        if any(field is None for field in required_fields):
            missing = []
            if self._name is None:
                missing.append("name")
            if self._department is None:
                missing.append("department")
            if self._base_salary is None:
                missing.append("base_salary")
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        factories = {
            "employee": EmployeeConcreteFactory(),
            "manager": ManagerConcreteFactory(),
            "developer": DeveloperConcreteFactory(),
            "salesperson": SalespersonConcreteFactory(),
        }

        factory = factories.get(self._type, EmployeeConcreteFactory())
        employee = factory.create_employee(
            self._id,
            self._name,
            self._department,
            self._base_salary,
            skills=self._skills,
            seniority=self._seniority,
            commission_rate=self._commission_rate,
            initial_sales=self._initial_sales,
        )

        if self._type == "manager" and hasattr(employee, "bonus"):
            employee.bonus = self._bonus

        result = employee
        self.reset()
        return result


# ==================== ЧАСТЬ 2: СТРУКТУРНЫЕ ПАТТЕРНЫ ====================


# 2.1. Adapter для внешней системы расчета зарплат
class ExternalSalarySystem:
    """Внешняя система с другим интерфейсом"""

    def compute_compensation(self, employee_data: Dict) -> float:
        base = employee_data.get("base", 0)
        bonus = employee_data.get("bonus", 0)
        return base + bonus


class SalaryAdapter:
    """Адаптер для интеграции внешней системы"""

    def __init__(self, external_system: ExternalSalarySystem):
        self._external_system = external_system

    def calculate_salary(self, employee: AbstractEmployee) -> float:
        # Преобразуем наш объект в формат внешней системы
        employee_data = {
            "base": employee.base_salary,
            "bonus": employee.calculate_bonus(),
        }
        return self._external_system.compute_compensation(employee_data)


# 2.2. Decorator для добавления функциональности
class EmployeeDecorator(AbstractEmployee):
    """Базовый декоратор"""

    def __init__(self, employee: AbstractEmployee):
        self._employee = employee
        # Копируем все свойства базового сотрудника
        super().__init__(
            employee.id, employee.name, employee.department, employee.base_salary
        )

    def calculate_salary(self) -> float:
        return self._employee.calculate_salary()

    def get_info(self) -> str:
        return self._employee.get_info()

    # Делегируем остальные методы
    def add_observer(self, observer):
        self._employee.add_observer(observer)

    def remove_observer(self, observer):
        self._employee.remove_observer(observer)

    def notify_observers(self, message):
        self._employee.notify_observers(message)

    def set_bonus_strategy(self, strategy):
        self._employee.set_bonus_strategy(strategy)

    def calculate_bonus(self):
        return self._employee.calculate_bonus()


class BonusDecorator(EmployeeDecorator):
    """Декоратор для добавления бонуса"""

    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        super().__init__(employee)
        self._bonus_amount = bonus_amount

    def calculate_salary(self) -> float:
        return self._employee.calculate_salary() + self._bonus_amount

    def get_info(self) -> str:
        return f"{self._employee.get_info()} [+Bonus: {self._bonus_amount}]"


class TrainingDecorator(EmployeeDecorator):
    """Декоратор для добавления обучения"""

    def __init__(self, employee: AbstractEmployee, training: str):
        super().__init__(employee)
        self._training = training

    def get_info(self) -> str:
        return f"{self._employee.get_info()} | Training: {self._training}"


# 2.3. Facade для упрощенного управления компанией
class CompanyFacade:
    """Фасад для упрощения работы со сложной системой компании"""

    def __init__(self, company: Company):
        self._company = company
        self._notification_system = NotificationSystem()

    def hire(self, employee_data: Dict) -> bool:
        """Упрощенный найм сотрудника"""
        try:
            builder = EmployeeBuilder()

            # Устанавливаем обязательные поля
            if "name" not in employee_data:
                raise ValueError("Name is required")
            if "department" not in employee_data:
                raise ValueError("Department is required")
            if "base_salary" not in employee_data:
                raise ValueError("Base salary is required")

            builder.set_name(employee_data["name"])
            builder.set_department(employee_data["department"])
            builder.set_base_salary(employee_data["base_salary"])

            # Устанавливаем опциональные поля
            if "id" in employee_data:
                builder.set_id(employee_data["id"])
            if "type" in employee_data:
                builder.set_type(employee_data["type"])
            if "skills" in employee_data:
                builder.set_skills(employee_data["skills"])
            if "seniority" in employee_data:
                builder.set_seniority(employee_data["seniority"])
            if "commission_rate" in employee_data:
                builder.set_commission_rate(employee_data["commission_rate"])
            if "bonus" in employee_data:
                builder.set_bonus(employee_data["bonus"])

            employee = builder.build()

            self._company.hire_employee(employee)
            employee.add_observer(self._notification_system)
            self._notification_system.notify(f"Hired: {employee.name}")
            return True
        except Exception as e:
            print(f"Hire failed: {e}")
            return False

    def fire(self, employee_id: int) -> bool:
        """Упрощенное увольнение сотрудника"""
        employee = next(
            (e for e in self._company.get_all_employees() if e.id == employee_id), None
        )
        if employee:
            self._company.fire_employee(employee_id)
            self._notification_system.notify(f"Fired: {employee.name}")
            return True
        return False

    def calculate_payroll(self) -> Dict:
        """Расчет всех зарплат"""
        employees = self._company.get_all_employees()
        total = sum(e.calculate_salary() for e in employees)
        count = len(employees)
        return {
            "total": total,
            "count": count,
            "average": total / count if count > 0 else 0,
        }


# ==================== ЧАСТЬ 3: ПОВЕДЕНЧЕСКИЕ ПАТТЕРНЫ ====================


# 3.1. Observer для системы уведомлений
class Observer(ABC):
    @abstractmethod
    def update(self, subject, message: str):
        pass


class NotificationSystem(Observer):
    """Система уведомлений"""

    def __init__(self):
        self._notifications = []

    def update(self, subject, message: str):
        notification = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {subject.name if hasattr(subject, 'name') else 'System'}: {message}"
        self._notifications.append(notification)
        print(f"NOTIFICATION: {notification}")

    def notify(self, message: str):
        # Для прямых уведомлений (без субъекта)
        self.update(None, message)

    def get_notifications(self):
        return self._notifications.copy()


# 3.2. Strategy для различных стратегий расчета бонусов
class BonusStrategy(ABC):
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        pass


class PerformanceBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        # Простая логика: 10% от базовой зарплаты
        return employee.base_salary * 0.1


class SeniorityBonusStrategy(BonusStrategy):
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        if isinstance(employee, Developer):
            multipliers = {"junior": 0.05, "middle": 0.1, "senior": 0.2}
            return employee.base_salary * multipliers.get(employee.seniority, 0)
        return employee.base_salary * 0.05


class ProjectBonusStrategy(BonusStrategy):
    def __init__(self, projects_completed: int = 0):
        self._projects_completed = projects_completed

    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        return self._projects_completed * 500  # 500 за проект


# 3.3. Command для операций с сотрудниками
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class HireEmployeeCommand(Command):
    def __init__(self, company: Company, employee: AbstractEmployee):
        self._company = company
        self._employee = employee
        self._executed = False

    def execute(self):
        self._company.hire_employee(self._employee)
        self._executed = True
        print(f"Executed: Hire {self._employee.name}")

    def undo(self):
        if self._executed:
            self._company.fire_employee(self._employee.id)
            print(f"Undone: Hire {self._employee.name}")


class FireEmployeeCommand(Command):
    def __init__(self, company: Company, employee_id: int):
        self._company = company
        self._employee_id = employee_id
        self._employee = None
        self._executed = False

    def execute(self):
        # Находим сотрудника перед удалением для возможности отмены
        employees = self._company.get_all_employees()
        for emp in employees:
            if emp.id == self._employee_id:
                self._employee = emp
                break

        self._company.fire_employee(self._employee_id)
        self._executed = True
        print(f"Executed: Fire employee {self._employee_id}")

    def undo(self):
        if self._executed and self._employee:
            self._company.hire_employee(self._employee)
            print(f"Undone: Fire employee {self._employee_id}")


class UpdateSalaryCommand(Command):
    def __init__(self, employee: AbstractEmployee, new_salary: float):
        self._employee = employee
        self._new_salary = new_salary
        self._old_salary = employee.base_salary
        self._executed = False

    def execute(self):
        self._employee.base_salary = self._new_salary
        self._executed = True
        print(
            f"Executed: Update salary for {self._employee.name} to {self._new_salary}"
        )

    def undo(self):
        if self._executed:
            self._employee.base_salary = self._old_salary
            print(f"Undone: Salary update for {self._employee.name}")


class CommandInvoker:
    """Invoker для управления командами"""

    def __init__(self):
        self._history = []

    def execute_command(self, command: Command):
        command.execute()
        self._history.append(command)

    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()


# ==================== ЧАСТЬ 4: КОМБИНИРОВАННЫЕ ПАТТЕРНЫ ====================


# 4.1. Repository Pattern для работы с данными
class EmployeeRepository:
    """Репозиторий для работы с сотрудниками"""

    def __init__(self):
        self._employees = []
        self._next_id = 1

    def add(self, employee: AbstractEmployee):
        if employee.id == 0:
            employee.id = self._next_id
            self._next_id += 1
        self._employees.append(employee)

    def get(self, employee_id: int) -> Optional[AbstractEmployee]:
        for emp in self._employees:
            if emp.id == employee_id:
                return emp
        return None

    def get_all(self) -> List[AbstractEmployee]:
        return self._employees.copy()

    def update(self, employee: AbstractEmployee):
        for i, emp in enumerate(self._employees):
            if emp.id == employee.id:
                self._employees[i] = employee
                return True
        return False

    def delete(self, employee_id: int) -> bool:
        for i, emp in enumerate(self._employees):
            if emp.id == employee_id:
                del self._employees[i]
                return True
        return False

    def find_by_specification(self, specification) -> List[AbstractEmployee]:
        return [emp for emp in self._employees if specification.is_satisfied_by(emp)]


class DepartmentRepository:
    """Репозиторий для работы с отделами"""

    def __init__(self):
        self._departments = []

    def add(self, department: Department):
        self._departments.append(department)

    def get_all(self) -> List[Department]:
        return self._departments.copy()


# 4.2. Unit of Work для управления транзакциями
class UnitOfWork:
    """Unit of Work для управления транзакциями"""

    def __init__(self):
        self._new_objects = []
        self._dirty_objects = []
        self._removed_objects = []

    def register_new(self, obj):
        self._new_objects.append(obj)

    def register_dirty(self, obj):
        if obj not in self._dirty_objects:
            self._dirty_objects.append(obj)

    def register_removed(self, obj):
        self._removed_objects.append(obj)

    def commit(self):
        # Здесь обычно происходит сохранение в БД
        print(
            f"Committing: {len(self._new_objects)} new, {len(self._dirty_objects)} dirty, {len(self._removed_objects)} removed"
        )

        # В реальной системе здесь был бы код для сохранения
        self._new_objects.clear()
        self._dirty_objects.clear()
        self._removed_objects.clear()

    def rollback(self):
        print("Rolling back all changes")
        self._new_objects.clear()
        self._dirty_objects.clear()
        self._removed_objects.clear()


# 4.3. Specification Pattern для фильтрации
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)


class SalarySpecification(Specification):
    def __init__(self, min_salary: float):
        self._min_salary = min_salary

    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        return employee.calculate_salary() >= self._min_salary


class DepartmentSpecification(Specification):
    def __init__(self, department: str):
        self._department = department

    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        return employee.department == self._department


class SkillSpecification(Specification):
    def __init__(self, required_skill: str):
        self._required_skill = required_skill

    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        if isinstance(employee, Developer):
            return self._required_skill in employee.skills
        return False


class AndSpecification(Specification):
    def __init__(self, spec1: Specification, spec2: Specification):
        self._spec1 = spec1
        self._spec2 = spec2

    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        return self._spec1.is_satisfied_by(employee) and self._spec2.is_satisfied_by(
            employee
        )


class OrSpecification(Specification):
    def __init__(self, spec1: Specification, spec2: Specification):
        self._spec1 = spec1
        self._spec2 = spec2

    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        return self._spec1.is_satisfied_by(employee) or self._spec2.is_satisfied_by(
            employee
        )


# ==================== ЧАСТЬ 5: ТЕСТИРОВАНИЕ И ДЕМОНСТРАЦИЯ ====================


def demonstrate_patterns():
    print("=" * 70)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНОВ ПРОЕКТИРОВАНИЯ")
    print("=" * 70)

    # 1. Singleton
    print("\n1. SINGLETON (DatabaseConnection):")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   Один и тот же экземпляр: {id(db1) == id(db2)}")

    # 2. Abstract Factory
    print("\n2. ABSTRACT FACTORY (Создание разных компаний):")

    tech_factory = TechCompanyFactory()
    tech_company = tech_factory.create_company("TechCorp")
    print(f"   Создана IT компания: {tech_company.name}")
    print(f"   Отделы в IT компании: {len(tech_company._Company__departments)}")

    sales_factory = SalesCompanyFactory()
    sales_company = sales_factory.create_company("SalesCorp")
    print(f"   Создана Sales компания: {sales_company.name}")
    print(f"   Отделы в Sales компании: {len(sales_company._Company__departments)}")

    # 3. Builder
    print("\n3. BUILDER (Пошаговое создание сотрудников):")

    developer = (
        EmployeeBuilder()
        .set_id(101)
        .set_name("Иван Петров")
        .set_department("DEV")
        .set_base_salary(5000)
        .set_type("developer")
        .set_skills(["Python", "Java", "Docker"])
        .set_seniority("senior")
        .build()
    )

    salesperson = (
        EmployeeBuilder()
        .set_id(102)
        .set_name("Анна Сидорова")
        .set_department("SALES")
        .set_base_salary(3000)
        .set_type("salesperson")
        .set_commission_rate(0.15)
        .set_initial_sales(10000)
        .build()
    )

    print(f"   Создан разработчик: {developer.get_info()}")
    print(f"   Создан продавец: {salesperson.get_info()}")

    # 4. Factory Method
    print("\n4. FACTORY METHOD (Создание через фабрики):")

    emp_factory = EmployeeConcreteFactory()
    dev_factory = DeveloperConcreteFactory()

    employee = emp_factory.create_employee(201, "Петр Иванов", "HR", 2500)
    developer2 = dev_factory.create_employee(
        202, "Мария Козлова", "DEV", 4500, skills=["Python", "SQL"], seniority="middle"
    )

    print(f"   Создан через EmployeeFactory: {employee.get_info()}")
    print(f"   Создан через DeveloperFactory: {developer2.get_info()}")

    # 5. Adapter
    print("\n5. ADAPTER (Интеграция внешней системы):")

    external_system = ExternalSalarySystem()
    adapter = SalaryAdapter(external_system)

    salary_via_adapter = adapter.calculate_salary(developer)
    salary_normal = developer.calculate_salary()

    print(f"   Зарплата через адаптер: {salary_via_adapter}")
    print(f"   Зарплата обычным способом: {salary_normal}")

    # 6. Decorator
    print("\n6. DECORATOR (Добавление функциональности):")

    decorated_developer = BonusDecorator(developer, 1000)
    double_decorated = TrainingDecorator(decorated_developer, "Cloud Computing")

    print(f"   Оригинал: {developer.get_info()}")
    print(f"   С бонусом: {decorated_developer.get_info()}")
    print(f"   С бонусом и обучением: {double_decorated.get_info()}")

    # 7. Facade
    print("\n7. FACADE (Упрощенный интерфейс):")

    facade = CompanyFacade(tech_company)
    result = facade.hire(
        {
            "name": "Алексей Смирнов",
            "department": "DEV",
            "base_salary": 4000,
            "type": "developer",
            "skills": ["Python"],
            "seniority": "middle",
        }
    )

    if result:
        payroll = facade.calculate_payroll()
        print(f"   Расчет зарплат через фасад: {payroll}")
    else:
        print("   Ошибка при найме через фасад")

    # 8. Observer
    print("\n8. OBSERVER (Система уведомлений):")

    notification_system = NotificationSystem()
    developer.add_observer(notification_system)

    # Изменяем зарплату - должно прийти уведомление
    old_salary = developer.base_salary
    developer.base_salary = 5500
    developer.notify_observers(
        f"Salary changed from {old_salary} to {developer.base_salary}"
    )

    print(f"   Уведомлений отправлено: {len(notification_system.get_notifications())}")

    # 9. Strategy
    print("\n9. STRATEGY (Разные стратегии бонусов):")

    developer.set_bonus_strategy(PerformanceBonusStrategy())
    print(f"   Бонус по производительности: {developer.calculate_bonus():.2f}")

    developer.set_bonus_strategy(SeniorityBonusStrategy())
    print(f"   Бонус за опыт: {developer.calculate_bonus():.2f}")

    developer.set_bonus_strategy(ProjectBonusStrategy(projects_completed=3))
    print(f"   Бонус за проекты: {developer.calculate_bonus():.2f}")

    # 10. Command
    print("\n10. COMMAND (Операции с отменой):")

    invoker = CommandInvoker()
    hire_cmd = HireEmployeeCommand(tech_company, developer2)
    invoker.execute_command(hire_cmd)

    # Отмена найма
    invoker.undo_last()

    # 11. Repository
    print("\n11. REPOSITORY (Работа с данными):")

    employee_repo = EmployeeRepository()
    employee_repo.add(developer)
    employee_repo.add(salesperson)

    print(f"   Сотрудников в репозитории: {len(employee_repo.get_all())}")
    found = employee_repo.get(101)
    print(f"   Сотрудник с ID 101: {found.name if found else 'Не найден'}")

    # 12. Unit of Work
    print("\n12. UNIT OF WORK (Транзакции):")

    uow = UnitOfWork()
    uow.register_new(developer)
    uow.register_dirty(salesperson)

    print("   Перед коммитом: изменения зарегистрированы")
    uow.commit()
    print("   После коммита: изменения применены")

    # 13. Specification
    print("\n13. SPECIFICATION (Фильтрация сотрудников):")

    high_salary_spec = SalarySpecification(min_salary=4000)
    dev_spec = DepartmentSpecification("DEV")
    python_spec = SkillSpecification("Python")

    combined_spec = high_salary_spec & dev_spec & python_spec

    matching_employees = employee_repo.find_by_specification(combined_spec)
    print(
        f"   Сотрудники с зарплатой > 4000 в отделе DEV со знанием Python: {len(matching_employees)}"
    )

    for emp in matching_employees:
        print(f"     - {emp.name}: {emp.calculate_salary():.2f}")

    # 14. Итоговая демонстрация взаимодействия
    print("\n" + "=" * 70)
    print("ИТОГОВАЯ ДЕМОНСТРАЦИЯ ВЗАИМОДЕЙСТВИЯ ПАТТЕРНОВ")
    print("=" * 70)

    # Создаем компанию через фабрику
    final_company = tech_factory.create_company("FinalCorp")
    final_facade = CompanyFacade(final_company)

    # Создаем сотрудников через фасад (который использует Builder внутри)
    employees_data = [
        {
            "name": "Дмитрий Волков",
            "department": "DEV",
            "base_salary": 6000,
            "type": "developer",
            "skills": ["Python", "JavaScript", "AWS"],
            "seniority": "senior",
        },
        {
            "name": "Ольга Новикова",
            "department": "DEV",
            "base_salary": 3500,
            "type": "developer",
            "skills": ["Java", "Spring"],
            "seniority": "middle",
        },
        {
            "name": "Сергей Ли",
            "department": "MGMT",
            "base_salary": 8000,
            "type": "manager",
            "bonus": 2000,
        },
    ]

    # Нанимаем через Facade (которая использует Command и Observer внутри)
    for emp_data in employees_data:
        final_facade.hire(emp_data)

    # Применяем Strategy для бонусов
    for emp in final_company.get_all_employees():
        if isinstance(emp, Developer):
            emp.set_bonus_strategy(SeniorityBonusStrategy())
        elif isinstance(emp, Manager):
            emp.set_bonus_strategy(PerformanceBonusStrategy())

    # Используем Decorator для особых случаев
    if final_company.get_all_employees():
        special_employee = final_company.get_all_employees()[0]
        decorated_emp = TrainingDecorator(
            BonusDecorator(special_employee, 1500), "Advanced Python"
        )
        print(f"   Декорированный сотрудник: {decorated_emp.get_info()}")

    # Сохраняем в репозиторий
    final_repo = EmployeeRepository()
    for emp in final_company.get_all_employees():
        final_repo.add(emp)

    # Ищем через Specification
    senior_devs = final_repo.find_by_specification(
        DepartmentSpecification("DEV") & SalarySpecification(4000)
    )

    print(f"\nФинальная статистика:")
    print(f"- Всего сотрудников: {final_company.get_employee_count()}")
    print(f"- Разработчиков с зарплатой > 4000: {len(senior_devs)}")
    print(
        f"- Общие затраты на зарплаты: {final_facade.calculate_payroll()['total']:.2f}"
    )

    # Демонстрация отмены через Command
    print(f"\nДемонстрация отмены операции:")
    command_invoker = CommandInvoker()

    # Создаем тестового сотрудника через Builder
    test_employee = (
        EmployeeBuilder()
        .set_name("Тестовый Сотрудник")
        .set_department("TEST")
        .set_base_salary(1000)
        .build()
    )

    hire_cmd = HireEmployeeCommand(final_company, test_employee)
    command_invoker.execute_command(hire_cmd)
    print(f"   После найма: {final_company.get_employee_count()} сотрудников")

    command_invoker.undo_last()
    print(f"   После отмены: {final_company.get_employee_count()} сотрудников")

    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_patterns()
