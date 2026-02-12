#!/usr/bin/env bash

pause() {
    read -rp "Press ENTER to continue..."
}

declare -A COMMANDS
COMMANDS[1]="pip3 install -r requirements.txt; pause"
COMMANDS[2]="python3 -m trainers.offline.train; pause"
COMMANDS[3]="python3 -c 'from models.helper import rollback; rollback()'; pause"
COMMANDS[4]="uvicorn api:app --host \$(hostname -I | awk '{print \$1}') --port 8001 --reload"

declare -A LABELS
LABELS[1]="Install dependencies"
LABELS[2]="Train offline model"
LABELS[3]="Rollback model version"
LABELS[4]="Run API server"

while true; do
    clear
    echo -e "\n-------------------------\n"

    for ((key=1; key<=${#COMMANDS[@]}; key++)); do
        echo "$key) ${LABELS[$key]}"
    done

    echo "q) Quit"
    echo -e "\n-------------------------\n"

    read -p "Select option: " choice

    if [[ "$choice" == "q" || "$choice" == "Q" ]]; then
        exit 0
    fi

    if [[ -n "${COMMANDS[$choice]}" ]]; then
        echo ">>> Running: ${LABELS[$choice]}"
        eval "${COMMANDS[$choice]}"
    else
        echo "Invalid option"
    fi
done