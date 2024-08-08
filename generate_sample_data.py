import pandas as pd
import numpy as np
from faker import Faker

def generate_sample_data():
    fake = Faker()

    # Generate employee data
    num_employees = 1000
    employees = pd.DataFrame({
        'Employee_ID': [f'EMP{i:04d}' for i in range(num_employees)],
        'Name': [fake.name() for _ in range(num_employees)],
        'Position': [fake.job() for _ in range(num_employees)],
        'Hourly_Rate': np.random.uniform(15, 50, num_employees).round(2),
        'Tax_Rate': np.random.uniform(0.05, 0.20, num_employees).round(2),
        'NI_Rate': np.random.uniform(0.01, 0.05, num_employees).round(2)
    })

    # Generate attendance data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31')
    attendance = pd.DataFrame({
        'Employee_ID': np.random.choice(employees['Employee_ID'], size=num_employees * len(dates), replace=True),
        'Date': np.tile(dates, num_employees),
        'Clock_In': np.random.choice(pd.date_range(start='2024-01-01 08:00', end='2024-01-01 10:00', freq='min').strftime('%Y-%m-%d %H:%M:%S'), num_employees * len(dates)),
        'Clock_Out': np.random.choice(pd.date_range(start='2024-01-01 16:00', end='2024-01-01 20:00', freq='min').strftime('%Y-%m-%d %H:%M:%S'), num_employees * len(dates)),
    })

    # Save to CSV
    employees.to_csv('employees.csv', index=False)
    attendance.to_csv('attendance.csv', index=False)
    
if __name__ == "__main__":
    generate_sample_data()

