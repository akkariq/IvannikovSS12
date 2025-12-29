# tests/test_part4_composition.py
"""
Тесты для части 4: Композиция

Тестирует:
- Управление проектами
- Управление компанией
- Управление отделами
- Обработку ошибок
"""

import pytest
from source_code import (
    Employee,
    Manager,
    Developer,
    Department,
    Project,
    Company
)


class TestProjectManagement:
    """Тесты управления проектами"""
    
    def test_project_creation(self):
        """Test: Создание проекта"""
        proj = Project(1, "AI Platform", "Development", "2024-12-31")
        
        assert proj.project_id == 1
        assert proj.name == "AI Platform"
        assert proj.status == "Development"
    
    def test_project_add_team_member(self):
        """Test: Добавление члена команды"""
        proj = Project(1, "Test", "Development", "2024-12-31")
        emp = Employee(1, "John", "DEV", 5000)
        
        proj.add_team_member(emp)
        assert proj.get_team_size() == 1
    
    def test_project_team_salary(self):
        """Test: Зарплата команды проекта"""
        proj = Project(1, "Test", "Development", "2024-12-31")
        emp1 = Employee(1, "A", "DEV", 5000)
        emp2 = Employee(2, "B", "DEV", 6000)
        
        proj.add_team_member(emp1)
        proj.add_team_member(emp2)
        
        assert proj.calculate_team_salary() == 11000
    
    def test_project_status_change(self):
        """Test: Изменение статуса проекта"""
        proj = Project(1, "Test", "Development", "2024-12-31")
        proj.change_status("Testing")
        assert proj.status == "Testing"


class TestCompanyManagement:
    """Тесты управления компанией"""
    
    def test_company_hire_employee(self):
        """Test: Найм сотрудника"""
        company = Company("TechCorp")
        emp = Employee(1, "John", "IT", 5000)
        
        company.hire_employee(emp)
        assert company.get_employee_count() == 1
    
    def test_company_calculate_total_salary(self):
        """Test: Общая зарплата компании"""
        company = Company("TechCorp")
        emp1 = Employee(1, "A", "IT", 5000)
        emp2 = Manager(2, "B", "MGMT", 5000, 1000)
        
        company.hire_employee(emp1)
        company.hire_employee(emp2)
        
        assert company.calculate_total_salary() == 11000
    
    def test_company_add_department(self):
        """Test: Добавление отдела"""
        company = Company("TechCorp")
        dept = Department("IT")
        
        company.add_department(dept)
        assert company.get_department_count() == 1
    
    def test_company_find_employee(self):
        """Test: Поиск сотрудника"""
        company = Company("TechCorp")
        emp = Employee(1, "John", "IT", 5000)
        company.hire_employee(emp)
        
        found = company.find_employee_by_id(1)
        assert found.name == "John"
    
    def test_company_find_nonexistent_employee(self):
        """Test: Поиск несуществующего сотрудника"""
        company = Company("TechCorp")
        found = company.find_employee_by_id(999)
        assert found is None
    
    def test_company_add_project(self):
        """Test: Добавление проекта"""
        company = Company("TechCorp")
        proj = Project(1, "Test", "Development", "2024-12-31")
        
        company.add_project(proj)
        assert company.get_project_count() == 1


class TestDepartmentManagement:
    """Тесты управления отделами"""
    
    def test_department_add_employee(self):
        """Test: Добавление сотрудника в отдел"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        assert len(dept) == 1
    
    def test_department_calculate_salary(self):
        """Test: Общая зарплата отдела"""
        dept = Department("IT")
        emp1 = Employee(1, "A", "IT", 5000)
        emp2 = Employee(2, "B", "IT", 6000)
        
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        assert dept.calculate_total_salary() == 11000
    
    def test_department_employee_count_by_type(self):
        """Test: Статистика по типам"""
        dept = Department("IT")
        emp = Employee(1, "A", "IT", 5000)
        dev = Developer(2, "B", "IT", 5000, ["Python"], "senior")
        
        dept.add_employee(emp)
        dept.add_employee(dev)
        
        stats = dept.get_employee_count()
        assert stats["Employee"] == 1
        assert stats["Developer"] == 1
    
    def test_department_remove_employee(self):
        """Test: Удаление сотрудника"""
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        
        dept.remove_employee(emp.id)
        assert len(dept) == 0