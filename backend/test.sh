#!/bin/bash
if [[ $(docker-compose -f ../docker-compose.yml exec backend printenv ENV_STATE) == *"test"* ]]; then
  docker-compose -f ../docker-compose.yml exec backend python -m pytest -vv
else
  echo "Make sure you are running the Docker container in test mode: ./run-locally.sh test"
fi