
# Hello World IE App Generator

## Overview

The **Hello World IE App Generator** is a Python-based interactive application that uses a Large Language Model (LLM) to generate responses to user prompts. The application is designed to provide a simple interface where users can interact with the LLM in a conversational manner.

## Prerequisites

Before running the Hello World IE App Generator, ensure you have the following installed and properly configured:

- **Python 3**: The application is written in Python, so you'll need Python 3 installed on your system.
- **Ollama**: This application relies on Ollama to handle the LLM processing. Ensure that Ollama is installed and running on your machine.
  - **Default Configuration**:
    - Ollama should be listening on port `11434`.
    - The model `gemma2:2b` should be installed.
  - **Alternative Configuration**:
    - If you prefer to use a different port or model, you can configure Ollama accordingly. However, you will need to update these settings in the `main.py` file located in the `src/` directory of this project.

## Installation

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   ```
2. **Navigate to the Project Directory**:
   ```
   cd ie-app-generation
   ```

## Configuration

If you need to change the default port or model for Ollama:

1. Open the `src/main.py` file.
2. Locate the configuration section where the port and model are specified.
3. Update the values to match your Ollama setup.

## Running the Application

To start the Hello World IE App Generator, follow these steps:

1. Ensure Ollama is running and correctly configured.
2. Run the following command from the `ie-app-generation` folder:
   ```
   python3 src/main.py
   ```

This will start the application, and you can begin interacting with the LLM.

## Usage

Once the application is running, it will prompt you to enter a query. The LLM will process your input and generate a response. The application will continue to interact with you until you type 'exit', 'quit', or 'stop'.

## License

This project is licensed under the MIT License.

