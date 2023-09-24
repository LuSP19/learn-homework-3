
"""
В этот раз у нас есть компания, в ней отделы, в отделах люди. У людей есть имя, должность и зарплата.
Ваши задачи такие:
1. Вывести названия всех отделов
2. Вывести имена всех сотрудников компании.
3. Вывести имена всех сотрудников компании с указанием отдела, в котором они работают.
4. Вывести имена всех сотрудников компании, которые получают больше 100к.
5. Вывести позиции, на которых люди получают меньше 80к (можно с повторениями).
6. Посчитать, сколько денег в месяц уходит на каждый отдел – и вывести вместе с названием отдела
Второй уровень:
7. Вывести названия отделов с указанием минимальной зарплаты в нём.
8. Вывести названия отделов с указанием минимальной, средней и максимальной зарплаты в нём.
9. Вывести среднюю зарплату по всей компании.
10. Вывести названия должностей, которые получают больше 90к без повторений.
11. Посчитать среднюю зарплату по каждому отделу среди девушек (их зовут Мишель, Николь, Кристина и Кейтлин).
12. Вывести без повторений имена людей, чьи фамилии заканчиваются на гласную букву.
Третий уровень:
Теперь вам пригодится ещё список taxes, в котором хранится информация о налогах на сотрудников из разных департаметов.
Если department None, значит, этот налог применяется ко всем сотрудникам компании.
Иначе он применяется только к сотрудникам департмента, название которого совпадает с тем, что записано по ключу department.
К одному сотруднику может применяться несколько налогов.
13. Вывести список отделов со средним налогом на сотрудников этого отдела.
14. Вывести список всех сотредников с указанием зарплаты "на руки" и зарплаты с учётом налогов.
15. Вывести список отделов, отсортированный по месячной налоговой нагрузки.
16. Вывести всех сотрудников, за которых компания платит больше 100к налогов в год.
17. Вывести имя и фамилию сотрудника, за которого компания платит меньше всего налогов.
"""

departments = [
    {
        "title": "HR department",
        "employees": [
            {"first_name": "Daniel", "last_name": "Berger", "position": "Junior HR", "salary_rub": 50000},
            {"first_name": "Michelle", "last_name": "Frey", "position": "Middle HR", "salary_rub": 75000},
            {"first_name": "Kevin", "last_name": "Jimenez", "position": "Middle HR", "salary_rub": 70000},
            {"first_name": "Nicole", "last_name": "Riley", "position": "HRD", "salary_rub": 120000},
        ]
    },
    {
        "title": "IT department",
        "employees": [
            {"first_name": "Christina", "last_name": "Walker", "position": "Python dev", "salary_rub": 80000},
            {"first_name": "Michelle", "last_name": "Gilbert", "position": "JS dev", "salary_rub": 85000},
            {"first_name": "Caitlin", "last_name": "Bradley", "position": "Teamlead", "salary_rub": 950000},
            {"first_name": "Brian", "last_name": "Hartman", "position": "CTO", "salary_rub": 130000},
        ]
    },
]

taxes = [
    {"department": None, "name": "vat", "value_percents": 13},
    {"department": "IT Department", "name": "hiring", "value_percents": 6},
    {"department": "BizDev Department", "name": "sales", "value_percents": 20},
]


def get_department_titles():
    return [department['title'] for department in departments]


def get_employee_names():
    employee_names = []

    for department in departments:
        for employee in department['employees']:
            employee_names.append(
                f'{employee["first_name"]} {employee["last_name"]}'
            )

    return employee_names


def get_employees_department():
    employees_department = {}

    for department in departments:
        for employee in department['employees']:
            employee_name = f'{employee["first_name"]} {employee["last_name"]}'
            employees_department[employee_name] = department['title']

    return employees_department


def filter_employees_by_salary(filter_mode, limit):
    passed_the_filter = []

    for department in departments:
        for employee in department['employees']:
            salary = employee['salary_rub']
            if (
                filter_mode == 'less' and salary < limit or
                filter_mode == 'greater' and salary > limit
            ):
                passed_the_filter.append(
                    f'{employee["first_name"]} {employee["last_name"]}'
                )

    return passed_the_filter


def get_departments_costs():
    departments_costs = {}

    for department in departments:
        salaries_sum = 0
        for employee in department['employees']:
            salaries_sum += employee['salary_rub']
        departments_costs[department['title']] = salaries_sum

    return departments_costs


def get_departments_min_salaries():
    departments_min_salaries = {}

    for department in departments:
        min_salary = float('inf')
        for employee in department['employees']:
            salary = employee['salary_rub']
            if salary < min_salary:
                min_salary = salary
        departments_min_salaries[department['title']] = min_salary

    return departments_min_salaries


def get_departments_stat():
    departments_stat = {}

    for department in departments:
        min_salary = float('inf')
        max_salary = 0
        salaries_sum = 0
        employees = department['employees']
        for employee in employees:
            salary = employee['salary_rub']
            if salary < min_salary:
                min_salary = salary
            if salary > max_salary:
                max_salary = salary
            salaries_sum += salary
        avg_salary = round(salaries_sum / len(employees), 2)
        departments_stat[department['title']] = [
            min_salary, max_salary, avg_salary
        ]

    return departments_stat


def get_avg_salary():
    employees_count = 0
    salaries_sum = 0

    for department in departments:
        for employee in department['employees']:
            employees_count += 1
            salaries_sum += employee['salary_rub']

    return round(salaries_sum / employees_count, 2)


def filter_positions_by_salary(filter_mode, limit):
    passed_the_filter = set()

    for department in departments:
        for employee in department['employees']:
            salary = employee['salary_rub']
            if (
                filter_mode == 'less' and salary < limit or
                filter_mode == 'greater' and salary > limit
            ):
                passed_the_filter.add(employee['position'])

    return list(passed_the_filter)


def get_departments_girl_avg_salaries():
    departments_girl_avg_salaries = {}
    girls_names = ['Michelle', 'Nicole', 'Christina', 'Caitlin']

    for department in departments:
        salaries_sum = 0
        girls_count = 0
        for employee in department['employees']:
            if employee['first_name'] in girls_names:
                salaries_sum += employee['salary_rub']
                girls_count += 1
        if salaries_sum:
            avg_salary = round(salaries_sum / girls_count, 2)
            departments_girl_avg_salaries[department['title']] = avg_salary

    return departments_girl_avg_salaries


def get_employee_names_with_certain_surnames():
    employee_names_with_certain_surnames = set()

    for department in departments:
        for employee in department['employees']:
            if employee['last_name'][-1] in 'aeiou':
                employee_names_with_certain_surnames.add(
                    employee['first_name']
                )

    return list(employee_names_with_certain_surnames)


def get_department_summary_tax_rate(department_title):
    department_summary_tax_rate = 0
    for tax in taxes:
        if tax['department'] in (department_title, None):
            department_summary_tax_rate += tax['value_percents']

    return department_summary_tax_rate


def get_departments_avg_taxes():
    departments_avg_taxes = {}

    for department in departments:
        department_title = department['title']
        department_summary_tax_rate = get_department_summary_tax_rate(
            department_title
        )
        summary_tax = 0
        employees = department['employees']
        for employee in employees:
            summary_tax += (
                employee['salary_rub'] * department_summary_tax_rate / 100
            )
        departments_avg_taxes[department_title] = round(
            summary_tax / len(employees), 2
        )

    return departments_avg_taxes


def get_employee_salaries():
    employee_salaries = {}

    for department in departments:
        department_summary_tax_rate = get_department_summary_tax_rate(
            department['title']
        )
        for employee in department['employees']:
            employee_name = f'{employee["first_name"]} {employee["last_name"]}'
            salary = employee['salary_rub']
            net_salary = (
                salary - salary * department_summary_tax_rate / 100
            )
            employee_salaries[employee_name] = [net_salary, salary]

    return employee_salaries


def get_department_summary_taxes():
    department_summary_taxes = {}

    for department in departments:
        department_title = department['title']
        department_summary_tax_rate = get_department_summary_tax_rate(
            department_title
        )
        summary_tax = 0
        employees = department['employees']
        for employee in employees:
            summary_tax += (
                employee['salary_rub'] * department_summary_tax_rate / 100
            )
        department_summary_taxes[department_title] = summary_tax

    return department_summary_taxes


def get_departments_sorted_by_summary_tax():
    department_summary_taxes = get_department_summary_taxes()
    departments_sorted_by_summary_tax = [
        pair[0] for pair
        in sorted(department_summary_taxes.items(), key=lambda x: x[1])
    ]
    return departments_sorted_by_summary_tax


def filter_employees_by_annual_tax(filter_mode, limit):
    passed_the_filter = []

    for department in departments:
        tax_rate = get_department_summary_tax_rate(department['title'])
        for employee in department['employees']:
            annual_tax = employee['salary_rub'] * tax_rate / 100 * 12
            if (
                filter_mode == 'less' and annual_tax < limit or
                filter_mode == 'greater' and annual_tax > limit
            ):
                passed_the_filter.append(
                    f'{employee["first_name"]} {employee["last_name"]}'
                )

    return passed_the_filter


def get_the_lowest_tax_employee():
    lowest_tax = float('inf')
    for department in departments:
        department_summary_tax_rate = get_department_summary_tax_rate(
            department['title']
        )
        for employee in department['employees']:
            tax = employee['salary_rub'] * department_summary_tax_rate / 100
            if tax < lowest_tax:
                lowest_tax = tax
                lowest_tax_employee = (
                    f'{employee["first_name"]} {employee["last_name"]}'
                )

    return lowest_tax_employee


def main():
    print(f'Department titles: {", ".join(get_department_titles())}')
    print(f'Employee names: {", ".join(get_employee_names())}')
    print(
        'Employees department:',
        *[
            f'\t{employee}: {department}'
            for employee, department in get_employees_department().items()
        ],
        sep='\n'
    )
    print(
        f'Employees earning more than 100k: '
        f'{", ".join(filter_employees_by_salary("greater", 100_000))}'
    )
    print(
        f'Employees earning less than 80k: '
        f'{", ".join(filter_employees_by_salary("less", 80_000))}'
    )
    print(
        'Departments costs:',
        *[
            f'\t{department}: {cost}'
            for department, cost in get_departments_costs().items()
        ],
        sep='\n'
    )
    print(
        'Departments minimum salaries:',
        *[
            f'\t{department}: {salary}'
            for department, salary in get_departments_min_salaries().items()
        ],
        sep='\n'
    )
    print(
        'Departments salary stat:',
        *[
            f'\t{department}: max: {stat[0]}, min: {stat[1]}, avg: {stat[2]}'
            for department, stat in get_departments_stat().items()
        ],
        sep='\n'
    )
    print(f'Company average salary: {get_avg_salary()}')
    print(
        f'Positions with salary greater than 90k: '
        f'{", ".join(filter_positions_by_salary("greater", 90_000))}'
    )
    print(
        'Departments girl average salaries:',
        *[
            f'\t{department}: {salary}'
            for department, salary
            in get_departments_girl_avg_salaries().items()
        ],
        sep='\n'
    )
    print(
        f'Employees with a vowel as last surname letter: '
        f'{", ".join(get_employee_names_with_certain_surnames())}'
    )
    print(
        'Departments average taxes:',
        *[
            f'\t{department}: {tax}'
            for department, tax in get_departments_avg_taxes().items()
        ],
        sep='\n'
    )
    print(
        'Employee net and gross salaries:',
        *[
            f'\t{full_name}: {salaries[0]}, {salaries[1]}'
            for full_name, salaries in get_employee_salaries().items()
        ],
        sep='\n'
    )
    print(
        f'Departments sorted by summary tax: '
        f'{", ".join(get_departments_sorted_by_summary_tax())}'
    )
    print(
        f'Employees with annual tax greater than 100k: '
        f'{", ".join(filter_employees_by_annual_tax("greater", 100_000))}'
    )
    print(f'The lowest tax employee: {get_the_lowest_tax_employee()}')


if __name__ == '__main__':
    main()
