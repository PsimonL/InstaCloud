# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-PYTHON_VERSION_NOT_SET}

FROM python:${INSTALL_PYTHON_VERSION} AS builder

WORKDIR /app

RUN true
COPY requirements requirements
RUN pip install --no-cache -r requirements/prod.txt

COPY instacloud_core instacloud_core
COPY migrations migrations
COPY .env.example .env

# ================================= PRODUCTION =================================
FROM python:${INSTALL_PYTHON_VERSION} as production

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY --from=builder --chown=sid:sid /app/instacloud_core/static /app/instacloud_core/static
COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY . .

EXPOSE 5000


# TESTING =======================================================================================================
RUN test -f /app/instacloud_core/app.py || (echo "Error: Flask application file not found." && exit 1)
RUN test -d /app/migrations || (echo "Error: Database migration directory not found." && exit 1)
RUN test -f /app/.env.example || (echo "Error: Database configuration file (.env) not found." && exit 1)
# ===============================================================================================================

# RUN ls -la
# RUN pwd

# Visible after build proces in a container
ENV FLASK_APP=instacloud_core.app
# ENV DATABASE_URL=$DATABASE_URL
# Visible only during build process
ARG DATABASE_URL
ARG SECRET_KEY
ARG SEND_FILE_MAX_AGE_DEFAULT

# RUN echo "DATABASE_URL: $DATABASE_URL"
# RUN printenv
# RUN flask db upgrade

ENTRYPOINT ["gunicorn"]  
CMD ["instacloud_core.app:create_app()", "-b", "0.0.0.0:5000", "-w", "1"]


# ================================= DEVELOPMENT ================================
FROM builder AS development
RUN pip install --no-cache -r requirements/dev.txt
EXPOSE 2992
EXPOSE 5000

ENV FLASK_APP autoapp.py

CMD ["flask", "run", "--host=0.0.0.0"]