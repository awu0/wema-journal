#!/bin/bash

export FLASK_ENV=development
export PROJ_DIR=$PWD
export DEBUG=1

# Run the Flask server locally in the background
PYTHONPATH=$(pwd):$PYTHONPATH FLASK_APP=server.endpoints flask run --debug --host=127.0.0.1 --port=8000 &

# Save the PID of the Flask process
FLASK_PID=$!

# Navigate to the React frontend directory
#cd frontend

# Start React app
#npm run start

# Kill the Flask server when React is stopped
#kill $FLASK_PID
