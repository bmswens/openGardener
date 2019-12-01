#!/usr/bin/env bash
# get current directory and cd into openGardener directory
directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${directory}
cd ..
cd ..
# stop and remove the service
systemctl disable openGardener
systemctl stop openGardener
rm /etc/systemd/system/openGardener.service
# remove all the files
rm -rf openGardener
