#!/usr/bin/env bash

# List all agents running
while read -r line; do
    if [[ "$line" == ID* ]] || [[ "$line" == --* ]]; then
        continue
    fi
    id=$(echo "$line" | awk '{print $1}')
    agent=$(echo "$line" | awk '{print $2}')
    
    if [ ! -d "/home/ubuntu/openfang/agents/$agent" ]; then
        echo "Killing removed agent: $agent ($id)"
        /home/ubuntu/.openfang/bin/openfang agent kill "$id"
    fi
done < <(/home/ubuntu/.openfang/bin/openfang agent list)
