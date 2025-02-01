#!/bin/bash

# Use the trivia conda environment and run the program passed as an argument
conda run -n trivia --live-stream python $1 $2
