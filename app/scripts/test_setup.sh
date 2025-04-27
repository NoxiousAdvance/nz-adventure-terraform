#!/bin/bash

# Start the Firestore emulator
start_emulator() {
    echo "Starting Firestore emulator..."
    gcloud beta emulators firestore start --host-port=localhost:8081 &
    export FIRESTORE_EMULATOR_HOST=localhost:8081
}

# Stop the Firestore emulator
stop_emulator() {
    echo "Stopping Firestore emulator..."
    kill $(lsof -t -i:8081)
    unset FIRESTORE_EMULATOR_HOST
}

# Handle script arguments
case "$1" in
    start)
        start_emulator
        ;;
    stop)
        stop_emulator
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac 