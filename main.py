import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI as LangChainOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--language", type=str, default="TypeScript")
parser.add_argument("--task", type=str, default="sort a list")
args = parser.parse_args()

# Load environment variables from a .env file
def load_environment():
    """
    Load the OpenAI API key from the environment variables.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()  # Load variables from .env file
    return os.getenv("OPENAI_API_KEY")  # Retrieve the API key

# Create a LangChain model instance
def create_langchain_model(api_key):
    """
    Create and return an instance of the LangChain OpenAI model.

    Args:
        api_key (str): The OpenAI API key.

    Returns:
        LangChainOpenAI: An instance of the LangChain OpenAI model.
    """
    return LangChainOpenAI(api_key=api_key, model_name="gpt-4-0125-preview")

# Main function to orchestrate the process
def main():
    """
    The main function that orchestrates the code generation and test generation process.
    """
    # Load the API key from environment variables
    api_key = load_environment()

    # Create a LangChain ChatOpenAI instance
    chat_model = create_langchain_model(api_key)

    # Define prompt templates
    code_prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant that writes code. Write a very short {language} function that will {task}."
    )
    test_prompt = ChatPromptTemplate.from_template(
        "You are a helpful assistant that writes test code. Write a short test for the following {language} function:\n\n{code}\n\nProvide a test that verifies the function works as expected."
    )

    # Create chains
    code_chain = code_prompt | chat_model | StrOutputParser()
    test_chain = test_prompt | chat_model | StrOutputParser()

    # Run the chains separately
    code_result = code_chain.invoke({
        "language": args.language,
        "task": args.task
    })

    test_result = test_chain.invoke({
        "language": args.language,
        "code": code_result
    })

    # Prepare and print result
    output = {
        "language": args.language,
        "task": args.task,
        "code": code_result,
        "test": test_result
    }
    print(json.dumps(output, indent=2))

# Standard boilerplate to call the main() function
if __name__ == "__main__":
    main()
