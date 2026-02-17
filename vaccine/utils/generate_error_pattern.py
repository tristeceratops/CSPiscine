from pathlib import Path
import sys

# Paths to your input error text files
MYSQL_FILE = "ressource/Mysql/errors_message.txt"
SQLITE_FILE = "ressource/SQLite/errors_message.txt"
OUTPUT_FILE = "ressource/generate/error_patterns.py"


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


def generate_error_patterns(mysql_file, sqlite_file, output_file):
    """Generate a Python file defining error patterns for MySQL and SQLite."""
    mysql_errors = load_errors(mysql_file)
    sqlite_errors = load_errors(sqlite_file)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Auto-generated file: error patterns for SQL detection\n\n")

            # Write MySQL errors
            f.write("MYSQL_ERRORS = {\n")
            for err in sorted(mysql_errors):
                f.write(f'    "{err}",\n')
            f.write("}\n\n")

            # Write SQLite errors
            f.write("SQLITE_ERRORS = {\n")
            for err in sorted(sqlite_errors):
                f.write(f'    "{err}",\n')
            f.write("}\n\n")

            # Combine into a single dict
            f.write("ERROR_PATTERNS = {\n")
            f.write("    'mysql': MYSQL_ERRORS,\n")
            f.write("    'sqlite': SQLITE_ERRORS,\n")
            f.write("}\n")

        print(f"[+] Successfully generated '{output_file}'.")
    except Exception as e:
        print(f"[!] Failed to write '{output_file}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_error_patterns(MYSQL_FILE, SQLITE_FILE, OUTPUT_FILE)

