# AI-Powered Code Generator

This project is an AI-powered code generator that creates functions and corresponding tests based on user-specified language and task requirements.

## Features

- Generates code snippets in various programming languages
- Creates corresponding test code for the generated functions
- Uses OpenAI's GPT models for code generation
- Supports custom language and task inputs via command-line arguments

## Prerequisites

- Python 3.11
- OpenAI API key

## Installation

1. Clone the repository:

   ```sh

   git clone https://github.com/yourusername/ai-code-generator.git
   cd ai-code-generator
   ```

2. Install dependencies using Pipenv:

   ```sh

   pipenv install
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:

   ```sh

   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the script using Pipenv with optional command-line arguments:
