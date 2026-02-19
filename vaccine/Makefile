UTIL_DIR := utils
RESSOURCE_DIR := ressource
GENERATE_DIR := generate

RESSOURCE_PATTERN_FILE := error_patterns.py
RESSOURCE_MYSQL_INJ := mysql_patterns.py
RESSOURCE_SQLITE_INJ := sqlite_patterns.py

GEN_ERROR_SCRIPT := $(UTIL_DIR)/generate_error_pattern.py
GEN_MYSQL_SCRIPT := $(UTIL_DIR)/generate_inj_mysql_pattern.py
GEN_SQLITE_SCRIPT := $(UTIL_DIR)/generate_inj_sqlite_pattern.py

RESSOURCE_PATTERN_PATH := $(RESSOURCE_DIR)/$(GENERATE_DIR)/$(RESSOURCE_PATTERN_FILE)
RESSOURCE_MYSQL_INJ_PATH := $(RESSOURCE_DIR)/$(GENERATE_DIR)/$(RESSOURCE_MYSQL_INJ)
RESSOURCE_SQLITE_INJ_PATH := $(RESSOURCE_DIR)/$(GENERATE_DIR)/$(RESSOURCE_SQLITE_INJ)

all: $(RESSOURCE_PATTERN_PATH) $(RESSOURCE_MYSQL_INJ_PATH) $(RESSOURCE_SQLITE_INJ_PATH)

$(RESSOURCE_PATTERN_PATH): \
	$(RESSOURCE_DIR)/Mysql/errors_message.txt \
	$(RESSOURCE_DIR)/SQLite/errors_message.txt \
	$(GEN_ERROR_SCRIPT)
	@echo "[*] Generating error patterns..."
	python3 $(GEN_ERROR_SCRIPT)
	@echo "[+] Done."

$(RESSOURCE_MYSQL_INJ_PATH): \
	$(RESSOURCE_DIR)/Mysql/error_base.txt \
	$(GEN_MYSQL_SCRIPT)
	@echo "[*] Generating MySQL injection patterns..."
	python3 $(GEN_MYSQL_SCRIPT)
	@echo "[+] Done."

$(RESSOURCE_SQLITE_INJ_PATH): \
	$(RESSOURCE_DIR)/SQLite/error_base.txt \
	$(GEN_SQLITE_SCRIPT)
	@echo "[*] Generating SQLite injection patterns..."
	python3 $(GEN_SQLITE_SCRIPT)
	@echo "[+] Done."

clean:
	rm -f $(RESSOURCE_PATTERN_PATH)
	rm -f $(RESSOURCE_MYSQL_INJ_PATH)
.PHONY: all clean

