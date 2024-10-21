from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, emp_id, name, email):
        self._emp_id = emp_id
        self._name = name
        self._email = email
        self._salary = 0

    @property
    def emp_id(self):
        return self._emp_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, str) and "@" in value:
            self._email = value
        else:
            raise ValueError("Invalid email format")

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._salary = value
        else:
            raise ValueError("Salary must be a non-negative number")

    @abstractmethod
    def calculate_salary(self):
        pass

    def __str__(self):
        return f"ID: {self._emp_id}, Name: {self._name}, Email: {self._email}, Salary: ${self._salary:.2f}"


class Manager(Employee):
    def __init__(self, emp_id, name, email, base_salary, bonus_percentage):
        super().__init__(emp_id, name, email)
        self._base_salary = base_salary
        self._bonus_percentage = bonus_percentage

    @property
    def bonus_percentage(self):
        return self._bonus_percentage

    @bonus_percentage.setter
    def bonus_percentage(self, value):
        if 0 <= value <= 100:
            self._bonus_percentage = value
        else:
            raise ValueError("Bonus percentage must be between 0 and 100")

    def calculate_salary(self):
        bonus = self._base_salary * (self._bonus_percentage / 100)
        self._salary = self._base_salary + bonus


class Developer(Employee):
    def __init__(self, emp_id, name, email, base_salary, overtime_hours):
        super().__init__(emp_id, name, email)
        self._base_salary = base_salary
        self._overtime_hours = overtime_hours

    @property
    def overtime_hours(self):
        return self._overtime_hours

    @overtime_hours.setter
    def overtime_hours(self, value):
        if value >= 0:
            self._overtime_hours = value
        else:
            raise ValueError("Overtime hours must be non-negative")

    def calculate_salary(self):
        overtime_pay = self._overtime_hours * (
            self._base_salary / 160
        )  # Assuming 160 working hours per month
        self._salary = self._base_salary + overtime_pay


class SalesRepresentative(Employee):
    def __init__(self, emp_id, name, email, base_salary, commission_rate, sales_volume):
        super().__init__(emp_id, name, email)
        self._base_salary = base_salary
        self._commission_rate = commission_rate
        self._sales_volume = sales_volume

    @property
    def commission_rate(self):
        return self._commission_rate

    @commission_rate.setter
    def commission_rate(self, value):
        if 0 <= value <= 100:
            self._commission_rate = value
        else:
            raise ValueError("Commission rate must be between 0 and 100")

    @property
    def sales_volume(self):
        return self._sales_volume

    @sales_volume.setter
    def sales_volume(self, value):
        if value >= 0:
            self._sales_volume = value
        else:
            raise ValueError("Sales volume must be non-negative")

    def calculate_salary(self):
        commission = self._sales_volume * (self._commission_rate / 100)
        self._salary = self._base_salary + commission


class EmployeeManagementSystem:
    def __init__(self):
        self._employees = {}

    def add_employee(self, employee):
        if isinstance(employee, Employee):
            employee.calculate_salary()  # Calculate salary when adding employee
            self._employees[employee.emp_id] = employee
            print(f"Employee {employee.name} added successfully.")
        else:
            raise TypeError("Invalid employee type")

    def remove_employee(self, emp_id):
        if emp_id in self._employees:
            employee = self._employees.pop(emp_id)
            print(f"Employee {employee.name} removed successfully.")
        else:
            print("Employee not found.")

    def get_employee(self, emp_id):
        employee = self._employees.get(emp_id)
        if employee:
            employee.calculate_salary()  # Recalculate salary when viewing employee
        return employee

    def list_employees(self):
        for employee in self._employees.values():
            employee.calculate_salary()  # Recalculate salary for each employee
            print(employee)

    def calculate_salaries(self):
        for employee in self._employees.values():
            employee.calculate_salary()
        print("All salaries calculated.")


def get_float_input(prompt):
    while True:
        try:
            value = input(prompt)
            # Remove commas and convert to float
            return float(value.replace(",", ""))
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    ems = EmployeeManagementSystem()

    while True:
        print("\nEmployee Management System")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. View Employee")
        print("4. List All Employees")
        print("5. Calculate Salaries")
        print("6. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            emp_type = input(
                "Enter employee type (Manager/Developer/Sales Representative): "
            )
            emp_id = input("Enter employee ID: ")
            name = input("Enter employee name: ")
            email = input("Enter employee email: ")
            base_salary = get_float_input("Enter base salary: ")

            if emp_type.lower() == "manager":
                bonus_percentage = get_float_input("Enter bonus percentage: ")
                employee = Manager(emp_id, name, email, base_salary, bonus_percentage)
            elif emp_type.lower() == "developer":
                overtime_hours = get_float_input("Enter overtime hours: ")
                employee = Developer(emp_id, name, email, base_salary, overtime_hours)
            elif emp_type.lower() == "sales representative":
                commission_rate = get_float_input("Enter commission rate: ")
                sales_volume = get_float_input("Enter sales volume: ")
                employee = SalesRepresentative(
                    emp_id, name, email, base_salary, commission_rate, sales_volume
                )
            else:
                print("Invalid employee type")
                continue

            ems.add_employee(employee)
            print(employee)  # Print the employee details after adding

        elif choice == "2":
            emp_id = input("Enter employee ID to remove: ")
            ems.remove_employee(emp_id)

        elif choice == "3":
            emp_id = input("Enter employee ID to view: ")
            emp = ems.get_employee(emp_id)
            if emp:
                print(emp)
            else:
                print("Employee not found.")

        elif choice == "4":
            ems.list_employees()

        elif choice == "5":
            ems.calculate_salaries()
            ems.list_employees()  # Show the updated salaries

        elif choice == "6":
            print("Thank you for using the Employee Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
