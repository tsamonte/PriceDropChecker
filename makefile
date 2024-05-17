VENV = venv

# Generated venv will have a different structure depending on the operating system
# Windows (checks if environment variable that only exists in Windows is present)
ifdef OS
	BIN = $(VENV)/Scripts
	RM = rmdir /s /q
# Linux
else
	ifeq ($(shell uname), Linux)
		BIN = $(VENV)/bin
		RM = rm -rf
	endif
endif

PYTHON = $(BIN)/python
PIP = $(BIN)/pip
ACTIVATE = $(BIN)/activate

$(ACTIVATE): requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

run: $(ACTIVATE)
	$(PYTHON) src/main.py persist

run-once: $(ACTIVATE)
	$(PYTHON) src/main.py

clean:
	$(RM) $(VENV)

all: $(ACTIVATE) run clean