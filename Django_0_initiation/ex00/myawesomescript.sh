#!/bin/bash
# This script prints url of a given bitly link

if [ $# -ne 1 ]; then
    echo "Usage: $0 <bitly_link>"
    exit 1
fi

bitly_link=$1

final_url= curl -s "$bitly_link" | cut -d '"' -f 2 | grep -E '^http'

echo -n $final_url