FROM python:3.6.9-slim-stretch

ENV PYTHONWARNINGS=ignore
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV AIRFLOW_GPL_UNIDECODE=yes
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
ENV AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres:5432/airflow
ENV AIRFLOW__CELERY__BROKER_URL=amqp://guest:guest@rabbitmq01:5672/
ENV AIRFLOW_HOME=/usr/local/airflow
ENV GCLOUD_CONFIGS=${AIRFLOW_HOME}/.config
ENV GOOGLE_APPLICATION_CREDENTIALS=${GCLOUD_CONFIGS}/gcloud/application_default_credentials.json

RUN useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow

RUN mkdir -p ${GCLOUD_CONFIGS}

RUN chown -R airflow: ${AIRFLOW_HOME}

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
    ' \
    && apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        apt-utils \
        apt-transport-https \
        ca-certificates \
        gnupg \
        curl \
        rsync \
        locales \
    && sed -i 's/^# en_US.UTF-8 UTF-8$/en_US.UTF-8 UTF-8/g' /etc/locale.gen \
    && locale-gen \
    && update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    && apt-get purge --auto-remove -y $buildDeps \
    && apt-get autoremove -y --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

ENV PSYCOPG_DEBUG=1

RUN pip install --no-cache -U pip setuptools wheel pytz pyOpenSSL ndg-httpsclient pyasn1 psycopg2-binary 

ARG GCLOUD_INSTALL="NO"

ADD ./install-gcloud-sdk.sh /install-gcloud-sdk.sh

RUN sh install-gcloud-sdk.sh ${GCLOUD_INSTALL}

ARG AIRFLOW_VERSION
ARG DAGS_FOLDER
ARG PLUGINS_FOLDER
ARG AIRFLOW_DEPS
ARG PIP_PKGS_EXT

ENV AIRFLOW_VERSION_NUMBER=${AIRFLOW_VERSION}

RUN pip install --no-cache apache-airflow${AIRFLOW_DEPS}==${AIRFLOW_VERSION} ${PIP_PKGS_EXT}

ADD ./entrypoint.sh /entrypoint.sh

EXPOSE 8080 5555 8793

WORKDIR ${AIRFLOW_HOME}

USER airflow

ENTRYPOINT ["/entrypoint.sh"]
