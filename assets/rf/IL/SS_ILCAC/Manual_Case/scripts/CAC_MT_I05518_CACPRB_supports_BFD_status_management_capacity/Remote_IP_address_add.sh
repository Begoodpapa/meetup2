
for ((j=60;j<=69;j++));
do
fsclish -c "set config-mode on" -c "add networking address dedicated /EITPUPTRMRG-2 iface ethtest20 ip-address 191.251.10.$j/24"
done;


