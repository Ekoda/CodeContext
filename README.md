# CodeContext - Project Snapshot Generator

CodeContext is a utility script designed to generate a detailed snapshot of a project's structure, dependencies, recent commits, and environment specifics. This snapshot is crafted to provide a comprehensive yet succinct overview of the project at any given point in time, aiding in effective communication with Language Models (LLMs) and team members.

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
    python path/to/context.py      # For complete snapshot (default)
    ```
5. The selected project snapshot information will be printed to the terminal.

## Configuration

- To tailor the script to your project’s specific needs, you may modify the `generate_project_snapshot` function in `context.py`.
- The root directory of your project is specified by the `root_directory` variable in the `__main__` section at the bottom of `context.py`, or it can be passed as an argument when running the script.

## Contribution

Your contributions are welcome! Feel free to fork this repository, make enhancements, and submit pull requests. For substantial changes, please open an issue first to discuss your proposed changes.