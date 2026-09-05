# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.de  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/06 02:51:25 by maprunty          #+#    #+#              #
#    Updated: 2026/09/06 00:39:55 by maprunty         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #



.PHONY: install run debug clean lint lint-strict

MAIN		:= main.py
CONFIG		:= config.txt
UV			:= uv
DBG			:= pdb
PYTHON		:= python3
MYPYFLAGS	:= --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

run:
	$(UV) run $(MAIN)

install:
	$(UV) sync --no-dev

dev: fclean
	$(UV) sync  --dev


debug:
	$(UV) run $(PYTHON) -m $(DBG) $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info"  -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "resized" -exec rm -rf {} +
	find . -type f -name "*.pyc"       -delete

fclean: clean
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name "wheels" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type f -name "*.whl" -exec rm -rf {} +
	find . -type f -name "uv.lock" -exec rm -rf {} +
	find . -type f -name "*.sw*" -exec rm -rf {} +

lint:
	$(UV) run $(PYTHON) -m flake8 .
	$(UV) run $(PYTHON) -m mypy . $(MYPYFLAGS)

lint-strict:
	$(UV) run $(PYTHON) -m flake8 .
	$(UV) run $(PYTHON) -m mypy . --strict
