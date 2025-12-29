from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import functools


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

    # Магические методы для перегрузки операторов
    def __eq__(self, other) -> bool:
        """Сравнение сотрудников по ID"""
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.id == other.id

    def __lt__(self, other) -> bool:
        """Сравнение сотрудников по итоговой зарплате"""
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()

    def __add__(self, other) -> float:
        """Сложение двух сотрудников возвращает сумму их зарплат"""
        if not isinstance(other, AbstractEmployee):
            return NotImplemented
        return self.calculate_salary() + other.calculate_salary()

    def __radd__(self, other) -> float:
        """Поддержка суммирования в списке через sum()"""
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
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AbstractEmployee":
        """Десериализация сотрудника из словаря"""
        raise NotImplementedError("Должен быть реализован в подклассах")


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

    def to_dict(self) -> dict:
        """Сериализация сотрудника в словарь"""
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """Десериализация сотрудника из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
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

    def to_dict(self) -> dict:
        """Сериализация менеджера в словарь"""
        data = super().to_dict()
        data["bonus"] = self.bonus
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Manager":
        """Десериализация менеджера из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            bonus=data["bonus"],
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

    def __iter__(self):
        """Итерация по стеку технологий разработчика"""
        return iter(self.__tech_stack)

    def to_dict(self) -> dict:
        """Сериализация разработчика в словарь"""
        data = super().to_dict()
        data["tech_stack"] = self.tech_stack
        data["seniority_level"] = self.seniority_level
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Developer":
        """Десериализация разработчика из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            tech_stack=data["tech_stack"],
            seniority_level=data["seniority_level"],
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

    def to_dict(self) -> dict:
        """Сериализация продавца в словарь"""
        data = super().to_dict()
        data["commission_rate"] = self.commission_rate
        data["sales_volume"] = self.sales_volume
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Salesperson":
        """Десериализация продавца из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            commission_rate=data["commission_rate"],
            sales_volume=data["sales_volume"],
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

    @staticmethod
    def from_dict(data: dict) -> AbstractEmployee:
        """
        Создание сотрудника из словаря

        Args:
            data: Словарь с данными сотрудника

        Returns:
            AbstractEmployee: Объект сотрудника
        """
        employee_type = data.get("type")
        if employee_type == "Employee":
            return Employee.from_dict(data)
        elif employee_type == "Manager":
            return Manager.from_dict(data)
        elif employee_type == "Developer":
            return Developer.from_dict(data)
        elif employee_type == "Salesperson":
            return Salesperson.from_dict(data)
        else:
            raise ValueError(f"Неизвестный тип сотрудника в словаре: {employee_type}")


class Department:
    """Класс отдела компании"""

    def __init__(self, name: str):
        """
        Инициализация отдела

        Args:
            name: Название отдела
        """
        self.__name = name
        self.__employees = []

    @property
    def name(self):
        """Название отдела"""
        return self.__name

    @name.setter
    def name(self, value):
        value = str(value)
        if value == "":
            raise ValueError("Название отдела не может быть пустым")
        self.__name = value

    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавление сотрудника в отдел

        Args:
            employee: Сотрудник для добавления
        """
        if not isinstance(employee, AbstractEmployee):
            raise TypeError("Можно добавлять только объекты AbstractEmployee")
        self.__employees.append(employee)

    def remove_employee(self, employee_id: int) -> None:
        """
        Удаление сотрудника по ID

        Args:
            employee_id: ID сотрудника для удаления
        """
        for i, emp in enumerate(self.__employees):
            if emp.id == employee_id:
                del self.__employees[i]
                return
        raise ValueError(f"Сотрудник с ID {employee_id} не найден в отделе")

    def get_employees(self) -> List[AbstractEmployee]:
        """
        Получение списка всех сотрудников отдела

        Returns:
            List[AbstractEmployee]: Список сотрудников отдела
        """
        return self.__employees.copy()

    def calculate_total_salary(self) -> float:
        """
        Вычисление общей зарплаты всех сотрудников отдела

        Returns:
            float: Общая зарплата отдела
        """
        return sum(emp.calculate_salary() for emp in self.__employees)

    def get_employee_count(self) -> Dict[str, int]:
        """
        Получение количества сотрудников каждого типа

        Returns:
            Dict[str, int]: Словарь с количеством сотрудников по типам
        """
        count = {}
        for emp in self.__employees:
            emp_type = emp.__class__.__name__
            count[emp_type] = count.get(emp_type, 0) + 1
        return count

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Поиск сотрудника по ID

        Args:
            employee_id: ID сотрудника для поиска

        Returns:
            Optional[AbstractEmployee]: Найденный сотрудник или None
        """
        for emp in self.__employees:
            if emp.id == employee_id:
                return emp
        return None

    # Магические методы
    def __len__(self) -> int:
        """Возвращает количество сотрудников в отделе"""
        return len(self.__employees)

    def __getitem__(self, key) -> AbstractEmployee:
        """Доступ к сотруднику по индексу"""
        return self.__employees[key]

    def __contains__(self, employee: AbstractEmployee) -> bool:
        """Проверка принадлежности сотрудника отделу"""
        return employee in self.__employees

    def __iter__(self):
        """Итерация по сотрудникам отдела"""
        return iter(self.__employees)

    def to_dict(self) -> dict:
        """Сериализация отдела в словарь"""
        return {
            "name": self.name,
            "employees": [emp.to_dict() for emp in self.__employees],
        }

    def save_to_file(self, filename: str) -> None:
        """
        Сохранение отдела в JSON файл

        Args:
            filename: Имя файла для сохранения
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, filename: str) -> "Department":
        """
        Загрузка отдела из JSON файла

        Args:
            filename: Имя файла для загрузки

        Returns:
            Department: Загруженный отдел
        """
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        department = cls(data["name"])
        for emp_data in data["employees"]:
            employee = EmployeeFactory.from_dict(emp_data)
            department.add_employee(employee)

        return department


# Функции-компараторы для сортировки
def compare_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнение сотрудников по имени"""
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    else:
        return 0


def compare_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Сравнение сотрудников по зарплате"""
    if emp1.calculate_salary() < emp2.calculate_salary():
        return -1
    elif emp1.calculate_salary() > emp2.calculate_salary():
        return 1
    else:
        return 0


def compare_by_department_and_name(
    emp1: AbstractEmployee, emp2: AbstractEmployee
) -> int:
    """Сравнение сотрудников по отделу и затем по имени"""
    if emp1.department < emp2.department:
        return -1
    elif emp1.department > emp2.department:
        return 1
    else:
        return compare_by_name(emp1, emp2)


def main():
    """Основная функция для демонстрации работы всех возможностей"""

    print("=" * 60)
    print("СОЗДАНИЕ ОТДЕЛА И ДОБАВЛЕНИЕ СОТРУДНИКОВ")
    print("=" * 60)

    # Создание отдела
    it_department = Department("IT Отдел")

    # Создание сотрудников разных типов
    employee1 = Employee(1, "Иван Иванов", "Бухгалтерия", 50000)
    manager1 = Manager(2, "Петр Петров", "Менеджмент", 70000, 20000)
    developer1 = Developer(
        3,
        "Алексей Сидоров",
        "Разработка",
        60000,
        ["Python", "Django", "PostgreSQL"],
        "middle",
    )
    salesperson1 = Salesperson(4, "Анна Козлова", "Продажи", 40000, 0.1, 150000)
    developer2 = Developer(
        5,
        "Елена Орлова",
        "Разработка",
        90000,
        ["Java", "Spring", "Hibernate"],
        "senior",
    )

    # Добавление сотрудников в отдел
    it_department.add_employee(employee1)
    it_department.add_employee(manager1)
    it_department.add_employee(developer1)
    it_department.add_employee(salesperson1)
    it_department.add_employee(developer2)

    print(f"Отдел: {it_department.name}")
    print(f"Количество сотрудников: {len(it_department)}")
    print(f"Общая зарплата отдела: {it_department.calculate_total_salary():.2f}")
    print(f"Количество по типам: {it_department.get_employee_count()}")

    print("\n" + "=" * 60)
    print("ПЕРЕГРУЗКА ОПЕРАТОРОВ")
    print("=" * 60)

    # Сравнение сотрудников
    print(f"Сравнение по ID (employee1 == manager1): {employee1 == manager1}")
    print(f"Сравнение по зарплате (employee1 < manager1): {employee1 < manager1}")

    # Суммирование зарплат
    print(f"Сумма зарплат employee1 и manager1: {employee1 + manager1:.2f}")

    # Суммирование списка сотрудников через sum()
    total_salary = sum(it_department.get_employees())
    print(f"Сумма зарплат всех сотрудников через sum(): {total_salary:.2f}")

    # Проверка вхождения сотрудника в отдел
    print(f"employee1 в отделе: {employee1 in it_department}")

    # Доступ к сотрудникам по индексу
    print(f"Первый сотрудник в отделе: {it_department[0].name}")

    print("\n" + "=" * 60)
    print("ИТЕРАЦИЯ")
    print("=" * 60)

    # Итерация по отделу
    print("Все сотрудники отдела:")
    for i, emp in enumerate(it_department, 1):
        print(f"{i}. {emp.name} - {emp.calculate_salary():.2f}")

    # Итерация по стеку технологий разработчика
    print(f"\nТехнологии разработчика {developer1.name}:")
    for skill in developer1:
        print(f"  - {skill}")

    print("\n" + "=" * 60)
    print("СЕРИАЛИЗАЦИЯ И ДЕСЕРИАЛИЗАЦИЯ")
    print("=" * 60)

    # Сохранение отдела в файл
    filename = "department.json"
    it_department.save_to_file(filename)
    print(f"Отдел сохранен в файл: {filename}")

    # Загрузка отдела из файла
    loaded_department = Department.load_from_file(filename)
    print(f"Отдел загружен из файла: {loaded_department.name}")
    print(f"Количество сотрудников в загруженном отделе: {len(loaded_department)}")

    print("\n" + "=" * 60)
    print("СОРТИРОВКА СОТРУДНИКОВ")
    print("=" * 60)

    employees = it_department.get_employees()

    # Сортировка с использованием key=
    print("Сортировка по имени (key=):")
    sorted_by_name = sorted(employees, key=lambda emp: emp.name)
    for emp in sorted_by_name:
        print(f"  - {emp.name}")

    print("\nСортировка по зарплате (key=):")
    sorted_by_salary = sorted(employees, key=lambda emp: emp.calculate_salary())
    for emp in sorted_by_salary:
        print(f"  - {emp.name}: {emp.calculate_salary():.2f}")

    # Сортировка с использованием компараторов через functools.cmp_to_key
    print("\nСортировка по имени (компаратор):")
    sorted_by_name_cmp = sorted(employees, key=functools.cmp_to_key(compare_by_name))
    for emp in sorted_by_name_cmp:
        print(f"  - {emp.name}")

    print("\nСортировка по отделу и имени (компаратор):")
    sorted_by_dept_name = sorted(
        employees, key=functools.cmp_to_key(compare_by_department_and_name)
    )
    for emp in sorted_by_dept_name:
        print(f"  - {emp.department}: {emp.name}")

    print("\n" + "=" * 60)
    print("ПОИСК И ДРУГИЕ ОПЕРАЦИИ")
    print("=" * 60)

    # Поиск сотрудника по ID
    found_employee = it_department.find_employee_by_id(3)
    if found_employee:
        print(f"Найден сотрудник с ID 3: {found_employee.name}")

    # Удаление сотрудника
    it_department.remove_employee(1)
    print(
        f"После удаления сотрудника с ID 1, количество сотрудников: {len(it_department)}"
    )

    # Демонстрация полиморфизма
    print("\nИнформация о всех сотрудниках (полиморфизм):")
    for emp in it_department:
        print(f"  - {emp.get_info()}")


if __name__ == "__main__":
    main()
