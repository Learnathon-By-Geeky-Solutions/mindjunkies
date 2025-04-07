param(
    [string]$Task = "help"
)

function Sync {
    uv sync
}

function InstallPreCommit {
    uv run pre-commit uninstall
    uv run pre-commit install
}

function Lint {
    uv run pre-commit run --all-files
}

function Tailwind {
    uv run python manage.py tailwind watch
}

function Migrations {
    uv run python manage.py makemigrations
}

function Migrate {
    uv run python manage.py migrate
}

function Runserver {
    uv run python manage.py runserver
}

function Superuser {
    uv run python manage.py createsuperuser
}

function Test {
    uv run pytest -v -rs -n auto
}

function Update {
    Sync
    Migrate
    InstallPreCommit
}

function Help {
    Write-Host "Available tasks:"
    Write-Host "  sync              -> uv sync"
    Write-Host "  install-pre-commit -> uninstall + install pre-commit"
    Write-Host "  lint              -> run lint via pre-commit"
    Write-Host "  tailwind          -> tailwind watch"
    Write-Host "  migrations        -> makemigrations"
    Write-Host "  migrate           -> migrate"
    Write-Host "  runserver         -> run Django server"
    Write-Host "  superuser         -> create superuser"
    Write-Host "  test              -> run tests"
    Write-Host "  update            -> sync + migrate + install-pre-commit"
    Write-Host "  help              -> show this help message"
}

switch ($Task.ToLower()) {
    "sync"               { Sync }
    "install-pre-commit" { InstallPreCommit }
    "lint"               { Lint }
    "tailwind"           { Tailwind }
    "migrations"         { Migrations }
    "migrate"            { Migrate }
    "runserver"          { Runserver }
    "superuser"          { Superuser }
    "test"               { Test }
    "update"             { Update }
    default              { Help }
}
