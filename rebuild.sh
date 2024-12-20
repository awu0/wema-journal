#!/bin/bash
# This runs on PythonAnywhere servers: fetches new code,
# installs needed packages, and restarts the server.

export API_TOKEN="a1a01ea213f67e26219bfb73905f6853c4dfa4fd"

touch rebuild
echo "Rebuilding $PA_DOMAIN"

echo "Install packages"
pip install --upgrade -r requirements.txt

echo "Installing PythonAnywhere helper package"
pip install pythonanywhere

echo "Going to reboot the webserver using $API_TOKEN"
curl -X POST \
     -H "Authorization: Token $API_TOKEN" \
     https://www.pythonanywhere.com/api/v0/user/$PA_USER/webapps/$PA_DOMAIN/reload/

touch reboot
echo "Finished rebuild."
