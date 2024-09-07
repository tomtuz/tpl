#!/bin/bash

# Get the directory of the original script, not the symlink
DIR="$( cd "$( dirname "$(readlink -f "${BASH_SOURCE[0]}")" )" && pwd )"

# Debug
echo "dirname: ${dirname}"
echo "BASH_SOURCE: ${BASH_SOURCE}"
echo "DIR: ${DIR}"

# Run the Python script with the same arguments
python3 "$DIR/tpl_core.py" "$@"
