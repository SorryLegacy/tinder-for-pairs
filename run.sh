#! /bin/bash

port=$1

if [ -z "$port" ]
then
    echo "Please provide port as ./run.sh 5001"
    exit 1
fi


uvicorn app:app --reload --host=0.0.0.0  --port=$port
