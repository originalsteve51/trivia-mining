#!/bin/zsh

# Do not push this to github because it contains my secret key used to 
# access OpenAI
# github is smart enough to detect these and prevent pushing files containing these secrets

# Since this file can hold secrets and it is not ever uploaded to github, I can
# copy the github Personal Access Token for my github userid here:
#
# As of January 13, 2024 it is:
# ID:                    originalsteve51
# Personal Access Token: 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

# For api calls to OpenAI to get song information, need the api key in the environment
export OPENAI_API_KEY="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"

python question_browser.py
