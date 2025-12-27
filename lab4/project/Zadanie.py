# cook your dish here

from __future__ import annotations  # Добавь в самом начале файла
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import json
from functools import cmp_to_key
from typing import List, Optional, Dict
import csv

class EmployeeNotFoundError(Exception):
    """Исключение для случая, когда сотрудник не найден"""
    pass

class DepartmentNotFoundError(Exception):
    """Исключение для случая, когда отдел не найден"""
    pass

class ProjectNotFoundError(Exception):
    """Исключение для случая, когда проект не найден"""
    pass

class InvalidStatusError(Exception):
    """Исключение для недопустимого статуса"""
    pass

class DuplicateIdError(Exception):
    """Исключение для дублирования ID"""
    pass

class InvalidDateError(Exception):
    """Исключение для некорректной даты"""
    pass

class InvalidSalaryError(Exception):
    """Исключение для некорректной зарплаты"""
    pass

class Validator:
    """Класс для комплексной валидации данных"""
    
    @staticmethod
    def validate_employee_id(employee_id: int, existing_ids: set) -> None:
        """Валидация ID сотрудника"""
        if not isinstance(employee_id, int) or employee_id <= 0:
            raise ValueError("ID сотрудника должен быть положительным целым числом")
        
        if employee_id in existing_ids:
            raise DuplicateIdError(f"Сотрудник с ID {employee_id} уже существует")
    
    @staticmethod
    def validate_project_id(project_id: str, existing_ids: set) -> None:
        """Валидация ID проекта"""
        if not project_id or not isinstance(project_id, str):
            raise ValueError("ID проекта должен быть непустой строкой")
        
        if project_id in existing_ids:
            raise DuplicateIdError(f"Проект с ID {project_id} уже существует")
    
    @staticmethod
    def validate_salary(salary: float) -> None:
        """Валидация зарплаты"""
        if not isinstance(salary, (int, float)) or salary < 0:
            raise InvalidSalaryError(f"Некорректная зарплата: {salary}. Зарплата должна быть неотрицательным числом")
        
        if salary > 1_000_000:  # Максимальная зарплата 1 млн
            raise InvalidSalaryError(f"Зарплата {salary} превышает максимально допустимую")
    
    @staticmethod
    def validate_date(date_str: str) -> None:
        """Валидация даты"""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise InvalidDateError(f"Некорректный формат даты: {date_str}. Ожидается YYYY-MM-DD")
    
    @staticmethod
    def validate_status(status: str, valid_statuses: list) -> None:
        """Валидация статуса"""
        if status not in valid_statuses:
            raise InvalidStatusError(f"Недопустимый статус: '{status}'. Допустимые статусы: {valid_statuses}")


class AbstractEmployee(ABC):

    _existing_ids = set()

    def __init__(self, id, name, department, base_salary, skip_validation=False):


        if not skip_validation:
            Validator.validate_employee_id(id, self._existing_ids)
            self._existing_ids.add(id)
        
        # Валидация зарплаты
        Validator.validate_salary(base_salary)

        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if id > 0:
            self.__id = id
        else:
            print("Число отрицательное")

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name != "":
            self.__name = name
        else:
            print("пустая строка")

    @property
    def department(self):
        return self.__department

    @department.setter
    def department(self, department):
        self.__department = department

    @property
    def base_salary(self):
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, base_salary):
        self.__base_salary = base_salary

    def __str__(self):
        # print(self.id, self.name, self.department, self.base_salary)
        return f"Сотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата:{self.base_salary}"

    @abstractmethod
    def calculate_salary(self):
        pass

    def get_info(self):
        pass
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, AbstractEmployee):
            return False
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
        # Когда вызывается sum(), начальное значение 0 + self
        return other + self.calculate_salary()
        
    def to_dict(self) -> dict:
        """Возвращает словарь с данными сотрудника"""
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'base_salary': self.base_salary,
            'calculated_salary': self.calculate_salary(),
            'type': self.__class__.__name__
        }    
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AbstractEmployee':
        """Создает объект сотрудника из словаря"""
        employee_type = data.get('type', 'Employee')
        
        if employee_type == 'Manager':
            return Manager.from_dict(data)
        elif employee_type == 'Developer':
            return Developer.from_dict(data)
        elif employee_type == 'Salesperson':
            return Saleperson.from_dict(data)
        else:
            return Employee.from_dict(data)
    def __repr__(self):
        """Для красивого вывода в списках"""
        return f"{self.__class__.__name__}('{self.name}', dept='{self.department}', salary={self.calculate_salary()})"

class Employee(AbstractEmployee):
    def __init__(self, id, name, department, base_salary, skip_validation=False):
        super().__init__(id, name, department, base_salary, skip_validation)

    def calculate_salary(self):
        return self.base_salary

    def get_info(self):
        print(
            f"Сотрудник id: {self.id}, имя: {self.name}, отдел: {self.department}, базовая зарплата:{self.calculate_salary()}")
            
    def to_dict(self) -> dict:
        """Возвращает словарь с данными сотрудника"""
        data = super().to_dict()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Employee':
        """Создает объект Employee из словаря"""
        return cls(
            id=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            skip_validation=True  # Пропускаем валидацию при восстановлении
        )


class Manager(Employee):
    def __init__(self, id, name, department, base_salary, bonus, skip_validation=False):
        self.__bonus = bonus
        super().__init__(id, name, department, base_salary, skip_validation)

    @property
    def bonus(self):
        return self.__bonus

    @bonus.setter
    def bonus(self, bonus):
        self.__bonus = bonus

    def calculate_salary(self):
        return self.base_salary + self.__bonus

    def get_info(self):
        print(f"{self.__str__()}, бонус: {self.bonus} итоговая зарплата:{self.calculate_salary()}")
    
    def to_dict(self) -> dict:
        """Возвращает словарь с данными менеджера"""
        data = super().to_dict()
        data.update({
            'bonus': self.bonus
        })
        return data
     
    @classmethod
    def from_dict(cls, data: dict) -> 'Manager':
        """Создает объект Manager из словаря"""
        return cls(
            id=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            bonus=data['bonus'],
            skip_validation=True
        )  
        
    
class Developer(Employee):
    def __init__(self, id, name, department, base_salary, tech_stack, seniority_level, skip_validation=False):
        self.__tech_stack = tech_stack
        self.__seniority_level = seniority_level
        super().__init__(id, name, department, base_salary, skip_validation)

    def calculate_salary(self):
        if self.__seniority_level == "junior":
            return self.base_salary
        if self.__seniority_level == "middle":
            return self.base_salary * 1.5
        if self.__seniority_level == "senior":
            return self.base_salary * 2

    def add_skill(self, new_skill):
        self.__tech_stack.add(new_skill)

    def get_info(self):
        print(f"{self.__str__()}, список технологий:{self.__tech_stack}, уровень: {self.__seniority_level}, итоговая зарплата: {self.calculate_salary()}")
    
    def __iter__(self):
        return iter(self.__tech_stack)
    
    def to_dict(self) -> dict:
        """Возвращает словарь с данными разработчика"""
        data = super().to_dict()
        data.update({
            'tech_stack': self.__tech_stack,
            'seniority_level': self.__seniority_level
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Developer':
        """Создает объект Developer из словаря"""
        return cls(
            id=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            tech_stack=data['tech_stack'],
            seniority_level=data['seniority_level'],
            skip_validation=True
        )
        

class Saleperson(Employee):
    def __init__(self, id, name, department, base_salary, commission_rate, sales_volume, skip_validation=False):
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume
        super().__init__(id, name, department, base_salary, skip_validation)
    def calculate_salary(self):
        return self.base_salary + (self.__commission_rate * self.__sales_volume)

    def update_sales(self, sales_volume):
        self.__sales_volume += sales_volume

    def get_info(self):
        print(f"{self.__str__()},  процент комиссии: {self.__commission_rate}, объем продаж: {self.__sales_volume}, итоговая зарплата: {self.calculate_salary()}")
    
    def to_dict(self) -> dict:
        """Возвращает словарь с данными продавца"""
        data = super().to_dict()
        data.update({
            'commission_rate': self.__commission_rate,
            'sales_volume': self.__sales_volume
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Saleperson':
        """Создает объект Saleperson из словаря"""
        return cls(
            id=data['id'],
            name=data['name'],
            department=data['department'],
            base_salary=data['base_salary'],
            commission_rate=data['commission_rate'],
            sales_volume=data['sales_volume'],
            skip_validation=True
        )
    
class EmployeeFactory:
    def create_employee(**emp_type):
        if "manager" in emp_type:
            pp = emp_type["manager"]
            manager = Manager(pp[0],pp[1],pp[2],pp[3],pp[4])
            return manager.get_info()
        if "developer" in emp_type:
            pp = emp_type["developer"]
            developer = Developer(pp[0], pp[1], pp[2], pp[3], pp[4], pp[5])
            return developer.get_info()
        if "salesperson" in emp_type:
            pp = emp_type["salesperson"]
            salesperson = Saleperson(pp[0], pp[1], pp[2], pp[3], pp[4], pp[5])
            return salesperson.get_info()
        if "employee" in emp_type:
            pp = emp_type["employee"]
            employee = Employee(pp[0], pp[1], pp[2], pp[3])
            return employee.get_info()


def compare_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по имени (по возрастанию)"""
    if emp1.name < emp2.name:
        return -1
    elif emp1.name > emp2.name:
        return 1
    else:
        return 0

def compare_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по зарплате (по убыванию)"""
    salary1 = emp1.calculate_salary()
    salary2 = emp2.calculate_salary()
    if salary1 > salary2:
        return -1
    elif salary1 < salary2:
        return 1
    else:
        return 0

def compare_by_department_then_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по отделу, затем по имени"""
    # Сначала сравниваем отделы
    if emp1.department < emp2.department:
        return -1
    elif emp1.department > emp2.department:
        return 1
    else:
        # Если отделы одинаковые, сравниваем по имени
        return compare_by_name(emp1, emp2)

def compare_by_type_then_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """Компаратор для сортировки по типу сотрудника, затем по зарплате (по убыванию)"""
    type1 = emp1.__class__.__name__
    type2 = emp2.__class__.__name__
    
    if type1 < type2:
        return -1
    elif type1 > type2:
        return 1
    else:
        # Если типы одинаковые, сравниваем по зарплате (по убыванию)
        return compare_by_salary(emp1, emp2)
        


def get_name_key(employee: 'AbstractEmployee') -> str:
    """Ключ для сортировки по имени"""
    return employee.name

def get_salary_key(employee: 'AbstractEmployee') -> float:
    """Ключ для сортировки по зарплате (для убывания используем отрицательное значение)"""
    return -employee.calculate_salary()

def get_department_name_key(employee: 'AbstractEmployee') -> tuple:
    """Ключ для сортировки по отделу, затем по имени"""
    return (employee.department, employee.name)

def get_type_salary_key(employee: 'AbstractEmployee') -> tuple:
    """Ключ для сортировки по типу, затем по зарплате (по убыванию)"""
    return (employee.__class__.__name__, -employee.calculate_salary())


Brenda = Saleperson(5, "Brenda", "4", 30000, 0.1, 5000)
Stiles = Developer(4, "Stiles", "5", 30000, ["C++","C","Python"], "middle")
Bread = Manager(3, "Bread", "4", 30000, 500)
tom2 = Employee(1, "Tom2", "2", 30001)
Bread.get_info()
Stiles.get_info()
Brenda.get_info()

EmployeeFactory.create_employee(manager = [6,"Pit","4",30000,100])
EmployeeFactory.create_employee(developer = [7, "Jhony", "5", 30000, ["C++","C","Python"], "junior"])
EmployeeFactory.create_employee(salesperson = [8, "Scot", "4", 30000, 0.1, 5000])
EmployeeFactory.create_employee(employee = [9,"Nick", "1", 30000])


class Department:
    def __init__(self, name: str):
        if not name or not isinstance(name, str):
            raise ValueError("Название отдела должно быть непустой строкой")
        self.name = name
        self.spis: List[AbstractEmployee] = []

    def add_employee(self, employee: AbstractEmployee) -> None:
        """Добавляет сотрудника в отдел"""
        # Проверяем, нет ли сотрудника с таким ID
        if any(emp.id == employee.id for emp in self.spis):
            raise ValueError(f"Сотрудник с ID {employee.id} уже существует в отделе")
        
        self.spis.append(employee)
        print(f"Сотрудник {employee.name} добавлен в отдел {self.name}")

    def remove_employee(self, employee_id: int) -> None:
        """Удаляет сотрудника по ID"""
        for i, employee in enumerate(self.spis):
            if employee.id == employee_id:
                removed_employee = self.spis.pop(i)
                print(f"Сотрудник {removed_employee.name} (ID: {employee_id}) удален из отдела {self.name}")
                return
        
        print(f"Сотрудник с ID {employee_id} не найден в отделе {self.name}")

    def get_employees(self) -> List[AbstractEmployee]:
        """Возвращает список всех сотрудников"""
        return self.spis.copy()
        
    def calculate_total_salary(self):
        c = 0 
        for i in self.spis.copy():
            c += i.calculate_salary()
            
        return c
            
    def get_employee_count(self):
        self.slovar_otdel = {
            "Manager" : 0,
            "Developer" : 0,
            "Salesperson" : 0,
            "Employee" : 0
            
        }
        for i in self.spis.copy():
            a = i.__class__.__name__
            if a in self.slovar_otdel.keys():
                self.slovar_otdel[str(a)] += 1
            
        return self.slovar_otdel
        
    def find_employee_by_id(self, empole_id):
        for i in self.spis.copy():
            if i.id == empole_id:
                return i
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе {self.name}")
    

    def __len__(self):
        return len(self.spis)
    
    def __getitem__(self, key) -> AbstractEmployee:
        for i in self.spis.copy():
            if i.id == key:
                return i
        
    def __contains__(self, employee: AbstractEmployee) -> bool:
        return any(emp.id == employee.id for emp in self.spis)
    
    def __iter__(self):
        return iter(self.spis)
        
    def save_to_file(self, filename: str) -> None:
        try:
            # Получаем данные отдела в виде словаря
            department_data = self.to_dict()
            
            # Сохраняем в файл с красивым форматированием
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(department_data, file, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"Ошибка при сохранении в файл '{filename}': {e}")
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """Загружает отдел из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                department_data = json.load(file)
            
            department = cls.from_dict(department_data)
            print(f"Данные отдела успешно загружены из файла '{filename}'")
            print(f"Загружено сотрудников: {len(department)}")
            
            return department
            
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден")
            return cls("Новый отдел")
        except Exception as e:
            print(f"Ошибка при загрузке из файла '{filename}': {e}")
            return cls("Новый отдел")
    def to_dict(self) -> dict:
        """Возвращает словарь с данными отдела"""
        return {
            'name': self.name,
            'employee_count': len(self.spis),
            'total_salary': self.calculate_total_salary(),
            'employees_by_type': self.get_employee_count(),
            'employees': [emp.to_dict() for emp in self.spis]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Department':
        """Создает объект Department из словаря"""
        department = cls(data['name'])
        for emp_data in data['employees']:
            employee = AbstractEmployee.from_dict(emp_data)
            department.add_employee(employee)
        return department

    def has_employees(self) -> bool:
        """Проверяет, есть ли сотрудники в отделе"""
        return len(self.spis) > 0

        
dep = Department("tytytyt")
dep.add_employee(tom2)
dep.add_employee(Bread)
dep.add_employee(Stiles)
#print(*dep.get_employees())
#print(dep.calculate_total_salary())
#dep.get_employee_count()

#print(dep.find_employee_by_id(1))

employees_list = [tom2, Bread, Stiles, Brenda]

#print(tom2 == Bread)
#print(*sorted(employees_list))
#print(tom2 + Bread)
#print(sum(employees_list))


#print(len(dep))
#print(dep[1])

#print(tom2 in dep)

#print(*list(dep))

#print(*list(Stiles))


tom2_dict = tom2.to_dict()
bread_dict = Bread.to_dict()
stiles_dict = Stiles.to_dict()
brenda_dict = Brenda.to_dict()

print("Словари:")
print("Employee:", tom2_dict)
print("Manager:", bread_dict)
print("Developer:", stiles_dict)
print("Salesperson:", brenda_dict)

print("\nВосстановленные объекты:")
tom2_restored = AbstractEmployee.from_dict(tom2_dict)
bread_restored = AbstractEmployee.from_dict(bread_dict)
stiles_restored = AbstractEmployee.from_dict(stiles_dict)
brenda_restored = AbstractEmployee.from_dict(brenda_dict)

# Проверяем, что объекты восстановились корректно
print("Employee восстановлен:", tom2_restored.to_dict())
print("Manager восстановлен:", bread_restored.to_dict())
print("Developer восстановлен:", stiles_restored.to_dict())
print("Salesperson восстановлен:", brenda_restored.to_dict())


dep.save_to_file("dep.json")


loaded_dep = Department.load_from_file("dep.json")

employees = employees_list
print("1. СОРТИРОВКА ПО ИМЕНИ (key=):")
sorted_by_name = sorted(employees, key=get_name_key)
for emp in sorted_by_name:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")


print("\n2. СОРТИРОВКА ПО ЗАРПЛАТЕ (ПО УБЫВАНИЮ, key=):")
sorted_by_salary = sorted(employees, key=get_salary_key)
for emp in sorted_by_salary:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")


print("\n3. СОРТИРОВКА ПО ОТДЕЛУ И ИМЕНИ (key=):")
sorted_by_dept_name = sorted(employees, key=get_department_name_key)
for emp in sorted_by_dept_name:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")
    
print("4 СОРТИРОВКА ПО ИМЕНИ (компаратор):")
sorted_cmp_name = sorted(employees, key=cmp_to_key(compare_by_name))
for emp in sorted_cmp_name:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")

print("\n5 СОРТИРОВКА ПО ЗАРПЛАТЕ (ПО УБЫВАНИЮ, компаратор):")
sorted_cmp_salary = sorted(employees, key=cmp_to_key(compare_by_salary))
for emp in sorted_cmp_salary:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")


print("\n6 СОРТИРОВКА ПО ОТДЕЛУ И ИМЕНИ (компаратор):")
sorted_cmp_dept_name = sorted(employees, key=cmp_to_key(compare_by_department_then_name))
for emp in sorted_cmp_dept_name:
    print(f"  {emp.name:12} | {emp.department:6} | {emp.calculate_salary():8.0f} | {emp.__class__.__name__}")



class Project:
    _existing_project_ids = set()
    _valid_statuses = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, project_id, name, description, deadline, status, team = []):

        Validator.validate_project_id(project_id, self._existing_project_ids)
        self._existing_project_ids.add(project_id)

        Validator.validate_status(status, self._valid_statuses)
        
        Validator.validate_date(deadline)
        
        self.project_id = project_id
        self.name = name
        self.description = description
        self.deadline = deadline
        self.status = status
        self.__team = team
        self.__valid_statuses = ["planning", "active", "completed", "cancelled"]
        
    def add_team_member(self, employee: AbstractEmployee) -> None:
        #if any(emp.id == employee.id for emp in self.__team):
        #    raise ValueError(f"Сотрудник с ID {employee.id} уже существует в отделе")
        self.__team.append(employee)
        print(f"Сотрудник {employee.name} добавлен в отдел {self.name}")
        
        

    def remove_team_member(self, employee_id: int) -> None:
        for i, employee in enumerate(self.__team):
            if employee.id == employee_id:
                removed_employee = self.__team.pop(i)
                print(f"Сотрудник {removed_employee.name} (ID: {employee_id}) удален из проекта {self.name}")
                return
        
        print(f"Сотрудник с ID {employee_id} не найден в отделе {self.name}")


    def get_team(self) -> list[AbstractEmployee]:
        spisok_pro = []
        for i in self.__team.copy():
            spisok_pro.append(i.__str__())
        return spisok_pro

    def get_team_size(self) -> int:
        return(len(self.__team.copy()))

    def calculate_total_salary(self):
        c = 0 
        for i in self.__team.copy():
            c += i.calculate_salary()
            
        return c
    def get_project_info(self) -> str:
        return f"id проекта {self.project_id}, название {self.name}, описание {self.description}, дедлайн {self.deadline}, статус {self.status}, команда {proektik.get_team()}"

    
    
    def change_status(self, new_status: str) -> None:
        """Изменяет статус проекта с валидацией"""
        # ВАЛИДАЦИЯ: проверяем, что новый статус допустимый
        if new_status not in self.__valid_statuses:
            raise ValueError(f"Недопустимый статус: '{new_status}'. Допустимые статусы: {self.__valid_statuses}")
        
        # ВАЛИДАЦИЯ: проверяем логику смены статусов
        old_status = self.status
        
        # Нельзя перейти из completed или cancelled в другие статусы
        if old_status in ["completed", "cancelled"]:
            raise ValueError(f"Нельзя изменить статус проекта с '{old_status}' на '{new_status}'")

        self.status = new_status
        print(f"Статус проекта '{self.name}' изменен: '{old_status}' -> '{new_status}'")

    def has_team_members(self) -> bool:
        """Проверяет, есть ли участники в проекте"""
        return len(self.__team) > 0

    def is_employee_in_project(self, employee_id: int) -> bool:
        """Проверяет, участвует ли сотрудник в проекте"""
        return any(emp.id == employee_id for emp in self.__team)



proektik = Project("1","Proekt_name", "описание проекта", "2025-12-15", "active", [tom2, Stiles])
proektik.add_team_member(Bread)
proektik.remove_team_member(1)
proektik.get_team()
print(proektik.get_team_size())
print(proektik.calculate_total_salary())
print(proektik.get_project_info())

proektik.change_status("planning") 
proektik.change_status("active")  



class Company:
    def __init__(self, name: str, departments: list[Department] = [], projects: list[Project] = []):
        if not name or not isinstance(name, str):
            raise ValueError("Название компании должно быть непустой строкой")
        
        self.name = name
        self.__departments = departments
        self.__projects = projects

    def add_department(self, department_or_name) -> Department:
        """Добавляет отдел в компанию (принимает как объект Department, так и название)"""
        if isinstance(department_or_name, Department):
            department = department_or_name
            name = department.name
        else:
            department = Department(department_or_name)
            name = department_or_name
        
        if any(dept.name == name for dept in self.__departments):
            raise DuplicateIdError(f"Отдел с названием '{name}' уже существует в компании")
        
        self.__departments.append(department)
        print(f"Отдел '{name}' добавлен в компанию '{self.name}'")
        return department
    
    
    def get_departments(self):
        for i in self.__departments.copy():
            print(i.name)


    def add_project(self, project_or_id, name=None, description=None, deadline=None, status="planning") -> Project:
        """Добавляет проект в компанию (принимает как объект Project, так и параметры для создания)"""
        if isinstance(project_or_id, Project):
            project = project_or_id
            project_id = project.project_id
        else:
            project_id = project_or_id
            if name is None or description is None or deadline is None:
                raise ValueError("Для создания проекта необходимо указать name, description и deadline")
            project = Project(project_id, name, description, deadline, status, [])
        
        if any(proj.project_id == project_id for proj in self.__projects):
            raise ValueError(f"Проект с ID '{project_id}' уже существует в компании")
        
        self.__projects.append(project)
        print(f"Проект '{project.name}' (ID: {project_id}) добавлен в компанию '{self.name}'")
        return project

    def remove_project(self, project_id: str) -> bool:
        """Удаляет проект из компании по ID с проверкой"""
        for i, project in enumerate(self.__projects):
            if project.project_id == project_id:
                if project.has_team_members():
                    raise ValueError(f"Нельзя удалить проект '{project.name}': в нем есть участники команды")
                
                removed_project = self.__projects.pop(i)
                print(f"Проект '{removed_project.name}' (ID: {project_id}) удален из компании '{self.name}'")
                return True
        
        raise ProjectNotFoundError(f"Проект с ID {project_id} не найден в компании '{self.name}'")

    def get_projects(self) -> List[Project]:
        spisok = []
        for i in self.__projects.copy():
            spisok.append(i.name)
        return spisok

    # Метод для получения всех сотрудников
    def get_all_employees(self) -> List[AbstractEmployee]:
        """Возвращает список всех сотрудников компании из всех отделов"""
        all_employees = []
        for department in self.__departments:
            all_employees.extend(department.get_employees())
        return all_employees

    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Поиск сотрудника по ID во всех отделах компании"""
        for department in self.__departments:
            try:
                employee = department.find_employee_by_id(employee_id)
                if employee:
                    return employee
            except EmployeeNotFoundError:
                continue
        
        raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в компании")

    def calculate_total_monthly_cost(self) -> float:
        """Расчет общих месячных затрат на зарплаты всех сотрудников"""
        total_cost = 0.0
        for department in self.__departments:
            total_cost += department.calculate_total_salary()
        return total_cost

    def get_projects_by_status(self, status: str) -> List[Project]:
        """Фильтрация проектов по статусу"""
        valid_statuses = ["planning", "active", "completed", "cancelled"]
        if status not in valid_statuses:
            raise ValueError(f"Недопустимый статус: '{status}'. Допустимые: {valid_statuses}")
        
        return [project for project in self.__projects if project.status == status]

    def is_employee_in_projects(self, employee_id: int) -> bool:
        """Проверяет, участвует ли сотрудник в каких-либо проектах"""
        for project in self.__projects:
            if project.is_employee_in_project(employee_id):
                return True
        return False

    def remove_department(self, name: str) -> bool:
        """Удаляет отдел из компании с проверкой"""
        for i, department in enumerate(self.__departments):
            if department.name == name:
                if department.has_employees():
                    raise ValueError(f"Нельзя удалить отдел '{name}': в нем есть сотрудники")
                
                removed_department = self.__departments.pop(i)
                print(f"Отдел '{name}' удален из компании '{self.name}'")
                return True
        raise DepartmentNotFoundError(f"Отдел с названием '{name}' не найден в компании '{self.name}'")

    def remove_employee_from_company(self, employee_id: int) -> bool:
        """Удаляет сотрудника из компании (из всех отделов) с проверкой"""
        if self.is_employee_in_projects(employee_id):
            raise ValueError(f"Нельзя удалить сотрудника ID {employee_id}: он участвует в проектах")
        
        employee_removed = False
        for department in self.__departments:
            try:
                department.remove_employee(employee_id)
                employee_removed = True
            except ValueError:
                continue
        
        if employee_removed:
            print(f"Сотрудник ID {employee_id} удален из компании '{self.name}'")
            return True
        else:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в компании")
    #АНАЛИЗ
    def get_department_stats(self) -> Dict[str, Dict]:
        """Возвращает детальную статистику по всем отделам"""
        stats = {}
        
        for department in self.__departments:
            dept_stats = {
                'name': department.name,
                'total_employees': len(department),
                'total_salary': department.calculate_total_salary(),
                'employee_count_by_type': department.get_employee_count(),
                'average_salary': 0,
                'salary_distribution': {},
                'projects_involvement': 0
            }
            
            # Расчет средней зарплаты
            if dept_stats['total_employees'] > 0:
                dept_stats['average_salary'] = dept_stats['total_salary'] / dept_stats['total_employees']
            
            # Распределение зарплат
            salaries = [emp.calculate_salary() for emp in department.get_employees()]
            if salaries:
                dept_stats['salary_distribution'] = {
                    'min': min(salaries),
                    'max': max(salaries),
                    'median': sorted(salaries)[len(salaries) // 2]
                }
            
            # Участие в проектах
            dept_employee_ids = {emp.id for emp in department.get_employees()}
            dept_stats['projects_involvement'] = sum(
                1 for project in self.__projects 
                if any(emp.id in dept_employee_ids for emp in project._Project__team)
            )
            
            stats[department.name] = dept_stats
        
        # Добавляем общую статистику
        stats['_company_summary'] = {
            'total_departments': len(self.__departments),
            'total_employees': sum(stats[dept]['total_employees'] for dept in stats if not dept.startswith('_')),
            'total_monthly_cost': self.calculate_total_monthly_cost(),
            'most_expensive_department': max(
                (dept for dept in stats if not dept.startswith('_')), 
                key=lambda x: stats[x]['total_salary']
            ) if stats else None
        }
        
        return stats
    
    def get_project_budget_analysis(self) -> Dict[str, Dict]:
        """Анализ бюджетов и эффективности проектов"""
        analysis = {}
        
        for project in self.__projects:
            project_analysis = {
                'name': project.name,
                'status': project.status,
                'team_size': project.get_team_size(),
                'total_salary_cost': project.calculate_total_salary(),
                'deadline': project.deadline,
                'days_until_deadline': self._days_until_date(project.deadline),
                'team_composition': {},
                'cost_per_member': 0,
                'efficiency_score': 0
            }
            
            # Состав команды по типам
            team_composition = {}
            for employee in project._Project__team:
                emp_type = employee.__class__.__name__
                team_composition[emp_type] = team_composition.get(emp_type, 0) + 1
            project_analysis['team_composition'] = team_composition
            
            # Стоимость на участника
            if project_analysis['team_size'] > 0:
                project_analysis['cost_per_member'] = (
                    project_analysis['total_salary_cost'] / project_analysis['team_size']
                )
            
            # Оценка эффективности (чем меньше команда и стоимость - тем выше оценка)
            base_score = 100
            if project_analysis['team_size'] > 0:
                # Штраф за большой размер команды
                size_penalty = min(project_analysis['team_size'] * 2, 30)
                # Штраф за высокую стоимость на участника
                cost_penalty = min(project_analysis['cost_per_member'] / 1000, 40)
                # Бонус за близкий дедлайн (срочность)
                deadline_bonus = max(30 - project_analysis['days_until_deadline'] / 10, 0)
                
                project_analysis['efficiency_score'] = max(
                    base_score - size_penalty - cost_penalty + deadline_bonus, 0
                )
            
            analysis[project.project_id] = project_analysis
        
        # Сравнительная статистика
        if analysis:
            active_projects = [p for p in analysis.values() if p['status'] == 'active']
            if active_projects:
                analysis['_comparison'] = {
                    'avg_team_size_active': sum(p['team_size'] for p in active_projects) / len(active_projects),
                    'avg_cost_active': sum(p['total_salary_cost'] for p in active_projects) / len(active_projects),
                    'most_efficient_active': max(active_projects, key=lambda x: x['efficiency_score'])['name'],
                    'most_expensive_active': max(active_projects, key=lambda x: x['total_salary_cost'])['name']
                }
        
        return analysis
    
    def _days_until_date(self, date_str: str) -> int:
        """Рассчитывает количество дней до указанной даты"""
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            current_date = datetime.now()
            return (target_date - current_date).days
        except ValueError:
            return 9999  # Большое число для некорректных дат
    
    def find_overloaded_employees(self, max_projects: int = 2) -> List[AbstractEmployee]:
        """Находит сотрудников, участвующих в слишком многих проектах"""
        employee_project_count = {}
        
        # Считаем количество проектов для каждого сотрудника
        for project in self.__projects:
            for employee in project._Project__team:
                employee_project_count[employee.id] = employee_project_count.get(employee.id, 0) + 1
        
        # Находим перегруженных сотрудников
        overloaded_employees = []
        for department in self.__departments:
            for employee in department.get_employees():
                project_count = employee_project_count.get(employee.id, 0)
                if project_count > max_projects:
                    # Добавляем информацию о перегрузке
                    overloaded_info = {
                        'employee': employee,
                        'project_count': project_count,
                        'current_projects': []
                    }
                    
                    # Находим в каких проектах участвует сотрудник
                    for project in self.__projects:
                        if any(emp.id == employee.id for emp in project._Project__team):
                            overloaded_info['current_projects'].append(project.name)
                    
                    overloaded_employees.append(overloaded_info)
        
        # Сортируем по уровню перегрузки
        overloaded_employees.sort(key=lambda x: x['project_count'], reverse=True)
        return overloaded_employees
    
    def get_employee_workload_report(self) -> Dict[str, any]:
        """Генерирует отчет о загрузке сотрудников"""
        workload_data = {
            'overloaded_employees': self.find_overloaded_employees(),
            'employee_project_distribution': {},
            'department_workload': {}
        }
        
        # Распределение сотрудников по количеству проектов
        project_count_distribution = {}
        for department in self.__departments:
            for employee in department.get_employees():
                project_count = sum(
                    1 for project in self.__projects 
                    if any(emp.id == employee.id for emp in project._Project__team)
                )
                project_count_distribution[project_count] = project_count_distribution.get(project_count, 0) + 1
        
        workload_data['employee_project_distribution'] = project_count_distribution
        
        # Загрузка по отделам
        for department in self.__departments:
            dept_workload = {
                'total_employees': len(department),
                'employees_in_projects': 0,
                'avg_projects_per_employee': 0,
                'overloaded_count': 0
            }
            
            total_projects = 0
            for employee in department.get_employees():
                emp_project_count = sum(
                    1 for project in self.__projects 
                    if any(emp.id == employee.id for emp in project._Project__team)
                )
                if emp_project_count > 0:
                    dept_workload['employees_in_projects'] += 1
                if emp_project_count > 2:  # Перегруженные
                    dept_workload['overloaded_count'] += 1
                total_projects += emp_project_count
            
            if dept_workload['total_employees'] > 0:
                dept_workload['avg_projects_per_employee'] = (
                    total_projects / dept_workload['total_employees']
                )
            
            workload_data['department_workload'][department.name] = dept_workload
        
        return workload_data

#ПЛАНАИРОВАНИЕ
    def assign_employee_to_project(self, employee_id: int, project_id: str) -> bool:
        """Назначает сотрудника на проект с проверкой доступности"""
        # Находим сотрудника
        employee = self.find_employee_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        
        # Находим проект
        project = None
        for proj in self.__projects:
            if proj.project_id == project_id:
                project = proj
                break
        
        if not project:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
        
        # Проверяем доступность сотрудника
        if not self.check_employee_availability(employee_id):
            current_projects = self.get_employee_projects(employee_id)
            raise ValueError(
                f"Сотрудник {employee.name} перегружен. "
                f"Текущие проекты: {', '.join(current_projects)}"
            )
        
        # Проверяем, не участвует ли уже в проекте
        if project.is_employee_in_project(employee_id):
            raise ValueError(f"Сотрудник {employee.name} уже участвует в проекте '{project.name}'")
        
        # Назначаем на проект
        project.add_team_member(employee)
        print(f"Сотрудник {employee.name} назначен на проект '{project.name}'")
        return True
    
    def check_employee_availability(self, employee_id: int, max_projects: int = 3) -> bool:
        """Проверяет доступность сотрудника для новых проектов"""
        current_project_count = sum(
            1 for project in self.__projects 
            if project.is_employee_in_project(employee_id)
        )
        return current_project_count < max_projects
    
    def get_employee_projects(self, employee_id: int) -> List[str]:
        """Возвращает список проектов, в которых участвует сотрудник"""
        projects = []
        for project in self.__projects:
            if project.is_employee_in_project(employee_id):
                projects.append(project.name)
        return projects
    
    def bulk_assign_to_project(self, employee_ids: List[int], project_id: str) -> Dict[str, any]:
        """Массовое назначение сотрудников на проект"""
        results = {
            'successful': [],
            'failed': [],
            'total_assigned': 0
        }
        
        for employee_id in employee_ids:
            try:
                success = self.assign_employee_to_project(employee_id, project_id)
                if success:
                    results['successful'].append(employee_id)
                    results['total_assigned'] += 1
            except (EmployeeNotFoundError, ProjectNotFoundError, ValueError) as e:
                results['failed'].append({
                    'employee_id': employee_id,
                    'error': str(e)
                })
        
        return results
    
    def optimize_workload_distribution(self) -> Dict[str, any]:
        """Оптимизирует распределение нагрузки между сотрудниками"""
        optimization_report = {
            'suggestions': [],
            'transfers_recommended': [],
            'workload_balanced': False
        }
        
        # Анализ текущей нагрузки
        workload_data = self.get_employee_workload_report()
        overloaded_employees = workload_data['overloaded_employees']
        
        if not overloaded_employees:
            optimization_report['workload_balanced'] = True
            optimization_report['suggestions'].append("Нагрузка распределена оптимально")
            return optimization_report
        
        # Предложения по оптимизации
        for overloaded in overloaded_employees:
            employee = overloaded['employee']
            suggestion = {
                'employee': employee.name,
                'current_projects': overloaded['project_count'],
                'recommendation': f"Снять с {overloaded['project_count'] - 2} проектов",
                'specific_projects': overloaded['current_projects'][2:]  # Проекты для снятия
            }
            optimization_report['suggestions'].append(suggestion)
        
        # Анализ отделов с низкой загрузкой
        underloaded_departments = []
        for dept_name, dept_data in workload_data['department_workload'].items():
            if dept_data['avg_projects_per_employee'] < 1.0:
                underloaded_departments.append({
                    'department': dept_name,
                    'avg_projects': dept_data['avg_projects_per_employee'],
                    'available_capacity': dept_data['total_employees'] - dept_data['employees_in_projects']
                })
        
        # Рекомендации по перераспределению
        if underloaded_departments and overloaded_employees:
            optimization_report['transfers_recommended'] = [
                f"Рассмотреть передачу задач из перегруженных отделов в {dept['department']} "
                f"(доступно {dept['available_capacity']} сотрудников)"
                for dept in underloaded_departments
            ]
        
        return optimization_report
    
    def get_resource_planning_report(self) -> str:
        """Генерирует отчет для планирования ресурсов"""
        workload_report = self.get_employee_workload_report()
        optimization = self.optimize_workload_distribution()
        
        report_lines = []
        report_lines.append("ОТЧЕТ ПО ПЛАНИРОВАНИЮ РЕСУРСОВ")
        report_lines.append("=" * 50)
        
        # Статистика загрузки
        report_lines.append("\nСТАТИСТИКА ЗАГРУЗКИ:")
        total_employees = sum(
            workload_report['department_workload'][dept]['total_employees'] 
            for dept in workload_report['department_workload']
        )
        employees_in_projects = sum(
            workload_report['department_workload'][dept]['employees_in_projects'] 
            for dept in workload_report['department_workload']
        )
        
        report_lines.append(f"Всего сотрудников: {total_employees}")
        report_lines.append(f"Занято в проектах: {employees_in_projects} ({employees_in_projects/total_employees*100:.1f}%)")
        report_lines.append(f"Перегружено: {len(workload_report['overloaded_employees'])}")
        
        # Распределение по количеству проектов
        report_lines.append("\nРАСПРЕДЕЛЕНИЕ ПО НАГРУЗКЕ:")
        for project_count, employee_count in workload_report['employee_project_distribution'].items():
            report_lines.append(f"  {project_count} проектов: {employee_count} сотрудников")
        
        # Рекомендации по оптимизации
        report_lines.append("\nРЕКОМЕНДАЦИИ:")
        if optimization['workload_balanced']:
            report_lines.append("  ✓ Нагрузка распределена оптимально")
        else:
            for suggestion in optimization['suggestions']:
                report_lines.append(f"  • {suggestion['employee']}: {suggestion['recommendation']}")
            
            for transfer in optimization['transfers_recommended']:
                report_lines.append(f"  → {transfer}")
        
        return "\n".join(report_lines)

    def to_dict(self) -> dict:
        """Возвращает словарь с данными всей компании для сериализации"""
        return {
            'company_name': self.name,
            'departments': [dept.to_dict() for dept in self.__departments],
            'projects': [self._project_to_dict(proj) for proj in self.__projects],
            'metadata': {
                'total_employees': sum(len(dept) for dept in self.__departments),
                'total_projects': len(self.__projects),
                'total_monthly_cost': self.calculate_total_monthly_cost(),
                'export_date': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
    
    def _project_to_dict(self, project: Project) -> dict:
        """Конвертирует проект в словарь с сохранением связей"""
        return {
            'project_id': project.project_id,
            'name': project.name,
            'description': project.description,
            'deadline': project.deadline,
            'status': project.status,
            'team_size': project.get_team_size(),
            'team_member_ids': [emp.id for emp in project._Project__team],  # Сохраняем только ID для избежания циклических ссылок
            'total_salary_cost': project.calculate_total_salary()
        }
    
    def save_to_json(self, filename: str) -> None:
        """Сохраняет всю компанию в JSON файл"""
        try:
            company_data = self.to_dict()
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(company_data, file, ensure_ascii=False, indent=2)
            
            print(f"Компания '{self.name}' успешно сохранена в файл '{filename}'")
            print(f"Сохранено: {len(self.__departments)} отделов, "
                  f"{sum(len(dept) for dept in self.__departments)} сотрудников, "
                  f"{len(self.__projects)} проектов")
            
        except Exception as e:
            print(f"Ошибка при сохранении компании в файл '{filename}': {e}")
    
    @classmethod
    def load_from_json(cls, filename: str) -> 'Company':
        """Загружает компанию из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                company_data = json.load(file)
            
            # Валидация структуры данных
            if not all(key in company_data for key in ['company_name', 'departments', 'projects']):
                raise ValueError("Некорректная структура файла компании")
            
            # Создаем компанию
            company = cls(company_data['company_name'])
            
            # Восстанавливаем отделы и сотрудников
            employee_id_map = {}  # Для связи ID -> объект сотрудника
            
            # Сначала создаем всех сотрудников
            for dept_data in company_data['departments']:
                department = Department(dept_data['name'])
                company.add_department(department)
                
                for emp_data in dept_data['employees']:
                    # Валидация данных сотрудника
                    if not all(key in emp_data for key in ['id', 'name', 'department', 'base_salary', 'type']):
                        print(f"Предупреждение: Пропущен сотрудник с некорректными данными")
                        continue
                    
                    try:
                        employee = AbstractEmployee.from_dict(emp_data)
                        department.add_employee(employee)
                        employee_id_map[employee.id] = employee
                    except (ValueError, DuplicateIdError) as e:
                        print(f"Предупреждение: Не удалось создать сотрудника {emp_data.get('name', 'Unknown')}: {e}")
            
            # Восстанавливаем проекты и связи
            for proj_data in company_data['projects']:
                # Валидация данных проекта
                if not all(key in proj_data for key in ['project_id', 'name', 'description', 'deadline', 'status']):
                    print(f"Предупреждение: Пропущен проект с некорректными данными")
                    continue
                
                try:
                    # Создаем проект с пустой командой
                    project = Project(
                        proj_data['project_id'],
                        proj_data['name'],
                        proj_data['description'],
                        proj_data['deadline'],
                        proj_data['status'],
                        []
                    )
                    
                    # Восстанавливаем команду проекта
                    team_member_ids = proj_data.get('team_member_ids', [])
                    for employee_id in team_member_ids:
                        if employee_id in employee_id_map:
                            project.add_team_member(employee_id_map[employee_id])
                        else:
                            print(f"Предупреждение: Сотрудник ID {employee_id} не найден для проекта '{proj_data['name']}'")
                    
                    company.add_project(project)
                except (ValueError, DuplicateIdError, InvalidDateError, InvalidStatusError) as e:
                    print(f"Предупреждение: Не удалось создать проект '{proj_data.get('name', 'Unknown')}': {e}")
            
            print(f"Компания '{company.name}' успешно загружена из файла '{filename}'")
            print(f"Загружено: {len(company.__departments)} отделов, "
                  f"{sum(len(dept) for dept in company.__departments)} сотрудников, "
                  f"{len(company.__projects)} проектов")
            
            return company
            
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден")
            return cls("Новая компания")
        except json.JSONDecodeError:
            print(f"Ошибка: Файл '{filename}' содержит некорректный JSON")
            return cls("Новая компания")
        except Exception as e:
            print(f"Ошибка при загрузке компании из файла '{filename}': {e}")
            return cls("Новая компания")
    
    def export_employees_csv(self, filename: str) -> None:
        """Экспортирует данные о сотрудниках в CSV файл"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Заголовки
                writer.writerow([
                    'ID', 'Имя', 'Отдел', 'Должность', 'Базовая зарплата',
                    'Дополнительные параметры', 'Итоговая зарплата', 'Участвует в проектах'
                ])
                
                # Данные
                for department in self.__departments:
                    for employee in department.get_employees():
                        # Определяем дополнительные параметры в зависимости от типа
                        additional_info = ""
                        if isinstance(employee, Manager):
                            additional_info = f"Бонус: {employee.bonus}"
                        elif isinstance(employee, Developer):
                            tech_stack = ', '.join(employee._Developer__tech_stack)
                            additional_info = f"Уровень: {employee._Developer__seniority_level}, Технологии: {tech_stack}"
                        elif isinstance(employee, Saleperson):
                            additional_info = f"Комиссия: {employee._Saleperson__commission_rate}, Продажи: {employee._Saleperson__sales_volume}"
                        
                        # Определяем участие в проектах
                        project_names = self.get_employee_projects(employee.id)
                        projects_info = ', '.join(project_names) if project_names else "Нет"
                        
                        writer.writerow([
                            employee.id,
                            employee.name,
                            employee.department,
                            employee.__class__.__name__,
                            f"{employee.base_salary:.2f}",
                            additional_info,
                            f"{employee.calculate_salary():.2f}",
                            projects_info
                        ])
            
            print(f"Данные о сотрудниках экспортированы в '{filename}'")
            print(f"Экспортировано {sum(len(dept) for dept in self.__departments)} сотрудников")
            
        except Exception as e:
            print(f"Ошибка при экспорте сотрудников в CSV '{filename}': {e}")
    
    def export_projects_csv(self, filename: str) -> None:
        """Экспортирует данные о проектах в CSV файл"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Заголовки
                writer.writerow([
                    'ID проекта', 'Название', 'Описание', 'Дедлайн', 'Статус',
                    'Размер команды', 'Бюджет на зарплаты', 'Состав команды', 'Дней до дедлайна'
                ])
                
                # Данные
                for project in self.__projects:
                    team_members = ", ".join([emp.name for emp in project._Project__team])
                    days_until_deadline = self._days_until_date(project.deadline)
                    
                    writer.writerow([
                        project.project_id,
                        project.name,
                        project.description,
                        project.deadline,
                        project.status,
                        project.get_team_size(),
                        f"{project.calculate_total_salary():.2f}",
                        team_members,
                        days_until_deadline
                    ])
            
            print(f"Данные о проектах экспортированы в '{filename}'")
            print(f"Экспортировано {len(self.__projects)} проектов")
            
        except Exception as e:
            print(f"Ошибка при экспорте проектов в CSV '{filename}': {e}")
    
    def generate_financial_report(self, filename: str) -> None:
        """Генерирует текстовый финансовый отчет компании"""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f"ФИНАНСОВЫЙ ОТЧЕТ КОМПАНИИ '{self.name}'\n")
                file.write("=" * 60 + "\n\n")
                
                file.write(f"Дата формирования: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Общая статистика
                total_employees = sum(len(dept) for dept in self.__departments)
                total_cost = self.calculate_total_monthly_cost()
                avg_salary = total_cost / total_employees if total_employees > 0 else 0
                
                file.write("ОБЩАЯ СТАТИСТИКА:\n")
                file.write("-" * 40 + "\n")
                file.write(f"Всего сотрудников: {total_employees}\n")
                file.write(f"Всего отделов: {len(self.__departments)}\n")
                file.write(f"Всего проектов: {len(self.__projects)}\n")
                file.write(f"Общие месячные затраты: {total_cost:,.2f} руб.\n")
                file.write(f"Средняя зарплата: {avg_salary:,.2f} руб.\n\n")
                
                # Статистика по отделам
                file.write("СТАТИСТИКА ПО ОТДЕЛАМ:\n")
                file.write("-" * 40 + "\n")
                
                dept_stats = self.get_department_stats()
                for dept_name, stats in dept_stats.items():
                    if not dept_name.startswith('_'):
                        file.write(f"\n{dept_name}:\n")
                        file.write(f"  Сотрудников: {stats['total_employees']}\n")
                        file.write(f"  Затраты: {stats['total_salary']:,.2f} руб.\n")
                        file.write(f"  Средняя зарплата: {stats['average_salary']:,.2f} руб.\n")
                        file.write(f"  Участвует в проектах: {stats['projects_involvement']}\n")
                        
                        # Распределение зарплат
                        if stats['salary_distribution']:
                            dist = stats['salary_distribution']
                            file.write(f"  Зарплаты: от {dist['min']:,.0f} до {dist['max']:,.0f} руб.\n")
                
                # Статистика по проектам
                file.write("\nСТАТИСТИКА ПО ПРОЕКТАМ:\n")
                file.write("-" * 40 + "\n")
                
                project_analysis = self.get_project_budget_analysis()
                active_cost = sum(p['total_salary_cost'] for p in project_analysis.values() 
                                if not p.get('project_id', '').startswith('_') and p['status'] == 'active')
                planning_cost = sum(p['total_salary_cost'] for p in project_analysis.values() 
                                  if not p.get('project_id', '').startswith('_') and p['status'] == 'planning')
                
                file.write(f"\nАктивные проекты: {len([p for p in self.__projects if p.status == 'active'])}\n")
                file.write(f"Проекты в планировании: {len([p for p in self.__projects if p.status == 'planning'])}\n")
                file.write(f"Завершенные проекты: {len([p for p in self.__projects if p.status == 'completed'])}\n")
                file.write(f"Затраты на активные проекты: {active_cost:,.2f} руб.\n")
                file.write(f"Планируемые затраты: {planning_cost:,.2f} руб.\n")
                
                # Эффективность проектов
                file.write("\nЭФФЕКТИВНОСТЬ ПРОЕКТОВ:\n")
                file.write("-" * 40 + "\n")
                
                efficient_projects = []
                for project_id, analysis in project_analysis.items():
                    if not project_id.startswith('_') and analysis['status'] == 'active':
                        efficient_projects.append((analysis['name'], analysis['efficiency_score']))
                
                efficient_projects.sort(key=lambda x: x[1], reverse=True)
                for project_name, score in efficient_projects[:5]:  # Топ-5 проектов
                    file.write(f"  {project_name}: {score:.1f}/100\n")
                
                # Рекомендации по оптимизации
                file.write("\nРЕКОМЕНДАЦИИ:\n")
                file.write("-" * 40 + "\n")
                
                workload_data = self.get_employee_workload_report()
                if workload_data['overloaded_employees']:
                    file.write("ВНИМАНИЕ: Обнаружены перегруженные сотрудники:\n")
                    for overloaded in workload_data['overloaded_employees'][:3]:  # Топ-3 перегруженных
                        file.write(f"  • {overloaded['employee'].name}: {overloaded['project_count']} проектов\n")
                    file.write("Рекомендуется перераспределить нагрузку.\n")
                else:
                    file.write("✓ Нагрузка сотрудников распределена оптимально\n")
                
                # Бюджетные рекомендации
                high_cost_dept = dept_stats.get('_company_summary', {}).get('most_expensive_department')
                if high_cost_dept:
                    file.write(f"Самый затратный отдел: {high_cost_dept}\n")
                    file.write("Рекомендуется провести анализ эффективности.\n")
            
            print(f"Финансовый отчет сгенерирован в '{filename}'")
            
        except Exception as e:
            print(f"Ошибка при генерации финансового отчета '{filename}': {e}")
    
    def export_all_reports(self, base_filename: str) -> None:
        """Экспортирует все отчеты компании"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Сохраняем полные данные компании
            company_file = f"{base_filename}_company_{timestamp}.json"
            self.save_to_json(company_file)
            
            # Экспортируем CSV отчеты
            employees_file = f"{base_filename}_employees_{timestamp}.csv"
            projects_file = f"{base_filename}_projects_{timestamp}.csv"
            self.export_employees_csv(employees_file)
            self.export_projects_csv(projects_file)
            
            # Генерируем финансовый отчет
            financial_file = f"{base_filename}_financial_report_{timestamp}.txt"
            self.generate_financial_report(financial_file)
            
            # Генерируем отчет по планированию
            planning_file = f"{base_filename}_planning_report_{timestamp}.txt"
            planning_report = self.get_resource_planning_report()
            with open(planning_file, 'w', encoding='utf-8') as f:
                f.write(planning_report)
            
            print(f"\nВсе отчеты компании '{self.name}' успешно экспортированы:")
            print(f"  • Данные компании: {company_file}")
            print(f"  • Сотрудники: {employees_file}")
            print(f"  • Проекты: {projects_file}")
            print(f"  • Финансовый отчет: {financial_file}")
            print(f"  • Отчет по планированию: {planning_file}")
            
        except Exception as e:
            print(f"Ошибка при экспорте всех отчетов: {e}")


company = Company("DADA",[],[])

it_dep = company.add_department("IT")
hr_dep = company.add_department("HR")
sale_dep = company.add_department("SALE")
company.remove_department("HR")
print(company.get_departments())
        

project2 = company.add_project("2", "CSS", "Описание 2", "2025-12-31", "active")
project3 = company.add_project("3", "комиксы", "Описание 3", "2025-11-30", "active")

company.remove_project("3")
print(company.get_projects())


it_dep.add_employee(tom2)
it_dep.add_employee(Bread)
it_dep.add_employee(Stiles)
print(company.get_all_employees())

employee = company.find_employee_by_id(4)  # Ищем Stiles
if employee:
    print(f"найден сотрудник: {employee.name} ({employee.__class__.__name__})")
else:
    print("сотрудник не найден")

total_cost = company.calculate_total_monthly_cost()
print(f"Общие затраты на зарплаты: {total_cost:.2f} руб.")


company = Company("TechInnovations")
# Создание отделов
dev_department = Department("DEV")
sales_department = Department("SAL")
# Добавление отделов в компанию
company.add_department(dev_department)
company.add_department(sales_department)
# Создание сотрудников разных типов
manager = Manager(10, "Alice Johnson", "DEV", 7000, 2000)
developer = Developer(11, "Bob Smith", "DEV", 5000, ["Python", "SQL"],
"senior")
salesperson = Saleperson(12, "Charlie Brown", "SAL", 4000, 0.15, 50000)
# Добавление сотрудников в отделы
dev_department.add_employee(manager)
dev_department.add_employee(developer)
sales_department.add_employee(salesperson)
# Создание проектов
ai_project = Project("101", "AI Platform", "Разработка AI системы", "2024-12-31", "active")
web_project = Project("102", "Web Portal", "Создание веб-портала", "2024-09-30", "planning")
# Добавление проектов в компанию
company.add_project(ai_project)
company.add_project(web_project)
# Формирование команд проектов
ai_project.add_team_member(developer)
ai_project.add_team_member(manager)
web_project.add_team_member(developer)

company.save_to_json("company_data.json")
# Загрузка компании
loaded_company = Company.load_from_json("company_data.json")
# Экспорт отчетов
company.export_employees_csv("employees_report.csv")
company.export_projects_csv("projects_report.csv")
