#!/bin/bash
sudo docker ps -a > bin
tail -n +2 bin > bi
awk 'NF>1{print $NF}' bi > $1
while IFS='' read -r line || [[ -n "$line" ]]; do
    sudo docker rm $line
done < "$1"
rm bin
rm bi
