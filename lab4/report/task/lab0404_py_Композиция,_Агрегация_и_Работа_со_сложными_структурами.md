### **Часть 4: Композиция, Агрегация и Работа со сложными структурами**

**Цель:** Освоить принципы композиции и агрегации для построения сложных объектных структур. Реализовать механизмы управления связями между объектами, валидации данных и комплексной сериализации/десериализации системы.

**Задание:**

**4.1. Система проектов и композиция**
1.  Создайте класс `Project` (Проект) с атрибутами:
    *   `project_id: int` - уникальный идентификатор проекта
    *   `name: str` - название проекта
    *   `description: str` - описание проекта
    *   `deadline: datetime` - срок выполнения проекта
    *   `status: str` - статус проекта ("planning", "active", "completed", "cancelled")
    *   `__team: list[AbstractEmployee]` - список сотрудников, работающих над проектом (**композиция**)

2.  Реализуйте в классе `Project`:
    *   `__init__()` с валидацией входных данных
    *   `add_team_member(employee: AbstractEmployee) -> None` - добавление сотрудника в проект
    *   `remove_team_member(employee_id: int) -> None` - удаление сотрудника по ID
    *   `get_team() -> list[AbstractEmployee]` - получение списка команды
    *   `get_team_size() -> int` - получение размера команды
    *   `calculate_total_salary() -> float` - расчет суммарной зарплаты команды
    *   `get_project_info() -> str` - полная информация о проекте
    *   `change_status(new_status: str) -> None` - изменение статуса с валидацией

**4.2. Класс Company и агрегация**
1.  Создайте класс `Company` (Компания) с атрибутами:
    *   `name: str` - название компании
    *   `__departments: list[Department]` - список отделов (**агрегация**)
    *   `__projects: list[Project]` - список проектов (**агрегация**)

2.  Реализуйте в классе `Company`:
    *   Методы управления отделами: `add_department()`, `remove_department()`, `get_departments()`
    *   Методы управления проектами: `add_project()`, `remove_project()`, `get_projects()`
    *   `get_all_employees() -> list[AbstractEmployee]` - получение всех сотрудников компании
    *   `find_employee_by_id(employee_id: int) -> Optional[AbstractEmployee]` - поиск сотрудника по ID
    *   `calculate_total_monthly_cost() -> float` - расчет общих месячных затрат на зарплаты
    *   `get_projects_by_status(status: str) -> list[Project]` - фильтрация проектов по статусу

**4.3. Система валидации и исключения**
1.  Создайте кастомные исключения:
    *   `EmployeeNotFoundError`
    *   `DepartmentNotFoundError`
    *   `ProjectNotFoundError`
    *   `InvalidStatusError`
    *   `DuplicateIdError`

2.  Реализуйте комплексную валидацию:
    *   Проверка уникальности ID сотрудников и проектов
    *   Валидация статусов проектов
    *   Проверка корректности дат
    *   Валидация финансовых показателей

**4.4. Управление зависимостями и связями**
1.  Реализуйте механизм проверки перед удалением:
    *   Нельзя удалить отдел, если в нем есть сотрудники
    *   Нельзя удалить сотрудника, если он участвует в проектах
    *   Нельзя удалить проект, если над ним работает команда

2.  Реализуйте методы для переноса сотрудников между отделами

**4.5. Расширенная сериализация и сохранение состояния**
1.  Реализуйте полную сериализацию всей компании в JSON:
    *   Сохранение всех отделов, сотрудников и проектов
    *   Сохранение связей между объектами
    *   Обработка циклических ссылок

2.  Реализуйте загрузку компании из JSON:
    *   Восстановление объектной структуры
    *   Восстановление связей между объектами
    *   Валидация загружаемых данных

3.  Реализуйте экспорт данных в различные форматы:
    *   CSV отчет по сотрудникам с детальной информацией
    *   CSV отчет по проектам с составом команд и бюджетами
    *   Текстовый отчет по финансовым показателям компании

**4.6. Комплексные бизнес-методы**
1.  Реализуйте методы для анализа данных:
    *   `get_department_stats() -> dict` - статистика по отделам
    *   `get_project_budget_analysis() -> dict` - анализ бюджетов проектов
    *   `find_overloaded_employees() -> list[AbstractEmployee]` - поиск перегруженных сотрудников

2.  Реализуйте методы для планирования:
    *   `assign_employee_to_project(employee_id: int, project_id: int) -> bool`
    *   `check_employee_availability(employee_id: int) -> bool`

**4.7. Тестирование и демонстрация**
В основной программе продемонстрируйте:

1.  **Создание комплексной структуры:**
    ```python
    # Создание компании
    company = Company("TechInnovations")
    
    # Создание отделов
    dev_department = Department("Development", "DEV")
    sales_department = Department("Sales", "SAL")
    
    # Добавление отделов в компанию
    company.add_department(dev_department)
    company.add_department(sales_department)
    
    # Создание сотрудников разных типов
    manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
    developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
    salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
    
    # Добавление сотрудников в отделы
    dev_department.add_employee(manager)
    dev_department.add_employee(developer)
    sales_department.add_employee(salesperson)
    
    # Создание проектов
    ai_project = Project(101, "AI Platform", "Разработка AI системы", "2024-12-31", "active")
    web_project = Project(102, "Web Portal", "Создание веб-портала", "2024-09-30", "planning")
    
    # Добавление проектов в компанию
    company.add_project(ai_project)
    company.add_project(web_project)
    
    # Формирование команд проектов
    ai_project.add_team_member(developer)
    ai_project.add_team_member(manager)
    web_project.add_team_member(developer)
    ```

2.  **Работу с композицией и агрегацией:**
    *   Покажите разницу в жизненном цикле объектов
    *   Демонстрацию управления связями

3.  **Валидацию и обработку ошибок:**
    *   Попытку добавить дубликат ID
    *   Попытку невалидного изменения статуса
    *   Попытку удаления занятого отдела

4.  **Сериализацию и экспорт:**
    ```python
    # Сохранение всей компании
    company.save_to_json("company_data.json")
    
    # Загрузка компании
    loaded_company = Company.load_from_json("company_data.json")
    
    # Экспорт отчетов
    company.export_employees_csv("employees_report.csv")
    company.export_projects_csv("projects_report.csv")
    ```

5.  **Анализ данных:**
    *   Получение статистики по компании
    *   Расчет финансовых показателей
    *   Поиск и анализ различных сущностей

**Требования к коду:**
*   Четкое разделение композиции и агрегации
*   Полноценная валидация всех операций
*   Корректная обработка исключительных ситуаций
*   Полный цикл сериализации/десериализации
*   Генерация содержательных отчетов

**Критерии оценки части 4:**
*   **Удовлетворительно:** Реализованы базовые классы Project и Company с основными методами
*   **Хорошо:** Реализована валидация данных, основные механизмы управления связями
*   **Отлично:** Полная сериализация/десериализация, комплексные бизнес-методы, генерация отчетов, демонстрация работы всей системы. Составлена UML-диаграмма классов https://plantuml.com/ru/