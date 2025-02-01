import openai

openai.api_key = "your_api_key_here"

print("Testing OpenAI API...")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
