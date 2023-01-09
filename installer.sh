#!/usr/bin/env bash

install_requirements() {
    pip3 install -q --upgrade pip
    echo -e "• Installing Requirements ..."
    pip3 install -q --no-cache-dir -r $DIR/requirements.txt
    echo -e "• Installing Optional Requirements ..."
    pip3 install -q --no-cache-dir -r $DIR/optional-requirements.txt
    echo -e "Installing YouTube Downloder ( yt-dlp ) ..."
    pip3 install -q yt-dlp
    echo -e "• All Requirements Was Installed!"
}

main() {
    echo -e "• Starting Fido Self Setup ..."
    (install_requirements)
    echo -e "• Installer Setup Was Completed!"
}

main
