#!/usr/bin/env bash

postgre_docker=$(docker ps -f name=postgres -a -q)
if [ "${postgre_docker}" ]; then
  docker container rm -f postgres
fi
exit 0