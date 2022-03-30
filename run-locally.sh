#!/bin/bash
export ENV_STATE=${1:-dev}
docker-compose up --build --remove-orphans