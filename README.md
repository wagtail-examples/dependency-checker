# Dependency checker for Python

## Usage

```bash
poetry install
poetry run start
```

Enter the url for your repository and the branch you want to check.

## Options

```bash
poetry run start --help
```

## Limitations

- Only works if the site is run using a Dockerfile in the root of the repository
- Only works if the Dockerfile is named `Dockerfile`
- Only works if the Dockerfile uses poetry to install dependencies

## TODO

- Add support for Dockerfile in subdirectory
- Add support for Dockerfile with different name
- Add support for different dependency managers (requirements.txt, etc.)

## How it works

- It will clone the repository and checkout the specified branch
- It will then inspect the Dockerfile to find the image version and poetry version used
- It will then build a new image and export the dependency list using poetry export -> requirements-frozen.txt
- It will then compare each dependency version in the requirements-frozen.txt with the latest version on PyPi
- It will then output the results in the console and indicate if there are any outdated dependencies

e.g.

```
Production dependencies ...
coverage 5.5 -> 7.2.7
dj-database-url 0.5.0 -> 2.0.0
django 3.2.16 -> 4.2.3
django-basic-auth-ip-whitelist 0.3.4 -> 0.5
django-birdbath 0.0.2 -> 1.1.0
django-csp 3.6 -> 3.7
django-pattern-library 0.7.0 -> 1.0.0
django-phonenumber-field 7.0.2 -> 7.1.0
django-redis 5.0.0 -> 5.3.0
django-referrer-policy == 1.0
django-storages 1.11.1 -> 1.13.2
honcho == 1.1.0
psycopg2 2.8.6 -> 2.9.6
scout-apm 2.10.0 -> 2.26.1
sentry-sdk 1.5.3 -> 1.27.0
wagtail 4.1.1 -> 5.0.2
wagtail-accessibility == 0.2.1
wagtail-django-recaptcha == 1.0
wagtail-factories 3.1.0 -> 4.1.0
wagtail-jotform == 2.0.0
wagtail-nhsuk-frontend 1.5.1 -> 1.5.2
wagtail-readinglevel git+https://github.com/alxbridge/wagtail-readinglevel@61d2660e -> 3.5.0
wagtail-storages == 1.0.0rc1
whitenoise 5.0.1 -> 6.5.0


Development dependencies ...
Werkzeug 2.2.2 -> 2.3.6
black 22.3.0 -> 23.3.0
cryptography 3.4.7 -> 41.0.1
detect-secrets 0.13.1 -> 1.4.0
django-extensions 2.2.9 -> 3.2.3
fabric 2.5.0 -> 3.1.0
flake8 3.8.3 -> 6.0.0
isort 5.12.0 -> 5.11.5
mkdocs 1.3.0 -> 1.4.3
mkdocs-material 8.2.8 -> 9.1.18
pre-commit 2.9.3 -> 3.3.3
pymdown-extensions 9.3 -> 10.0.1
seed-isort-config 1.9.4 -> 2.2.0
stellar == 0.4.5


Manual check required
gunicorn
python
```
