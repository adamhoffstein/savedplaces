#!/bin/bash
docker-compose -f ../docker-compose.yml exec db psql postgres -U postgres