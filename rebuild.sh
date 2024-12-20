#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

touch rebuild
echo "Rebuilding $PA_DOMAIN"

echo "Install packages"
pip install --upgrade -r requirements.txt

echo "Installing PythonAnywhere helper package"
pip install pythonanywhere

echo "Going to reboot the webserver using $API_TOKEN"
export PYTHONANYWHERE_TOKEN=$API_TOKEN
export username="wl2612"
pa_reload_webapp.py $PA_DOMAIN

touch reboot
echo "Finished rebuild."
