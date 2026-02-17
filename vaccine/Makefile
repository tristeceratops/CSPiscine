UTIL_DIR := utils
RESSOURCE_DIR := ressource
GENERATE_DIR := generate
RESSOURCE_PATTERN_FILE := error_patterns.py

RESSOURCE_PATTERN_PATH := $(RESSOURCE_DIR)/$(GENERATE_DIR)/$(RESSOURCE_PATTERN_FILE)

all: $(RESSOURCE_PATTERN_PATH)

$(RESSOURCE_PATTERN_PATH): $(RESSOURCE_DIR)/Mysql/errors_message.txt $(RESSOURCE_DIR)/SQLite/errors_message.txt
	@echo "[*] Generating error patterns..."
	python3 $(UTIL_DIR)/generate_error_pattern.py
	@echo "[+] Done."
