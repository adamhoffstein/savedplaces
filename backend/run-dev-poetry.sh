#!/usr/bin/env bash
export ENV_STATE=dev
poetry run uvicorn app.main:app --reload