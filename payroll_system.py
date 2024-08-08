import pandas as pd
import datetime
from dateutil import parser

# Constants
WORK_HOURS_PER_DAY = 8

def load_data():
    """Load attendance and employee data."""
    attendance_df = pd.read_csv('attendance.csv')
    employees_df = pd.read_csv('employees.csv')
    return attendance_df, employees_df

def calculate_hours(row):
    """Calculate the total hours worked by an employee in a day."""
    clock_in = parser.parse(row['ClockIn'])
    clock_out = parser.parse(row['ClockOut'])
    worked_hours = (clock_out - clock_in).seconds / 3600
    return worked_hours

def generate_payroll(attendance_df):
    """Generate payroll report based on attendance data."""
    payroll_report = []
    for employee_id, group in attendance_df.groupby('EmployeeID'):
        total_hours = group.apply(calculate_hours, axis=1).sum()
        expected_hours = len(group) * WORK_HOURS_PER_DAY
        absences = max(0, expected_hours - total_hours)
        payroll_report.append({
            'EmployeeID': employee_id,
            'TotalHours': total_hours,
            'ExpectedHours': expected_hours,
            'Absences': absences
        })
    return pd.DataFrame(payroll_report)

def save_payroll_report(payroll_df):
    """Save the payroll report to a CSV file."""
    payroll_df.to_csv('payroll_report.csv', index=False)
    print("Payroll report generated successfully!")

if __name__ == '__main__':
    attendance_df, employees_df = load_data()
    payroll_df = generate_payroll(attendance_df)
    save_payroll_report(payroll_df)

