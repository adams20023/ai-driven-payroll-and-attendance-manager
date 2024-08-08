import subprocess

def run_script(script_name):
    result = subprocess.run(['python', script_name], capture_output=True, text=True)
    print(f"Running {script_name}...")
    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_script('attendance_analysis.py')
    run_script('full_payroll_system.py')

