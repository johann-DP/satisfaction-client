#!/bin/bash

# Start the MLflow server
mlflow server --backend-store-uri sqlite:////app/mlflow_data/mlflow.db --default-artifact-root /app/mlflow_data/mlruns --host 0.0.0.0 --port 5000

# echo "Checking if MLflow server is available..."
# /app/scripts/wait-for-it.sh localhost 5000 -- echo "MLflow server is available."

######### SERVEUR ETERNEL ########################



# echo "Creating CSV file..."
# python /app/scripts/extraction_features.py

# echo "Starting experiment..."
# python /app/scripts/experiment.py

# # Clean up and stop MLflow server
# echo "Stopping MLflow server..."
# kill $(jobs -p)
