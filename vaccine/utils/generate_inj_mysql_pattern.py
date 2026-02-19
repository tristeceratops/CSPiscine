from pathlib import Path
import sys

# Paths to your input error text files
ERROR_INJ_FILE = "ressource/Mysql/error_base.txt"
OUTPUT_FILE = "ressource/generate/mysql_patterns.py"


def load_errors(file_path):
    """Read lines from a file, strip them, ignore empty lines, convert to lowercase."""
    path = Path(file_path)
    if not path.exists():
        print(f"[!] Error: File '{file_path}' does not exist.")
        sys.exit(1)
    if not path.is_file():
        print(f"[!] Error: '{file_path}' is not a regular file.")
        sys.exit(1)
    if not path.stat().st_size:
        print(f"[!] Warning: File '{file_path}' is empty.")

    try:
        with open(path, "r", encoding="utf-8") as f:
            errors = {line.strip().lower() for line in f if line.strip()}
            if not errors:
                print(f"[!] Warning: No valid error patterns found in '{file_path}'.")
            return errors
    except Exception as e:
        print(f"[!] Error reading '{file_path}': {e}")
        sys.exit(1)


def generate_error_patterns(mysql_file, output_file):
    """Generate a Python file defining error patterns for MySQL and SQLite."""
    mysql_errors = load_errors(mysql_file)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated file: error injection for MySQL detection\n\n")

            # Write MySQL errors
            f.write("ERRORS_INJ = {\n")
            for err in mysql_errors:
                f.write('    ' + repr(err) + ',\n')
            f.write("}\n\n")

            # Combine into a single dict
            f.write("MYSQL_ERROR = {\n")
            f.write("    'errors': ERRORS_INJ,\n")
            f.write("}\n")

        print(f"[+] Successfully generated '{output_file}'.")
    except Exception as e:
        print(f"[!] Failed to write '{output_file}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_error_patterns(ERROR_INJ_FILE, OUTPUT_FILE)

