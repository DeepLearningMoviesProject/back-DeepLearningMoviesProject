#!/bin/bash
sudo docker ps -a > bin1
tail -n +2 bin1 > bin2
awk 'NF>1{print $NF}' bin2 > bin3
while IFS='' read -r line || [[ -n "$line" ]]; do
    sudo docker rm -f $line
done < "bin3"
rm bin1
rm bin2
rm bin3
