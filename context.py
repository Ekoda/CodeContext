import argparse
import os
import subprocess
import platform
import json
import fnmatch
import xml.etree.ElementTree as ET

def get_gitignore_patterns(rootdir):
    gitignore_path = os.path.join(rootdir, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as file:
            return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return []

def is_ignored(path, ignore_patterns):
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
        if fnmatch.fnmatch(os.path.basename(path), pattern):
            return True
    return False

def get_directory_structure(rootdir, ignore_patterns=[], prefix="", is_last=False):
    dir_structure = []
    explicit_ignore = ['.git', '__pycache__', 'venv', 'env', 'target', '.mvn', 'logs', '*.log', '.next', 'node_modules', '.vercel', 'out', '.idea', '.DS_Store', '.vscode', '*.swp', '*.swo', '*.bak', '*.pyi']
    
    dirnames = [d for d in os.listdir(rootdir) if os.path.isdir(os.path.join(rootdir, d)) and not d.startswith('.')]
    dirnames[:] = [d for d in dirnames if not is_ignored(os.path.join(rootdir, d), ignore_patterns + explicit_ignore)]
    
    filenames = [f for f in os.listdir(rootdir) if os.path.isfile(os.path.join(rootdir, f))]
    filenames[:] = [f for f in filenames if not is_ignored(os.path.join(rootdir, f), ignore_patterns)]
    
    all_names = dirnames + filenames
    all_names.sort()

    if prefix:
        dir_structure.append(f"{prefix}{'└── ' if is_last else '├── '}{os.path.basename(rootdir)}")

    for i, name in enumerate(all_names):
        is_last_item = i == len(all_names) - 1
        new_prefix = f"{prefix}{'    ' if is_last else '│   '}"
        
        if name in filenames:
            dir_structure.append(f"{new_prefix}{'└── ' if is_last_item else '├── '}{name}")
        else:
            subdir_path = os.path.join(rootdir, name)
            dir_structure.extend(get_directory_structure(subdir_path, ignore_patterns, new_prefix, is_last_item))
    
    return dir_structure


def get_dependencies(rootdir):
    """Gets project dependencies in a compact form."""
    dependencies = {}

    # Python
    requirements_path = os.path.join(rootdir, 'requirements.txt')
    if os.path.exists(requirements_path):
        encodings = ['utf-8', 'utf-16']  # extend this list as needed
        for encoding in encodings:
            try:
                with open(requirements_path, 'r', encoding=encoding) as file:
                    python_deps = [line.strip().split('==')[0] for line in file if line.strip()]
                    dependencies['Python'] = ', '.join(python_deps)
                    break
            except UnicodeDecodeError:
                continue 

    # Java
    pom_path = os.path.join(rootdir, 'pom.xml')
    if os.path.exists(pom_path):
        tree = ET.parse(pom_path)
        root = tree.getroot()
        namespace = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
        java_deps = [element.text for element in root.findall('.//mvn:artifactId', namespace)]
        dependencies['Java'] = ', '.join(java_deps)

    # JavaScript/TypeScript
    package_path = os.path.join(rootdir, 'package.json')
    if os.path.exists(package_path):
        with open(package_path, 'r') as file:
            package_json = json.load(file)
            js_deps = list(package_json.get('dependencies', {}).keys())
            dependencies['JavaScript/TypeScript'] = ', '.join(js_deps)

    return dependencies

def get_recent_commits():
    """Gets the 5 most recent commits."""
    result = subprocess.run(['git', 'log', '--oneline', '-n', '5'], stdout=subprocess.PIPE, text=True)
    return result.stdout

def get_command_output(command):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True, universal_newlines=True)
        return output.strip()
    except subprocess.CalledProcessError as e:
        return f"None"

def get_environment_details():
    """Gets basic environment details like OS, Python, Java, Node.js and TypeScript versions."""
    details = {}
    # OS Info
    os_info = f"{platform.system()} {platform.release()}"
    details['OS Info'] = os_info
    
    # Python
    python_version = platform.python_version()
    if python_version:
        details['Python Version'] = python_version
    
    # Java
    java_version = get_command_output("java -version")
    if java_version:
        details['Java Version'] = java_version
    
    # Node.js
    node_version = get_command_output("node -v")
    if node_version:
        details['Node.js Version'] = node_version
    
    # TypeScript
    typescript_version = get_command_output("tsc -v")
    if typescript_version:
        details['TypeScript Version'] = typescript_version

    return details

def get_llm_info(rootdir):
    readme_path = os.path.join(rootdir, 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as file:
            content = file.read()
            llm_start = content.find('<!--LLM-->')
            llm_end = content.find('<!--LLM-->', llm_start + 1)
            if llm_start != -1 and llm_end != -1:
                llm_info = content[llm_start + len('<!--LLM-->'): llm_end].strip()
                return llm_info
    return None

def main():
    parser = argparse.ArgumentParser(description='Generate project snapshot.')
    parser.add_argument('command', nargs='?', default='all', choices=['dir', 'env', 'llm', 'all'], help='Command to execute. Choose "dir" for directory structure, "llm" for project details, "env" for environment details, or "all" for complete snapshot.')
    parser.add_argument('rootdir', nargs='?', default='.', help='Root directory of the project (optional, default is current directory).')
    args = parser.parse_args()

    print("---")
    print("The following project information is generated by a script and is included in the conversation for contextual purposes.")
    print(f"Project:\n{os.path.basename(os.path.abspath(args.rootdir))}\n")
    
    if args.command == 'llm' or args.command == 'all':
        llm_info = get_llm_info(args.rootdir)
        if llm_info:
            print(f"Project Context:\n{llm_info}\n")

    if args.command == 'dir' or args.command == 'all':
        dir_structure = get_directory_structure(args.rootdir, get_gitignore_patterns(args.rootdir))
        dir_structure_str = '\n'.join(dir_structure)
        print(f"Directory Structure:\n{dir_structure_str}\n")

    if args.command == 'env' or args.command == 'all':
        print(f"Environment Details:\n{get_environment_details()}\n")

    if args.command == 'all':
        print(f"Dependencies:\n{get_dependencies(args.rootdir)}\n")
        print(f"Recent Commits:\n{get_recent_commits()}\n")

    print("---")

if __name__ == "__main__":
    main()