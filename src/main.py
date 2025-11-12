# import langchain 1.0
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# define tools using the @tool decorator
@tool
def search_function(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

@tool
def calculator_function(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)  # Note: eval is unsafe for production
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating: {str(e)}"

# initialize the language model using Google GenAI
# You need to set GOOGLE_API_KEY environment variable
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",  
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# create the agent using create_agent
agent = create_agent(
    model=model,
    tools=[search_function, calculator_function],
    system_prompt="You are a helpful assistant."
)

# execute the agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "What is the capital of France and what is 2 + 2?"}]
})

print(response["messages"][-1].content)

