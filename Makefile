.PHONY: sync
sync:
	uv sync

.PHONY: install-pre-commit
install-pre-commit:
	uv run pre-commit uninstall && uv run pre-commit install

.PHONY: lint
lint:
	uv run pre-commit run --all-files

.PHONY: tailwind
tailwind:
	uv run python manage.py tailwind watch

.PHONY: migrations
migrations:
	uv run python manage.py makemigrations

.PHONE: migrate
migrate:
	uv run python manage.py migrate

.PHONY: runserver
runserver:
	uv run python manage.py runserver

.PHONY: run
run:
	uv run python manage.py tailwind runserver

.PHONY: superuser
superuser:
	uv run python manage.py createsuperuser

.PHONY: test
test:
	uv run pytest -v -rs -n auto

.PHONY: update
update: sync migrate install-pre-commit;


.PHONY: commit

commit:
	git status
	@read -p "Enter commit message: " msg; \
	git add .; \
	git commit -m "$$msg"
