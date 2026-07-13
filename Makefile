PYTHON      := python3
SCRIPT      := a_maze_ing.py
CONFIG      := config.txt
REQ_FILE    := requirements.txt

GREEN       := \033[1;32m
BLUE        := \033[1;34m
YELLOW      := \033[1;33m
RESET       := \033[0m

install:
	@$(PYTHON) -m venv venv
	@echo "$(BLUE) -> Installing dependencies $(REQ_FILE) $(RESET)"
	@. venv/bin/activate && pip install -r $(REQ_FILE)
	@echo "$(GREEN) -> Installation Complete!$(RESET)"

run:
	@echo "$(GREEN) -> Running $(SCRIPT) with $(CONFIG) $(RESET)"
	@$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	@echo "$(YELLOW) -> Starting the debugger (PDB) $(RESET)"
	@$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

lint:
	@echo "$(BLUE) -> Passing the Linter (flake8 y Mypy) $(RESET)"
	@venv/bin/flake8 . --exclude=venv,mlx
	@venv/bin/mypy .
	@echo "$(GREEN) -> Clean, well-typed code! $(RESET)"

lint-strict:
	@echo "$(YELLOW) -> Passing the STRICT Linter (Mypy --strict) $(RESET)"
	@venv/bin/mypy . --strict
	@echo "$(GREEN) -> Perfect! Code is 100% strict and well-typed! $(RESET)"

build: clean
	@echo "$(BLUE) -> Project Packaging $(RESET)"
	@$(PYTHON) -m build
	@mv dist/*.whl .
	@mv dist/*.tar.gz .
	@rm -rf dist build *.egg-info
	@echo "$(GREEN) -> Package generated in the root of the repo $(RESET)"

clean:
	@echo "$(YELLOW) -> Deleting Temporary Files and Cache $(RESET)"
	@rm -rf __pycache__ .mypy_cache *.egg-info build dist mazegen/__pycache__ mlx/__pycache__ maze.txt
	@echo "$(GREEN) -> Cleaning complete! $(RESET)"

.PHONY: install run debug lint build clean
