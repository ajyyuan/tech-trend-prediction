import os

def print_directory_structure(path, gitignore_path):
    with open(gitignore_path) as f:
        gitignore = set(line.strip() for line in f if line.strip() and not line.startswith('#'))
    
    for root, dirs, files in os.walk(path):
        # Filter out directories and files starting with '.'
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        files = [f for f in files if not f.startswith('.')]
        
        # Determine the level of indentation
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        # Skip directories that are in the gitignore
        if any(ignored in root for ignored in gitignore):
            continue
        
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        
        for f in files:
            # Skip files that are in the gitignore
            if f not in gitignore and not any(ignored in os.path.join(root, f) for ignored in gitignore):
                print('{}{}'.format(subindent, f))

print_directory_structure(".", ".gitignore")