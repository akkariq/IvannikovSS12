import json
import csv
from datetime import datetime, date
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import functools


# Кастомные исключения
class EmployeeNotFoundError(Exception):
    """Исключение при ненахождении сотрудника"""

    pass


class DepartmentNotFoundError(Exception):
    """Исключение при ненахождении отдела"""

    pass


class ProjectNotFoundError(Exception):
    """Исключение при ненахождении проекта"""

    pass


class InvalidStatusError(Exception):
    """Исключение при невалидном статусе"""

    pass


class DuplicateIdError(Exception):
    """Исключение при дублировании ID"""

    pass


class DepartmentNotEmptyError(Exception):
    """Исключение при попытке удалить непустой отдел"""

    pass


class EmployeeInProjectError(Exception):
    """Исключение при попытке удалить сотрудника, участвующего в проектах"""

    pass


class ProjectHasTeamError(Exception):
    """Исключение при попытке удалить проект с командой"""

    pass


# Базовые классы (из предыдущего кода с дополнениями)
class AbstractEmployee(ABC):
    """Абстрактный базовый класс для всех сотрудников"""

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
        self.__assigned_projects: List["Project"] = []

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

    @property
    def assigned_projects(self):
        return self.__assigned_projects.copy()

    @id.setter
    def id(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("ID должен быть положительным")
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

    def assign_to_project(self, project: "Project") -> None:
        """Назначить сотрудника на проект"""
        if project not in self.__assigned_projects:
            self.__assigned_projects.append(project)

    def remove_from_project(self, project: "Project") -> None:
        """Убрать сотрудника с проекта"""
        if project in self.__assigned_projects:
            self.__assigned_projects.remove(project)

    def get_project_count(self) -> int:
        """Получить количество проектов сотрудника"""
        return len(self.__assigned_projects)

    def is_available(self) -> bool:
        """Проверить доступность сотрудника для новых проектов"""
        return len(self.__assigned_projects) < 3  # Максимум 3 проекта

    @abstractmethod
    def calculate_salary(self) -> float:
        pass

    @abstractmethod
    def get_info(self) -> str:
        pass

    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other) -> bool:
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()

    def __add__(self, other) -> float:
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() + other.calculate_salary()

    def __radd__(self, other) -> float:
        if other == 0:
            return self.calculate_salary()
        else:
            return other + self.calculate_salary()

    def to_dict(self) -> dict:
        """Сериализация сотрудника в словарь"""
        return {
            "type": self.__class__.__name__,
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "base_salary": self.base_salary,
            "assigned_project_ids": [p.project_id for p in self.__assigned_projects],
        }

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "AbstractEmployee":
        raise NotImplementedError("Должен быть реализован в подклассах")


class Employee(AbstractEmployee):
    def calculate_salary(self) -> float:
        return self.base_salary

    def get_info(self) -> str:
        return (
            f"Сотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, итоговая зарплата: {self.calculate_salary()}, "
            f"проектов: {self.get_project_count()}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Employee":
        employee = cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
        )
        # Восстановление связей с проектами
        if company:
            for project_id in data.get("assigned_project_ids", []):
                project = company.find_project_by_id(project_id)
                if project:
                    employee.assign_to_project(project)
        return employee


class Manager(Employee):
    def __init__(
        self, id: int, name: str, department: str, base_salary: float, bonus: float
    ):
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus

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
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        return (
            f"Менеджер id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, бонус: {self.bonus}, "
            f"итоговая зарплата: {self.calculate_salary()}, проектов: {self.get_project_count()}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Manager":
        manager = cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            bonus=data["bonus"],
        )
        if company:
            for project_id in data.get("assigned_project_ids", []):
                project = company.find_project_by_id(project_id)
                if project:
                    manager.assign_to_project(project)
        return manager


class Developer(Employee):
    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        tech_stack: list[str],
        seniority_level: str,
    ):
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level

    @property
    def tech_stack(self):
        return self.__tech_stack.copy()

    @property
    def seniority_level(self):
        return self.__seniority_level

    @seniority_level.setter
    def seniority_level(self, value):
        allowed_levels = ["junior", "middle", "senior"]
        if value not in allowed_levels:
            raise ValueError(
                f'Уровень должен быть один из: {", ".join(allowed_levels)}'
            )
        self.__seniority_level = value

    def add_skill(self, new_skill: str) -> None:
        self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * multipliers[self.seniority_level]

    def get_info(self) -> str:
        return (
            f"Разработчик id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, уровень: {self.seniority_level}, "
            f'стек технологий: {", ".join(self.tech_stack)}, '
            f"итоговая зарплата: {self.calculate_salary()}, проектов: {self.get_project_count()}"
        )

    def __iter__(self):
        return iter(self.__tech_stack)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["tech_stack"] = self.tech_stack
        data["seniority_level"] = self.seniority_level
        return data

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Developer":
        developer = cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            tech_stack=data["tech_stack"],
            seniority_level=data["seniority_level"],
        )
        if company:
            for project_id in data.get("assigned_project_ids", []):
                project = company.find_project_by_id(project_id)
                if project:
                    developer.assign_to_project(project)
        return developer


class Salesperson(Employee):
    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        commission_rate: float,
        sales_volume: float,
    ):
        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self.__commission_rate

    @property
    def sales_volume(self):
        return self.__sales_volume

    @commission_rate.setter
    def commission_rate(self, value):
        value = float(value)
        if not 0 <= value <= 1:
            raise ValueError("Ставка комиссии должна быть между 0 и 1")
        self.__commission_rate = value

    @sales_volume.setter
    def sales_volume(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Объем продаж не может быть отрицательным")
        self.__sales_volume = value

    def update_sales(self, new_sales: float) -> None:
        if new_sales < 0:
            raise ValueError("Нельзя добавить отрицательный объем продаж")
        self.__sales_volume += new_sales

    def calculate_salary(self) -> float:
        return self.base_salary + (self.commission_rate * self.sales_volume)

    def get_info(self) -> str:
        return (
            f"Продавец id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, ставка комиссии: {self.commission_rate}, "
            f"объем продаж: {self.sales_volume}, итоговая зарплата: {self.calculate_salary()}, "
            f"проектов: {self.get_project_count()}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["commission_rate"] = self.commission_rate
        data["sales_volume"] = self.sales_volume
        return data

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Salesperson":
        salesperson = cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            commission_rate=data["commission_rate"],
            sales_volume=data["sales_volume"],
        )
        if company:
            for project_id in data.get("assigned_project_ids", []):
                project = company.find_project_by_id(project_id)
                if project:
                    salesperson.assign_to_project(project)
        return salesperson


class Department:
    def __init__(self, name: str, code: str):
        self.__name = name
        self.__code = code
        self.__employees: List[AbstractEmployee] = []

    @property
    def name(self):
        return self.__name

    @property
    def code(self):
        return self.__code

    @property
    def employee_count(self):
        return len(self.__employees)

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название отдела не может быть пустым")
        self.__name = value

    def add_employee(self, employee: AbstractEmployee) -> None:
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только объекты AbstractEmployee")
        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                if emp.get_project_count() > 0:
                    raise EmployeeInProjectError(
                        f"Сотрудник {emp.name} участвует в проектах и не может быть удален"
                    )
                del self.__employees[i]
                return
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе")

    def get_employees(self) -> List[AbstractEmployee]:
        return self.__employees.copy()

    def calculate_total_salary(self) -> float:
        return sum(emp.calculate_salary() for emp in self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        count = {}
        for emp in self.__employees:
            emp_type = emp.__class__.__name__
            count[emp_type] = count.get(emp_type, 0) + 1
        return count

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None

    def transfer_employee(self, employee_id: int, new_department: "Department") -> None:
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")

        self.__employees.remove(employee)
        new_department.add_employee(employee)
        employee.department = new_department.name

    def __len__(self) -> int:
        return len(self.__employees)

    def __getitem__(self, key) -> AbstractEmployee:
        return self.__employees[key]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        return employee in self.__employees

    def __iter__(self):
        return iter(self.__employees)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "code": self.code,
            "employees": [emp.to_dict() for emp in self.__employees],
        }

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Department":
        department = cls(data["name"], data["code"])
        for emp_data in data["employees"]:
            employee = EmployeeFactory.from_dict(emp_data, company)
            department.add_employee(employee)
        return department


class Project:
    """Класс проекта с композицией - команда проекта"""

    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]

    def __init__(
        self,
        project_id: int,
        name: str,
        description: str,
        deadline: str,
        status: str = "planning",
    ):
        self.__project_id = project_id
        self.__name = name
        self.__description = description
        self.__deadline = self._parse_date(deadline)
        self.__status = status
        self.__team: List[AbstractEmployee] = []  # Композиция

    @property
    def project_id(self):
        return self.__project_id

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def deadline(self):
        return self.__deadline

    @property
    def status(self):
        return self.__status

    @project_id.setter
    def project_id(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("ID проекта должен быть положительным")
        self.__project_id = value

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название проекта не может быть пустым")
        self.__name = value

    def _parse_date(self, date_str: str) -> datetime:
        """Парсинг даты из строки"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте YYYY-MM-DD")

    def add_team_member(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника в команду проекта"""
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только сотрудников")

        if employee in self.__team:
            raise DuplicateIdError(f"Сотрудник {employee.name} уже в команде проекта")

        if not employee.is_available():
            raise ValueError(f"Сотрудник {employee.name} перегружен проектами")

        self.__team.append(employee)
        employee.assign_to_project(self)

    def remove_team_member(self, employee_id: int) -> None:
        """Удалить сотрудника из команды проекта по ID"""
        for i, emp in enumerate(self.__team):
            if emp.id == employee_id:
                emp.remove_from_project(self)
                del self.__team[i]
                return
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в проекте")

    def get_team(self) -> List[AbstractEmployee]:
        """Получить список команды"""
        return self.__team.copy()

    def get_team_size(self) -> int:
        """Получить размер команды"""
        return len(self.__team)

    def calculate_total_salary(self) -> float:
        """Рассчитать суммарную зарплату команды"""
        return sum(emp.calculate_salary() for emp in self.__team)

    def get_project_info(self) -> str:
        """Получить полную информацию о проекте"""
        team_info = ", ".join([f"{emp.name} ({emp.department})" for emp in self.__team])
        return (
            f"Проект {self.project_id}: {self.name}\n"
            f"Описание: {self.description}\n"
            f"Дедлайн: {self.deadline.strftime('%Y-%m-%d')}\n"
            f"Статус: {self.status}\n"
            f"Команда ({self.get_team_size()} чел.): {team_info}\n"
            f"Бюджет на зарплаты: {self.calculate_total_salary():.2f}"
        )

    def change_status(self, new_status: str) -> None:
        """Изменить статус проекта"""
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(
                f'Неверный статус. Допустимые: {", ".join(self.VALID_STATUSES)}'
            )
        self.__status = new_status

    def is_overdue(self) -> bool:
        """Проверить, просрочен ли проект"""
        return datetime.now() > self.__deadline

    def days_until_deadline(self) -> int:
        """Количество дней до дедлайна"""
        return (self.__deadline - datetime.now()).days

    def to_dict(self) -> dict:
        """Сериализация проекта в словарь"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "team": [emp.id for emp in self.__team],  # Сохраняем только ID сотрудников
        }

    @classmethod
    def from_dict(cls, data: dict, company: "Company" = None) -> "Project":
        """Десериализация проекта из словаря"""
        project = cls(
            project_id=data["project_id"],
            name=data["name"],
            description=data["description"],
            deadline=data["deadline"],
            status=data["status"],
        )

        # Восстановление команды
        if company:
            for employee_id in data.get("team", []):
                employee = company.find_employee_by_id(employee_id)
                if employee:
                    try:
                        project.add_team_member(employee)
                    except (DuplicateIdError, ValueError):
                        # Игнорируем ошибки при загрузке (уже в команде или перегружен)
                        pass
        return project


class Company:
    """Класс компании с агрегацией - отделы и проекты"""

    def __init__(self, name: str):
        self.__name = name
        self.__departments: List[Department] = []  # Агрегация
        self.__projects: List[Project] = []  # Агрегация

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название компании не может быть пустым")
        self.__name = value

    # Управление отделами
    def add_department(self, department: Department) -> None:
        """Добавить отдел в компанию"""
        if not isinstance(department, Department):
            raise TypeError("Можно добавлять только объекты Department")

        # Проверка уникальности кода отдела
        for dept in self.__departments:
            if dept.code == department.code:
                raise DuplicateIdError(
                    f"Отдел с кодом {department.code} уже существует"
                )

        self.__departments.append(department)

    def remove_department(self, department_code: str) -> None:
        """Удалить отдел из компании"""
        for i, dept in enumerate(self.__departments):
            if dept.code == department_code:
                if dept.employee_count > 0:
                    raise DepartmentNotEmptyError(
                        f"Отдел {dept.name} не пуст и не может быть удален"
                    )
                del self.__departments[i]
                return
        raise DepartmentNotFoundError(f"Отдел с кодом {department_code} не найден")

    def get_departments(self) -> List[Department]:
        """Получить список всех отделов"""
        return self.__departments.copy()

    def find_department_by_code(self, code: str) -> Optional[Department]:
        """Найти отдел по коду"""
        for dept in self.__departments:
            if dept.code == code:
                return dept
        return None

    # Управление проектами
    def add_project(self, project: Project) -> None:
        """Добавить проект в компанию"""
        if not isinstance(project, Project):
            raise TypeError("Можно добавлять только объекты Project")

        # Проверка уникальности ID проекта
        for proj in self.__projects:
            if proj.project_id == project.project_id:
                raise DuplicateIdError(
                    f"Проект с ID {project.project_id} уже существует"
                )

        self.__projects.append(project)

    def remove_project(self, project_id: int) -> None:
        """Удалить проект из компании"""
        for i, proj in enumerate(self.__projects):
            if proj.project_id == project_id:
                if proj.get_team_size() > 0:
                    raise ProjectHasTeamError(
                        f"Проект {proj.name} имеет команду и не может быть удален"
                    )
                del self.__projects[i]
                return
        raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")

    def get_projects(self) -> List[Project]:
        """Получить список всех проектов"""
        return self.__projects.copy()

    def find_project_by_id(self, project_id: int) -> Optional[Project]:
        """Найти проект по ID"""
        for proj in self.__projects:
            if proj.project_id == project_id:
                return proj
        return None

    # Основные методы
    def get_all_employees(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников компании"""
        employees = []
        for dept in self.__departments:
            employees.extend(dept.get_employees())
        return employees

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Найти сотрудника по ID во всей компании"""
        for dept in self.__departments:
            employee = dept.find_employee_by_id(employee_id)
            if employee:
                return employee
        return None

    def calculate_total_monthly_cost(self) -> float:
        """Рассчитать общие месячные затраты на зарплаты"""
        return sum(emp.calculate_salary() for emp in self.get_all_employees())

    def get_projects_by_status(self, status: str) -> List[Project]:
        """Получить проекты по статусу"""
        if status not in Project.VALID_STATUSES:
            raise InvalidStatusError(
                f'Неверный статус. Допустимые: {", ".join(Project.VALID_STATUSES)}'
            )

        return [proj for proj in self.__projects if proj.status == status]

    # Бизнес-методы
    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        """Назначить сотрудника на проект"""
        employee = self.find_employee_by_id(employee_id)
        project = self.find_project_by_id(project_id)

        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        if not project:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")

        try:
            project.add_team_member(employee)
            return True
        except (DuplicateIdError, ValueError) as e:
            print(f"Ошибка назначения: {e}")
            return False

    def check_employee_availability(self, employee_id: int) -> bool:
        """Проверить доступность сотрудника для новых проектов"""
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")

        return employee.is_available()

    def get_department_stats(self) -> Dict[str, Any]:
        """Получить статистику по отделам"""
        stats = {}
        for dept in self.__departments:
            stats[dept.code] = {
                "name": dept.name,
                "employee_count": dept.employee_count,
                "total_salary": dept.calculate_total_salary(),
                "employee_types": dept.get_employee_count(),
                "avg_salary": dept.calculate_total_salary() / dept.employee_count
                if dept.employee_count > 0
                else 0,
            }
        return stats

    def get_project_budget_analysis(self) -> Dict[str, Any]:
        """Анализ бюджетов проектов"""
        analysis = {
            "total_projects": len(self.__projects),
            "by_status": {},
            "total_budget": 0,
            "avg_team_size": 0,
            "overdue_projects": 0,
        }

        total_team_size = 0
        for proj in self.__projects:
            # Статистика по статусам
            analysis["by_status"][proj.status] = (
                analysis["by_status"].get(proj.status, 0) + 1
            )

            # Бюджет
            analysis["total_budget"] += proj.calculate_total_salary()

            # Размер команды
            total_team_size += proj.get_team_size()

            # Просроченные проекты
            if proj.is_overdue() and proj.status in ["planning", "active"]:
                analysis["overdue_projects"] += 1

        analysis["avg_team_size"] = (
            total_team_size / len(self.__projects) if self.__projects else 0
        )
        return analysis

    def find_overloaded_employees(self) -> List[AbstractEmployee]:
        """Найти перегруженных сотрудников"""
        return [emp for emp in self.get_all_employees() if not emp.is_available()]

    # Сериализация
    def to_dict(self) -> dict:
        """Сериализация компании в словарь"""
        return {
            "name": self.name,
            "departments": [dept.to_dict() for dept in self.__departments],
            "projects": [proj.to_dict() for proj in self.__projects],
        }

    def save_to_json(self, filename: str) -> None:
        """Сохранить компанию в JSON файл"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_json(cls, filename: str) -> "Company":
        """Загрузить компанию из JSON файла"""
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        company = cls(data["name"])

        # Сначала создаем отделы и сотрудников
        for dept_data in data["departments"]:
            department = Department.from_dict(dept_data, company)
            company.add_department(department)

        # Затем создаем проекты и восстанавливаем связи
        for proj_data in data["projects"]:
            project = Project.from_dict(proj_data, company)
            company.add_project(project)

        return company

    # Экспорт отчетов
    def export_employees_csv(self, filename: str) -> None:
        """Экспорт сотрудников в CSV"""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Имя",
                    "Отдел",
                    "Должность",
                    "Базовая зарплата",
                    "Итоговая зарплата",
                    "Проектов",
                ]
            )

            for emp in self.get_all_employees():
                writer.writerow(
                    [
                        emp.id,
                        emp.name,
                        emp.department,
                        emp.__class__.__name__,
                        emp.base_salary,
                        emp.calculate_salary(),
                        emp.get_project_count(),
                    ]
                )

    def export_projects_csv(self, filename: str) -> None:
        """Экспорт проектов в CSV"""
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "ID",
                    "Название",
                    "Статус",
                    "Дедлайн",
                    "Размер команды",
                    "Бюджет зарплат",
                    "Дней до дедлайна",
                ]
            )

            for proj in self.__projects:
                writer.writerow(
                    [
                        proj.project_id,
                        proj.name,
                        proj.status,
                        proj.deadline.strftime("%Y-%m-%d"),
                        proj.get_team_size(),
                        proj.calculate_total_salary(),
                        proj.days_until_deadline(),
                    ]
                )

    def export_financial_report(self, filename: str) -> None:
        """Экспорт финансового отчета"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write("ФИНАНСОВЫЙ ОТЧЕТ КОМПАНИИ\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Компания: {self.name}\n")
            f.write(f"Общее количество сотрудников: {len(self.get_all_employees())}\n")
            f.write(
                f"Общие месячные затраты: {self.calculate_total_monthly_cost():.2f}\n\n"
            )

            f.write("СТАТИСТИКА ПО ОТДЕЛАМ:\n")
            stats = self.get_department_stats()
            for dept_code, dept_stats in stats.items():
                f.write(
                    f"- {dept_stats['name']} ({dept_code}): {dept_stats['employee_count']} сотрудников, "
                    f"зарплаты: {dept_stats['total_salary']:.2f}, средняя: {dept_stats['avg_salary']:.2f}\n"
                )

            f.write("\nАНАЛИЗ ПРОЕКТОВ:\n")
            analysis = self.get_project_budget_analysis()
            f.write(f"Всего проектов: {analysis['total_projects']}\n")
            f.write(f"Общий бюджет: {analysis['total_budget']:.2f}\n")
            f.write(f"Средний размер команды: {analysis['avg_team_size']:.1f}\n")
            f.write(f"Просроченных проектов: {analysis['overdue_projects']}\n")

            f.write("\nПЕРЕГРУЖЕННЫЕ СОТРУДНИКИ:\n")
            overloaded = self.find_overloaded_employees()
            if overloaded:
                for emp in overloaded:
                    f.write(
                        f"- {emp.name} ({emp.department}): {emp.get_project_count()} проектов\n"
                    )
            else:
                f.write("Нет перегруженных сотрудников\n")


class EmployeeFactory:
    """Фабрика для создания сотрудников"""

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        if emp_type == "employee":
            return Employee(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
            )
        elif emp_type == "manager":
            return Manager(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                bonus=kwargs.get("bonus"),
            )
        elif emp_type == "developer":
            return Developer(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                tech_stack=kwargs.get("tech_stack", []),
                seniority_level=kwargs.get("seniority_level"),
            )
        elif emp_type == "salesperson":
            return Salesperson(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                commission_rate=kwargs.get("commission_rate"),
                sales_volume=kwargs.get("sales_volume"),
            )
        else:
            raise ValueError(f"Неизвестный тип сотрудника: {emp_type}")

    @staticmethod
    def from_dict(data: dict, company: "Company" = None) -> AbstractEmployee:
        employee_type = data.get("type")
        if employee_type == "Employee":
            return Employee.from_dict(data, company)
        elif employee_type == "Manager":
            return Manager.from_dict(data, company)
        elif employee_type == "Developer":
            return Developer.from_dict(data, company)
        elif employee_type == "Salesperson":
            return Salesperson.from_dict(data, company)
        else:
            raise ValueError(f"Неизвестный тип сотрудника в словаре: {employee_type}")


# Функции-компараторы (из предыдущего кода)
def compare_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    else:
        return 0


def compare_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    if emp1.calculate_salary() < emp2.calculate_salary():
        return -1
    elif emp1.calculate_salary() > emp2.calculate_salary():
        return 1
    else:
        return 0


def compare_by_department_and_name(
    emp1: AbstractEmployee, emp2: AbstractEmployee
) -> int:
    if emp1.department < emp2.department:
        return -1
    elif emp1.department > emp2.department:
        return 1
    else:
        return compare_by_name(emp1, emp2)


def main():
    """Демонстрация работы всей системы"""

    print("=" * 70)
    print("СОЗДАНИЕ КОМПАНИИ И КОМПЛЕКСНОЙ СТРУКТУРЫ")
    print("=" * 70)

    try:
        # Создание компании
        company = Company("TechInnovations Inc.")

        # Создание отделов
        dev_department = Department("Разработка", "DEV")
        sales_department = Department("Продажи", "SALES")
        management_department = Department("Менеджмент", "MGMT")

        # Добавление отделов в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)
        company.add_department(management_department)

        # Создание сотрудников разных типов
        manager = Manager(1, "Алиса Иванова", "MGMT", 150000, 50000)
        senior_dev = Developer(
            2,
            "Борис Петров",
            "DEV",
            120000,
            ["Python", "Django", "PostgreSQL", "Docker"],
            "senior",
        )
        middle_dev = Developer(
            3,
            "Виктор Сидоров",
            "DEV",
            90000,
            ["JavaScript", "React", "Node.js"],
            "middle",
        )
        junior_dev = Developer(
            4, "Галина Козлова", "DEV", 60000, ["Python", "HTML", "CSS"], "junior"
        )
        salesperson = Salesperson(5, "Дмитрий Орлов", "SALES", 70000, 0.1, 500000)

        # Добавление сотрудников в отделы
        dev_department.add_employee(senior_dev)
        dev_department.add_employee(middle_dev)
        dev_department.add_employee(junior_dev)
        sales_department.add_employee(salesperson)
        management_department.add_employee(manager)

        # Создание проектов
        ai_project = Project(
            101,
            "AI Платформа",
            "Разработка платформы искусственного интеллекта для анализа данных",
            "2024-12-31",
            "active",
        )

        web_project = Project(
            102,
            "Веб-Портал",
            "Создание корпоративного веб-портала с системой управления контентом",
            "2024-09-30",
            "planning",
        )

        mobile_project = Project(
            103,
            "Мобильное Приложение",
            "Разработка мобильного приложения для iOS и Android",
            "2024-11-15",
            "active",
        )

        # Добавление проектов в компанию
        company.add_project(ai_project)
        company.add_project(web_project)
        company.add_project(mobile_project)

        # Формирование команд проектов
        print("\nФормирование команд проектов:")

        # AI проект
        ai_project.add_team_member(senior_dev)
        ai_project.add_team_member(middle_dev)
        print(
            f"- В проект '{ai_project.name}' добавлено {ai_project.get_team_size()} сотрудников"
        )

        # Веб проект
        web_project.add_team_member(middle_dev)
        web_project.add_team_member(junior_dev)
        print(
            f"- В проект '{web_project.name}' добавлено {web_project.get_team_size()} сотрудников"
        )

        # Мобильный проект
        mobile_project.add_team_member(senior_dev)
        mobile_project.add_team_member(junior_dev)
        print(
            f"- В проект '{mobile_project.name}' добавлено {mobile_project.get_team_size()} сотрудников"
        )

        print("\n" + "=" * 70)
        print("ИНФОРМАЦИЯ О ПРОЕКТАХ")
        print("=" * 70)

        for project in company.get_projects():
            print(f"\n{project.get_project_info()}")

        print("\n" + "=" * 70)
        print("СТАТИСТИКА КОМПАНИИ")
        print("=" * 70)

        print(f"Общее количество сотрудников: {len(company.get_all_employees())}")
        print(
            f"Месячные затраты на зарплаты: {company.calculate_total_monthly_cost():.2f}"
        )

        # Статистика по отделам
        print("\nСтатистика по отделам:")
        stats = company.get_department_stats()
        for dept_code, dept_stats in stats.items():
            print(
                f"- {dept_stats['name']}: {dept_stats['employee_count']} сотрудников, "
                f"зарплаты: {dept_stats['total_salary']:.2f}"
            )

        # Анализ проектов
        analysis = company.get_project_budget_analysis()
        print(f"\nАнализ проектов:")
        print(f"- Всего проектов: {analysis['total_projects']}")
        print(f"- Общий бюджет: {analysis['total_budget']:.2f}")
        print(f"- По статусам: {analysis['by_status']}")

        print("\n" + "=" * 70)
        print("ДЕМОНСТРАЦИЯ ВАЛИДАЦИИ И ОБРАБОТКИ ОШИБОК")
        print("=" * 70)

        # Попытка добавить дубликат ID
        try:
            duplicate_employee = Employee(1, "Дубликат", "TEST", 10000)
            dev_department.add_employee(duplicate_employee)
        except DuplicateIdError as e:
            print(f"✓ Защита от дубликатов: {e}")

        # Попытка невалидного изменения статуса
        try:
            ai_project.change_status("invalid_status")
        except InvalidStatusError as e:
            print(f"✓ Валидация статусов: {e}")

        # Попытка удалить отдел с сотрудниками
        try:
            company.remove_department("DEV")
        except DepartmentNotEmptyError as e:
            print(f"✓ Защита от удаления непустых отделов: {e}")

        # Попытка назначить перегруженного сотрудника
        try:
            test_project = Project(999, "Тестовый проект", "Тест", "2024-12-31")
            company.add_project(test_project)
            # senior_dev уже в 2 проектах
            test_project.add_team_member(senior_dev)
            test_project.add_team_member(senior_dev)  # Дубликат
            test_project.add_team_member(senior_dev)  # Перегрузка
        except (DuplicateIdError, ValueError) as e:
            print(f"✓ Контроль нагрузки сотрудников: {e}")

        print("\n" + "=" * 70)
        print("СЕРИАЛИЗАЦИЯ И ЭКСПОРТ")
        print("=" * 70)

        # Сохранение компании в JSON
        company.save_to_json("tech_innovations.json")
        print("✓ Компания сохранена в файл 'tech_innovations.json'")

        # Экспорт отчетов
        company.export_employees_csv("employees_report.csv")
        company.export_projects_csv("projects_report.csv")
        company.export_financial_report("financial_report.txt")

        print("✓ Отчеты экспортированы:")
        print("  - employees_report.csv (сотрудники)")
        print("  - projects_report.csv (проекты)")
        print("  - financial_report.txt (финансовый отчет)")

        # Демонстрация загрузки
        loaded_company = Company.load_from_json("tech_innovations.json")
        print(f"✓ Компания загружена из файла: {loaded_company.name}")
        print(f"  Отделов: {len(loaded_company.get_departments())}")
        print(f"  Проектов: {len(loaded_company.get_projects())}")
        print(f"  Сотрудников: {len(loaded_company.get_all_employees())}")

        print("\n" + "=" * 70)
        print("РАСШИРЕННЫЕ ВОЗМОЖНОСТИ")
        print("=" * 70)

        # Перенос сотрудника между отделами
        print("\nПеренос сотрудника между отделами:")
        print(f"До переноса: {middle_dev.name} в отделе {middle_dev.department}")
        dev_department.transfer_employee(3, sales_department)
        print(f"После переноса: {middle_dev.name} в отделе {middle_dev.department}")

        # Поиск перегруженных сотрудников
        overloaded = company.find_overloaded_employees()
        if overloaded:
            print(f"\nПерегруженные сотрудники ({len(overloaded)}):")
            for emp in overloaded:
                print(f"- {emp.name}: {emp.get_project_count()} проектов")
        else:
            print("\nНет перегруженных сотрудников")

        # Проверка доступности сотрудников
        print(f"\nПроверка доступности:")
        for emp in company.get_all_employees():
            status = "доступен" if emp.is_available() else "перегружен"
            print(f"- {emp.name}: {status} ({emp.get_project_count()}/3 проектов)")

        print("\n" + "=" * 70)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 70)

    except Exception as e:
        print(f"Ошибка при демонстрации: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
