# CodeContext - Project Snapshot Generator

CodeContext is a utility script designed to generate a detailed snapshot of a project's structure, dependencies, recent commits, and environment specifics. This snapshot is crafted to provide a comprehensive yet succinct overview of the project at any given point in time, aiding in effective communication with Language Models (LLMs) and team members.

This script marks an interesting point in tech history. Right now, Language Learning Models (LLMs), despite being quite powerful, still need a human touch to do well in the engineering domain. I suspect these models will grow in autonomy and eventually not need my input at all. Only time will tell.

## Features

- **Directory Structure**: Generates a tree-like representation of your project’s file structure, filtering out specified files and directories (e.g., `.git`, `__pycache__`, and items listed in `.gitignore`).
- **Dependencies**: Enumerates project dependencies for Python, Java, and JavaScript/TypeScript, as applicable.
- **Recent Commits**: Retrieves the 5 most recent commits from the project's git history.
- **Environment Details**: Captures basic environment details like OS and version information for Python, Java, Node.js, and TypeScript.

## Usage

1. Ensure Python 3.6 or later is installed on your machine.
2. Clone this repository or download the script `context.py`.
3. Navigate to your project's root directory in the terminal.
4. Run the script from your project's root directory using one of the following commands based on the information you wish to generate:
    ```bash
    python path/to/context.py dir  # For Directory Structure
    python path/to/context.py env  # For Environment Details
    python path/to/context.py llm  # For Context Details (requires LLM tag in readme)
    python path/to/context.py      # For complete snapshot (default)
    ```
5. The selected project snapshot information will be printed to the terminal.

For simplicity I recommend setting a bash alias for the script, so you can grab the context anywhere easily.

## LLM Tag Usage

The LLM tag is specifically designed to encapsulate project context for Language Models (LLMs). By delineating information such as the objectives and challenges of the project within the LLM tags, you provide a structured narrative that can help LLMs better understand the project’s context. This is particularly useful when initiating conversations with LLMs, ensuring they have the necessary background to provide insightful responses.

You can even include code snippets and instructions for how you prefer to code.

To incorporate the LLM tag in your project:
- Enclose the relevant project context information within `<!--LLM-->` tags in your README file.

## Contribution

Your contributions are welcome! Feel free to fork this repository, make enhancements, and submit pull requests. For substantial changes, please open an issue first to discuss your proposed changes.

## Project Context
<!--LLM-->
### Objectives:
- Automate project snapshot generation for enhanced team and LLM communication.

### Challenges:
- Accurate cross-language dependency enumeration.
- Readable directory structure representation.
<!--LLM-->
