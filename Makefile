run:
	uv run ./main.py -h

lint:
	uvx ruff check ./main.py

update:
	uv sync -U
	uv pip compile pyproject.toml > requirements.txt
