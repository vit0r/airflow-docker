#!/usr/bin/env bash

function wrapper_flask1103(){
  echo "AIRFLOW_VERSION_NUMBER == ${AIRFLOW_VERSION_NUMBER}"
  if [ "${AIRFLOW_VERSION_NUMBER}" == "1.10.3" ]; then
    python3.6 -m pip install Flask==1.0.4 --user
  fi
}

case "$1" in
  webserver)
    wrapper_flask1103
    install_gcloud_sdk
    airflow initdb
    airflow scheduler &
    exec airflow webserver
    ;;
  version)
    exec airflow "$@"
    ;;
  bash)
    exec "$@"
    ;;
esac
