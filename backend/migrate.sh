#!/bin/bash
docker-compose -f ../docker-compose.yml exec backend alembic revision --autogenerate -m "migration at $(date '+%Y%m%d%H%M')"
docker-compose -f ../docker-compose.yml exec backend alembic upgrade head