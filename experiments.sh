#!/bin/bash

# Define la ruta de la carpeta con los archivos de agentes
AGENT_FOLDER="./agents"

# Define la ruta al script de Python
PYTHON_SCRIPT="./experiments.py"

# Itera sobre cada archivo en la carpeta de agentes
for agent_file in "$AGENT_FOLDER"/*
do
    echo "Procesando: $agent_file"
    python "$PYTHON_SCRIPT" "$agent_file"
done