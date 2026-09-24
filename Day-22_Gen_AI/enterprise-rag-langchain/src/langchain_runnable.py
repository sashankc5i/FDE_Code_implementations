from langchain_model import model
from langchain_prompt import prompt


# Build a Runnable pipeline
chain = (
    prompt
    | model
)


# Input to the pipeline
input_data = {
    "context": """
HTTP 401 errors can occur because of expired tokens,
invalid tokens, incorrect token audiences,
or incorrect authentication configuration.
""",
    "question": "What are common causes of HTTP 401 errors?"
}


# Execute the pipeline
response = chain.invoke(input_data)


print("\n========== RUNNABLE PIPELINE ==========")
print(response.content)