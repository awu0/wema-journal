#!/usr/bin/env python3

import os
import sys
import requests
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def reload_pythonanywhere_webapp(domain, token):
    """
    Reload a PythonAnywhere web application using their API.
    """
    api_url = f"https://www.pythonanywhere.com/api/v0/user/{domain.split('.')[0]}/webapps/{domain}/reload/"
    headers = {'Authorization': f'Token {token}'}

    try:
        response = requests.post(api_url, headers=headers)
        if response.status_code == 200:
            logging.info("Web application reloaded successfully")
            return True
        else:
            logging.error(f"Failed to reload web application: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logging.error(f"Error reloading web application: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: pa_reload_webapp.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    token = os.getenv('API_TOKEN')
    
    if not token:
        logging.error("API_TOKEN environment variable not set")
        sys.exit(1)

    if reload_pythonanywhere_webapp(domain, token):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()