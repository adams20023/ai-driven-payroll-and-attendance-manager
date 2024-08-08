import pandas as pd
import openai

# Configure your OpenAI API key
openai.api_key = 'openai.api_key'

def calculate_payroll(attendance_df, employee_df):
    # Merge attendance and employee data
    payroll_df = pd.merge(attendance_df, employee_df, on='Employee_ID', how='left')
    
    # Calculate hours worked
    payroll_df['Clock_In'] = pd.to_datetime(payroll_df['Clock_In'])
    payroll_df['Clock_Out'] = pd.to_datetime(payroll_df['Clock_Out'])
    payroll_df['Hours_Worked'] = (payroll_df['Clock_Out'] - payroll_df['Clock_In']).dt.total_seconds() / 3600
    
    # Calculate pay, tax, and national insurance
    payroll_df['Pay'] = payroll_df['Hours_Worked'] * payroll_df['Hourly_Rate']
    payroll_df['Tax'] = payroll_df['Pay'] * payroll_df['Tax_Rate']
    payroll_df['NI'] = payroll_df['Pay'] * payroll_df['NI_Rate']
    payroll_df['Net_Pay'] = payroll_df['Pay'] - payroll_df['Tax'] - payroll_df['NI']
    
    return payroll_df[['Employee_ID', 'Name', 'Position', 'Hours_Worked', 'Pay', 'Tax', 'NI', 'Net_Pay']]

def generate_report(payroll_df):
    prompt = "Generate a detailed payroll report based on the following summarized data:\n\n"
    
    # Summarize the data
    summary = payroll_df.describe(include='all').to_csv()  # Generate summary statistics
    prompt += summary
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"An error occurred while generating the report: {e}")
        return "Failed to generate the report."

def process_payroll(attendance_file, employee_file):
    try:
        attendance_df = pd.read_csv(attendance_file)
        employee_df = pd.read_csv(employee_file)
        
        if attendance_df.empty or employee_df.empty:
            print("One or both of the data files are empty.")
            return
        
        # Check for required columns
        required_attendance_columns = {'Employee_ID', 'Date', 'Clock_In', 'Clock_Out'}
        if not required_attendance_columns.issubset(attendance_df.columns):
            print("Attendance data is missing required columns.")
            return
        
        required_employee_columns = {'Employee_ID', 'Name', 'Position', 'Hourly_Rate', 'Tax_Rate', 'NI_Rate'}
        if not required_employee_columns.issubset(employee_df.columns):
            print("Employee data is missing required columns.")
            return
        
        # Calculate payroll
        payroll_df = calculate_payroll(attendance_df, employee_df)
        
        # Generate report
        report = generate_report(payroll_df)
        print("Payroll Report Generated")
        print(report)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except pd.errors.EmptyDataError:
        print("Error: One or more data files are empty.")
    except pd.errors.ParserError:
        print("Error: Could not parse one or more data files.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    attendance_file = 'attendance.csv'
    employee_file = 'employees.csv'
    process_payroll(attendance_file, employee_file)

