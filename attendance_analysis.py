import pandas as pd
import openai

# Configure your OpenAI API key
openai.api_key = 'openai.api_key'

# List of models to try
models = ["gpt-3.5-turbo"]

def analyze_data(dataframe):
    prompt = "Analyze the following attendance data:\n\n"
    
    # Convert DataFrame to a summary or a smaller snippet
    summary = dataframe.head(5).to_csv(index=False)  # Limit to first 5 rows for simplicity
    prompt += summary
    
    for model in models:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue  # Try the next model in the list
    return "All models failed."

def process_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Columns in DataFrame:", df.columns)
        if df.empty:
            print("The data file is empty.")
            return
        
        # Ensure required columns are present
        required_columns = {'Employee_ID', 'Date', 'Clock_In', 'Clock_Out'}
        if not required_columns.issubset(df.columns):
            print("Data is missing required columns.")
            return

        # Convert Clock_In and Clock_Out to datetime
        df['Clock_In'] = pd.to_datetime(df['Clock_In'])
        df['Clock_Out'] = pd.to_datetime(df['Clock_Out'])
        
        # Check for any missing data
        if df.isnull().any().any():
            print("Data contains missing values.")
            return
        
        # Generate analysis
        analysis = analyze_data(df)
        print("Analysis Result:", analysis)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"Error: No data in file: {file_path}")
    except pd.errors.ParserError:
        print(f"Error: Could not parse file: {file_path}")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    file_path = 'attendance.csv'  # Path to your attendance data file
    process_data(file_path)

