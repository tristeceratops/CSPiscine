from pathlib import Path
import sys

# Paths
ERROR_INJ_FILE = "ressource/SQLite/error_base.txt"
NB_COLUMN_PATTERN = "ressource/SQLite/nb_column_pattern.txt"
OUTPUT_FILE = "ressource/generate/sqlite_patterns.py"


def load_errors(file_path):
    """Read lines from a file, strip them, ignore empty lines."""
    path = Path(file_path)

    if not path.exists():
        print(f"[!] Error: File '{file_path}' does not exist.")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            errors = {line.strip().lower() for line in f if line.strip()}
            return errors
    except Exception as e:
        print(f"[!] Error reading '{file_path}': {e}")
        sys.exit(1)


def load_nb_column_patterns(file_path):
    """
    Read payload patterns of the form:
    payload | PLACEHOLDER_TYPE
    """
    path = Path(file_path)

    if not path.exists():
        print(f"[!] Error: File '{file_path}' does not exist.")
        sys.exit(1)

    patterns = []

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "|" not in line:
                    print(f"[!] Invalid pattern format: {line}")
                    continue

                payload, placeholder = line.split("|", 1)

                patterns.append({
                    "payload": payload.strip(),
                    "placeholder": placeholder.strip()
                })

        return patterns

    except Exception as e:
        print(f"[!] Error reading '{file_path}': {e}")
        sys.exit(1)


def generate_patterns(error_file, nb_column_file, output_file):
    """Generate Python module with SQLi patterns."""

    mysql_errors = load_errors(error_file)
    nb_column_patterns = load_nb_column_patterns(nb_column_file)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_path, "w", encoding="utf-8") as f:

            f.write("# Auto-generated file: SQL injection patterns\n\n")

            # Error injection payloads
            f.write("ERRORS_INJ = {\n")
            for err in mysql_errors:
                f.write(f"    {repr(err)},\n")
            f.write("}\n\n")

            # Column detection patterns
            f.write("NB_COLUMN_PATTERNS = [\n")
            for p in nb_column_patterns:
                f.write(
                    "    "
                    + repr(p)
                    + ",\n"
                )
            f.write("]\n\n")

            # Final exported object
            f.write("SQLITE_ERROR = {\n")
            f.write("    'errors': ERRORS_INJ,\n")
            f.write("    'nb_column_patterns': NB_COLUMN_PATTERNS,\n")
            f.write("}\n")

        print(f"[+] Successfully generated '{output_file}'.")

    except Exception as e:
        print(f"[!] Failed to write '{output_file}': {e}")
        sys.exit(1)


if __name__ == "__main__":
    generate_patterns(ERROR_INJ_FILE, NB_COLUMN_PATTERN, OUTPUT_FILE)

