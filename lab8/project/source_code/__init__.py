# source_code/__init__.py
"""Пакет с исходным кодом Lab08-Testing"""

__version__ = "1.0.0"

# Импорты с обработкой ошибок - импортируем что существует

try:
    from source_code.part1 import Employee
except ImportError:
    Employee = None

try:
    from source_code.part2 import AbstractEmployee
except ImportError:
    AbstractEmployee = None

try:
    from source_code.part2 import Manager
except ImportError:
    Manager = None

try:
    from source_code.part2 import Developer
except ImportError:
    Developer = None

try:
    from source_code.part2 import Salesperson
except ImportError:
    Salesperson = None

try:
    from source_code.part2 import EmployeeFactory
except ImportError:
    EmployeeFactory = None

try:
    from source_code.part3 import Department
except ImportError:
    Department = None

try:
    from source_code.part4 import Project
except ImportError:
    Project = None

try:
    from source_code.part4 import Company
except ImportError:
    Company = None

try:
    from source_code.part4 import InvalidStatusError
except ImportError:
    InvalidStatusError = None

try:
    from source_code.part4 import DepartmentNotEmpty
except ImportError:
    DepartmentNotEmpty = None

try:
    from source_code.sourcecode import DatabaseConnection
except ImportError:
    DatabaseConnection = None

try:
    from source_code.sourcecode import EmployeeBuilder
except ImportError:
    EmployeeBuilder = None

try:
    from source_code.sourcecode import SalaryAdapter
except ImportError:
    SalaryAdapter = None

try:
    from source_code.sourcecode import BonusDecorator
except ImportError:
    BonusDecorator = None

try:
    from source_code.sourcecode import EmployeeRepository
except ImportError:
    EmployeeRepository = None

try:
    from source_code.sourcecode import EmployeeSpecification
except ImportError:
    EmployeeSpecification = None

# Экспортируем только существующие классы
__all__ = [
    name for name in [
        "Employee",
        "AbstractEmployee",
        "Manager",
        "Developer",
        "Salesperson",
        "EmployeeFactory",
        "Department",
        "Project",
        "Company",
        "InvalidStatusError",
        "DepartmentNotEmpty",
        "DatabaseConnection",
        "EmployeeBuilder",
        "SalaryAdapter",
        "BonusDecorator",
        "EmployeeRepository",
        "EmployeeSpecification",
    ]
    if globals().get(name) is not None
]
