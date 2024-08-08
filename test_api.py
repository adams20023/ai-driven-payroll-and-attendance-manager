import openai

# Configure your OpenAI API key
openai.api_key = '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'

def test_openai_api():
    try:
        response = openai.Completion.create(
            model="gpt-4",  # Use GPT-4 model
            prompt="Test the API.",
            max_tokens=50
        )
        print(response.choices[0].text.strip())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_openai_api()

