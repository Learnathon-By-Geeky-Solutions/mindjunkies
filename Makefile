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

.PHONY: run-server
run-server:
	uv run python manage.py runserver

.PHONY: superuser
superuser:
	uv run python manage.py createsuperuser


.PHONY: update
update: sync migrate install-pre-commit;
