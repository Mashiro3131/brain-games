#!/bin/bash

# You may want to change the permissions of the script to make it executable:
# chmod +x install_fonts.sh

# Change the path to the brain-games folder "$HOME/YourFolder/brain-games/fonts"
fontFolder="$HOME/Downloads/brain-games/fonts"

for fontFile in "$fontFolder"/*.otf; do
    echo "Installing font: $(basename "$fontFile")"
    
    cp "$fontFile" "/usr/local/share/fonts/" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "Font $(basename "$fontFile") is already installed."
    else
        echo "Failed to install font $(basename "$fontFile")."
    fi
done
