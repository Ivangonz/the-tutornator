import os

from invoke import task


@task
def backend(c):
    c.run('cd api && flask run')


@task
def npmdeps(c):
    if os.path.isdir("webapp/node_modules"):
        c.run('cd webapp && npm install')
    else:
        pass


@task(pre=(npmdeps,))
def webapp(c):
    c.run('cd webapp && npm run serve')


@task
def test(c):
    c.run('python -m pytest --cov=api --color=yes tests/')


@task
def tox(c):
    c.run('tox')


@task
def lock_proj(c):
    c.run('poetry lock -n')


@task
def lint(c):
    """Sorts, cleans, and formats current code."""
    commands = [
        (
            'Sort imports',
            'isort -j2 .',
        ),
        (
            'Remove unused',
            'autoflake -r --remove-all-unused-imports  --ignore-init-module-imports --remove-unused-variables --exclude scratch.py -i api tasks tests setup.py',
        ), (
            'Fix python format',
            'yapf -r -i -p api tests',
        ), (
            'Analyze runtime errors',
            'pyflakes api/',
        ),
        (
            'Check for misspellings',
            'codespell -q3 --skip=".git,.idea,*.pyc,*.pyo,.mypy*,poetry.lock,build,dist" -I .dictionary api',
        )
    ]

    for name, cmd in commands:
        print(' -- ', name)
        c.run(cmd)


@task
def req(c):
    c.run('poetry export -f requirements.txt --without-hashes > requirements.txt')


@task(post=(req,))
def clean(c):
    folders = [
        '.pytest_cache',
        '.tox',
        'build',
        'dist',
        'api.egg-info',
    ]

    files = [
        'requirements.txt',
        '.coverage',
    ]

    for file in files + folders:
        c.run(f'rm -rf {file}')
