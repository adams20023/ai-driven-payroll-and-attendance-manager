def generate_report(payroll_df):
    prompt = "Generate a detailed payroll report based on the following data:\n\n"
    
    # Split DataFrame into chunks
    chunk_size = 100  # Define chunk size
    chunks = [payroll_df[i:i + chunk_size] for i in range(0, len(payroll_df), chunk_size)]
    
    full_report = ""
    
    for chunk in chunks:
        report_data = chunk.to_csv(index=False)
        prompt = f"Generate a report based on the following data:\n\n{report_data}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            full_report += response.choices[0].message['content'].strip() + "\n\n"
        except Exception as e:
            print(f"An error occurred while generating the report: {e}")
            return "Failed to generate the report."
    
    return full_report

