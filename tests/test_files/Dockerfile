#
# A typical Dockerfile for a Django app using Poetry for dependency management
# This image is never run it only a template for testing purposes
# The only parts needed from this are the python image and poetry version
#

FROM node:18-slim as frontend

ENV NODE_OPTIONS=--openssl-legacy-provider

ARG CI=true

COPY package.json package-lock.json tsconfig.json webpack.config.js tailwind.config.js  ./
RUN npm ci --no-optional --no-audit --progress=false


COPY ./appname/ ./appname/
RUN npm run build:prod


# This is the production image. It is optimized for runtime performance and
FROM python:3.11-slim-bullseye as production

ARG POETRY_INSTALL_ARGS="--no-dev"
ARG POETRY_VERSION=1.3.2

ENV VIRTUAL_ENV=/venv

RUN useradd newuser --create-home && mkdir /app $VIRTUAL_ENV && chown -R newuser /app $VIRTUAL_ENV

WORKDIR /app

# ENV PATH=$VIRTUAL_ENV/bin:$PATH \
#     POETRY_INSTALL_ARGS=${POETRY_INSTALL_ARGS} \
#     PYTHONUNBUFFERED=1 \
#     DJANGO_SETTINGS_MODULE=appname.settings.production \
#     PORT=8000 \
#     WEB_CONCURRENCY=3 \
#     GUNICORN_CMD_ARGS="-c gunicorn-conf.py --max-requests 1200 --max-requests-jitter 50 --access-logfile - --timeout 25"

# ARG BUILD_ENV
# ENV BUILD_ENV=${BUILD_ENV}

EXPOSE 8000

# RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     curl \
#     git \
#     && apt-get autoremove && rm -rf /var/lib/apt/lists/*


# RUN apt-get update --yes --quiet && apt-get install -y binutils libproj-dev gdal-bin

# RUN pip install --no-cache poetry==${POETRY_VERSION}

USER newuser

# Install your app's Python requirements.
# RUN python -m venv $VIRTUAL_ENV
# COPY --chown=sueryder pyproject.toml poetry.lock ./
# RUN pip install --no-cache --upgrade pip && poetry install ${POETRY_INSTALL_ARGS} --no-root --extras gunicorn && rm -rf $HOME/.cache

# COPY --chown=sueryder --from=frontend ./sueryder/static_compiled ./sueryder/static_compiled

# Copy application code.
COPY --chown=newuser . .

# Run poetry install again to install our project (so the the sueryder package is always importable)
# RUN poetry install ${POETRY_INSTALL_ARGS}

# Collect static. This command will move static files from application
# directories and "static_compiled" folder to the main static directory that
# will be served by the WSGI server.
# RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

# Load shortcuts
# COPY ./docker/bashrc.sh /home/sueryder/.bashrc

# Run the WSGI server. It reads GUNICORN_CMD_ARGS, PORT and WEB_CONCURRENCY
# environment variable hence we don't specify a lot options below.
CMD gunicorn sueryder.wsgi:application



FROM production as dev

USER root

RUN apt-get update --yes --quiet && apt-get install -y postgresql-client

USER newuser

ENV NODE_OPTIONS=--openssl-legacy-provider

ARG NVM_VERSION=0.39.5
COPY --chown=sueryder .nvmrc ./
RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v${NVM_VERSION}/install.sh | bash \
    && bash --login -c "nvm install --no-progress && nvm alias default $(nvm run --silent --version)"

COPY --chown=newuser --from=frontend ./node_modules ./node_modules

CMD tail -f /dev/null
