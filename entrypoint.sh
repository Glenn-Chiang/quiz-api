#!/bin/bash
flask db upgrade
exec gunicorn --bind :5000 app:app --timeout 90