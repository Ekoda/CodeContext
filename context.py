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
    return any(fnmatch.fnmatch(path, pattern) for pattern in ignore_patterns)

def get_directory_structure(rootdir):
    """Gets the directory structure starting from rootdir, excluding certain files/folders."""
    dir_structure = []
    ignore_patterns = get_gitignore_patterns(rootdir)
    for dirpath, dirnames, filenames in os.walk(rootdir):
        dirnames[:] = [d for d in dirnames if not is_ignored(d, ignore_patterns)]
        filenames[:] = [f for f in filenames if not is_ignored(f, ignore_patterns)]
        
        if '.git' in dirnames:
            dirnames.remove('.git')  
        if '__pycache__' in dirnames:
            dirnames.remove('__pycache__')
        
        structure = f"{dirpath}\n"
        structure += '\n'.join([f"|-- {file}" for file in filenames if not file.endswith(('.gitignore',))])
        dir_structure.append(structure)
    return '\n'.join(dir_structure)

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

def main():
    parser = argparse.ArgumentParser(description='Generate project snapshot.')
    parser.add_argument('--command', default='all', choices=['dir', 'env', 'all'], help='Command to execute. Choose "dir" for directory structure, "env" for environment details, or "all" for complete snapshot.')
    parser.add_argument('rootdir', nargs='?', default='.', help='Root directory of the project (optional, default is current directory).')
    args = parser.parse_args()

    print(f"Project:\n{os.path.basename(os.path.abspath(args.rootdir))}\n")

    if args.command == 'dir' or args.command == 'all':
        print(f"Directory Structure:\n{get_directory_structure(args.rootdir)}\n")

    if args.command == 'env' or args.command == 'all':
        print(f"Environment Details:\n{get_environment_details()}\n")

    if args.command == 'all':
        print(f"Dependencies:\n{get_dependencies(args.rootdir)}\n")
        print(f"Recent Commits:\n{get_recent_commits()}\n")

if __name__ == "__main__":
    main()