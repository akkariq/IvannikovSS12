from abc import ABC, abstractmethod
from typing import Dict, Any


class AbstractEmployee(ABC):
    """Абстрактный базовый класс для всех сотрудников"""

    def __init__(self, id: int, name: str, department: str, base_salary: float):
        """
        Инициализация базовых атрибутов сотрудника

        Args:
            id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел, в котором работает сотрудник
            base_salary: Базовая зарплата сотрудника
        """
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    @property
    def id(self):
        """Уникальный идентификатор сотрудника"""
        return self.__id

    @property
    def name(self):
        """Имя сотрудника"""
        return self.__name

    @property
    def department(self):
        """Отдел, в котором работает сотрудник"""
        return self.__department

    @property
    def base_salary(self):
        """Базовая зарплата сотрудника"""
        return self.__base_salary

    @id.setter
    def id(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("Число должно быть положительным")
        self.__id = value

    @name.setter
    def name(self, value):
        value = str(value)
        if value == "":
            raise ValueError("Строка не должна быть пустой")
        self.__name = value

    @department.setter
    def department(self, value):
        value = str(value)
        if value == "":
            raise ValueError("Строка не должна быть пустой")
        self.__department = value

    @base_salary.setter
    def base_salary(self, value):
        value = int(value)
        if value < 1:
            raise ValueError("Число должно быть положительным")
        self.__base_salary = value

    @abstractmethod
    def calculate_salary(self) -> float:
        """Абстрактный метод для расчета итоговой заработной платы"""
        pass

    @abstractmethod
    def get_info(self) -> str:
        """Абстрактный метод для получения полной информации о сотруднике"""
        pass


class Employee(AbstractEmployee):
    """Класс обычного сотрудника"""

    def calculate_salary(self) -> float:
        """
        Расчет итоговой заработной платы

        Returns:
            float: Итоговая зарплата (равна базовой)
        """
        return self.base_salary

    def get_info(self) -> str:
        """
        Получение полной информации о сотруднике

        Returns:
            str: Строка с информацией о сотруднике
        """
        return (
            f"Сотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, итоговая зарплата: {self.calculate_salary()}"
        )


class Manager(Employee):
    """Класс менеджера с дополнительным бонусом"""

    def __init__(
        self, id: int, name: str, department: str, base_salary: float, bonus: float
    ):
        """
        Инициализация менеджера

        Args:
            id: Уникальный идентификатор
            name: Имя менеджера
            department: Отдел
            base_salary: Базовая зарплата
            bonus: Бонус менеджера
        """
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus

    @property
    def bonus(self):
        """Бонус менеджера"""
        return self.__bonus

    @bonus.setter
    def bonus(self, value):
        value = float(value)
        if value < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self.__bonus = value

    def calculate_salary(self) -> float:
        """
        Расчет итоговой заработной платы менеджера

        Returns:
            float: Итоговая зарплата (базовая + бонус)
        """
        return self.base_salary + self.bonus

    def get_info(self) -> str:
        """
        Получение полной информации о менеджере

        Returns:
            str: Строка с информацией о менеджере
        """
        return (
            f"Менеджер id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, бонус: {self.bonus}, "
            f"итоговая зарплата: {self.calculate_salary()}"
        )


class Developer(Employee):
    """Класс разработчика с учетом уровня и технологий"""

    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        tech_stack: list[str],
        seniority_level: str,
    ):
        """
        Инициализация разработчика

        Args:
            id: Уникальный идентификатор
            name: Имя разработчика
            department: Отдел
            base_salary: Базовая зарплата
            tech_stack: Стек технологий
            seniority_level: Уровень разработчика (junior, middle, senior)
        """
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level

    @property
    def tech_stack(self):
        """Стек технологий разработчика"""
        return self.__tech_stack.copy()

    @property
    def seniority_level(self):
        """Уровень разработчика"""
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
        """
        Добавление новой технологии в стек

        Args:
            new_skill: Новая технология
        """
        self.__tech_stack.append(new_skill)

    def calculate_salary(self) -> float:
        """
        Расчет итоговой заработной платы разработчика

        Returns:
            float: Итоговая зарплата (базовая * коэффициент уровня)
        """
        multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
        return self.base_salary * multipliers[self.seniority_level]

    def get_info(self) -> str:
        """
        Получение полной информации о разработчике

        Returns:
            str: Строка с информацией о разработчике
        """
        return (
            f"Разработчик id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, уровень: {self.seniority_level}, "
            f'стек технологий: {", ".join(self.tech_stack)}, '
            f"итоговая зарплата: {self.calculate_salary()}"
        )


class Salesperson(Employee):
    """Класс продавца с комиссионными от продаж"""

    def __init__(
        self,
        id: int,
        name: str,
        department: str,
        base_salary: float,
        commission_rate: float,
        sales_volume: float,
    ):
        """
        Инициализация продавца

        Args:
            id: Уникальный идентификатор
            name: Имя продавца
            department: Отдел
            base_salary: Базовая зарплата
            commission_rate: Процент комиссии
            sales_volume: Объем продаж
        """
        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume

    @property
    def commission_rate(self):
        """Процент комиссии продавца"""
        return self.__commission_rate

    @property
    def sales_volume(self):
        """Объем продаж"""
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
        """
        Добавление суммы к текущему объему продаж

        Args:
            new_sales: Новая сумма продаж
        """
        if new_sales < 0:
            raise ValueError("Нельзя добавить отрицательный объем продаж")
        self.__sales_volume += new_sales

    def calculate_salary(self) -> float:
        """
        Расчет итоговой заработной платы продавца

        Returns:
            float: Итоговая зарплата (базовая + комиссия от продаж)
        """
        return self.base_salary + (self.commission_rate * self.sales_volume)

    def get_info(self) -> str:
        """
        Получение полной информации о продавце

        Returns:
            str: Строка с информацией о продавце
        """
        return (
            f"Продавец id: {self.id}, имя: {self.name}, отдел: {self.department}, "
            f"базовая зарплата: {self.base_salary}, ставка комиссии: {self.commission_rate}, "
            f"объем продаж: {self.sales_volume}, итоговая зарплата: {self.calculate_salary()}"
        )


class EmployeeFactory:
    """Фабрика для создания объектов сотрудников"""

    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создание сотрудника определенного типа

        Args:
            emp_type: Тип сотрудника ("employee", "manager", "developer", "salesperson")
            **kwargs: Аргументы для создания сотрудника

        Returns:
            AbstractEmployee: Объект сотрудника

        Raises:
            ValueError: Если передан неизвестный тип сотрудника
        """
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


def main():
    """Основная функция для демонстрации работы классов"""

    print("=" * 60)
    print("СОЗДАНИЕ СОТРУДНИКОВ НАПРЯМУЮ ЧЕРЕЗ КОНСТРУКТОРЫ")
    print("=" * 60)

    # Создание экземпляров каждого типа сотрудника
    employee = Employee(1, "Иван Иванов", "Бухгалтерия", 50000)
    manager = Manager(2, "Петр Петров", "Менеджмент", 70000, 20000)
    developer = Developer(
        3, "Алексей Сидоров", "IT", 60000, ["Python", "Django", "PostgreSQL"], "middle"
    )
    salesperson = Salesperson(4, "Анна Козлова", "Продажи", 40000, 0.1, 150000)

    # Демонстрация работы сеттеров
    print("\nДемонстрация работы сеттеров:")
    employee.name = "Иван Николаев"
    manager.bonus = 25000
    developer.add_skill("Redis")
    salesperson.update_sales(50000)

    # Вывод информации о сотрудниках
    employees = [employee, manager, developer, salesperson]
    for emp in employees:
        print("\n" + "-" * 40)
        print(f"Зарплата: {emp.calculate_salary()}")
        print(emp.get_info())

    print("\n" + "=" * 60)
    print("СОЗДАНИЕ СОТРУДНИКОВ ЧЕРЕЗ ФАБРИКУ")
    print("=" * 60)

    # Создание сотрудников через фабрику
    factory_employee = EmployeeFactory.create_employee(
        "employee", id=5, name="Мария Смирнова", department="HR", base_salary=45000
    )

    factory_manager = EmployeeFactory.create_employee(
        "manager",
        id=6,
        name="Олег Кузнецов",
        department="Администрация",
        base_salary=80000,
        bonus=30000,
    )

    factory_developer = EmployeeFactory.create_employee(
        "developer",
        id=7,
        name="Елена Орлова",
        department="Разработка",
        base_salary=90000,
        tech_stack=["Java", "Spring", "Hibernate"],
        seniority_level="senior",
    )

    factory_salesperson = EmployeeFactory.create_employee(
        "salesperson",
        id=8,
        name="Дмитрий Волков",
        department="Маркетинг",
        base_salary=50000,
        commission_rate=0.15,
        sales_volume=200000,
    )

    # Демонстрация полиморфного поведения
    print("\nДемонстрация полиморфного поведения:")
    factory_employees = [
        factory_employee,
        factory_manager,
        factory_developer,
        factory_salesperson,
    ]

    for emp in factory_employees:
        print("\n" + "-" * 40)
        print(emp.get_info())

    # Создание смешанного списка сотрудников
    print("\n" + "=" * 60)
    print("СМЕШАННЫЙ СПИСОК СОТРУДНИКОВ (ПОЛИМОРФИЗМ)")
    print("=" * 60)

    all_employees = employees + factory_employees

    for i, emp in enumerate(all_employees, 1):
        print(f"\n{i}. {emp.get_info()}")


if __name__ == "__main__":
    main()
