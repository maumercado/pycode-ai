import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.prompts import PromptTemplate
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

# Create an instance of the OpenAI client
def create_openai_client(api_key):
    """
    Create and return an instance of the OpenAI client.

    Args:
        api_key (str): The OpenAI API key.

    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return OpenAI(api_key=api_key)

# Create a prompt template using LangChain
def create_prompt_template(prompt):
    """
    Create and return a LangChain PromptTemplate based on the given prompt string.

    Args:
        prompt (str): The prompt string to be used as a template.

    Returns:
        PromptTemplate: A template for generating prompts.
    """
    return PromptTemplate.from_template(prompt)

# Generate content using the OpenAI API
def generate_content(client, template, **kwargs):
    """
    Generate content using the OpenAI API.

    Args:
        client (OpenAI): An instance of the OpenAI client.
        template (PromptTemplate): A LangChain prompt template.
        **kwargs: Keyword arguments to format the template.

    Returns:
        str: The generated content.
    """
    prompt = template.format(**kwargs)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Main function to orchestrate the process
def main():
    """
    The main function that orchestrates the code generation and test generation process.
    """
    # Load the API key from environment variables
    api_key = load_environment()

    # Create an OpenAI client instance
    client = create_openai_client(api_key)

    # Define prompt strings
    code_prompt = "You are a helpful assistant that writes code. Write a very short {language} function that will {task}."
    test_prompt = "You are a helpful assistant that writes test code. Write a short test for the following {language} function:\n\n{code}\n\nProvide a test that verifies the function works as expected."

    # Create prompt templates
    code_prompt_template = create_prompt_template(code_prompt)
    test_prompt_template = create_prompt_template(test_prompt)

    # Generate function
    generated_code = generate_content(client, code_prompt_template, language=args.language, task=args.task)

    # Generate test
    test_code = generate_content(client, test_prompt_template, language=args.language, code=generated_code)

    # Prepare result
    result = {
        "language": args.language,
        "task": args.task,
        "code": generated_code,
        "test": test_code
    }

    # Print the result as a properly formatted JSON string
    print(json.dumps(result, indent=2))

# Standard boilerplate to call the main() function
if __name__ == "__main__":
    main()
