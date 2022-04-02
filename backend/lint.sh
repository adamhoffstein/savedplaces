#!/bin/bash
poetry run black -l 79 app
poetry run pyflakes app