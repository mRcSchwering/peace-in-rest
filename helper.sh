#!/usr/bin/env bash
export FLASK_ENV="development"
export FLASK_APP="app.py"

HOST="127.0.0.1"
PORT=5000


flask run -h "$HOST" -p "$PORT"
