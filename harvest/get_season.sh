#!/bin/zsh

GET_WEBIDS_FOR_SEASON="./get_webids_for_season.py"
GAME_RETRIEVE_FOR_WEBID="./j-scrape.py"

# Loop indefinitely
while true do
    # Get a webid and mark it as processed in the database
    VALUE=$(python "$GET_WEBIDS_FOR_SEASON" $1)
    # Check if the value is -1 signifying all have been processed
    if [ "$VALUE" -eq -1 ]; then
        echo "Terminating loop as all webids have been processed."
        break
    fi
    echo "$VALUE"

    # Access the show pointed to by the webid and get all its categories, questions, etc
    python "$GAME_RETRIEVE_FOR_WEBID" "$VALUE"