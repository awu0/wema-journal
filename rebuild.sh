#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

touch rebuild
echo "Rebuilding $PA_DOMAIN"

echo "Setting up mock PythonAnywhere environment in GitHub Actions"
export PA_MOCK_HOME="/home/$PA_USER/.virtualenvs/$VENV"
mkdir -p $PA_MOCK_HOME
python3 -m venv $PA_MOCK_HOME

echo "Activating the virtual environment for user $PA_USER"
source $PA_MOCK_HOME/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

echo "Install packages"
pip install --upgrade -r requirements.txt

echo "Installing PythonAnywhere helper package"
pip install pythonanywhere

echo "Going to reboot the webserver using $API_TOKEN"
export PYTHONANYWHERE_TOKEN=$API_TOKEN
if command -v pa_reload_webapp.py &>/dev/null; then
  pa_reload_webapp.py $PA_DOMAIN

touch reboot
echo "Finished rebuild."
