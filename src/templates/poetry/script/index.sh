#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get the parent directory (templates/poetry)
TEMPLATE_DIR="$(dirname "$SCRIPT_DIR")"

# Check if a command is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <command> [args]"
    echo "Available commands:"
    echo "  new <project_name> - Create a new Poetry project"
    exit 1
fi

COMMAND="$1"
shift  # Remove the first argument (the command)

case "$COMMAND" in
    new)
        python3 "$TEMPLATE_DIR/new.py" "$@"
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo "Available commands:"
        echo "  new <project_name> - Create a new Poetry project"
        exit 1
        ;;
esac
