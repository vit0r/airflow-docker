#!/usr/bin/env bash

if [ ! -d ${HOME}/.config/gcloud ];then
    exit 1;    
fi

if [ ! -f ${HOME}/.config/gcloud/application_default_credentials.json ];then
    gcloud auth application-default login
fi

rsync -Pru ${HOME}/.config/gcloud ${1}/.tmp_gcloud_config --exclude logs

exit 0