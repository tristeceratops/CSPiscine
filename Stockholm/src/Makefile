KEY_PATH := .key
SRC := stockholm.py

all: run

run:
	@if [ -f $(KEY_PATH) ]; then \
		python3 $(SRC) $(KEY_PATH); \
	else \
		echo "Error: $(KEY_PATH) does not exist"; \
	fi

reverse:
	@if [ -f $(KEY_PATH) ]; then \
		python3 $(SRC) -r $(KEY_PATH); \
	else \
		echo "Error: $(KEY_PATH) does not exist"; \
	fi

version:
	@python3 $(SRC) -v

.PHONY: all run reverse version