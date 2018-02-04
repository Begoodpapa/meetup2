for((i=50;i<=59;i++));
do
fsclish -c "delete config-mode on" -c "add networking address dedicated /QNUP-0 iface ethtest20 ip-address 191.251.10.$i/24"
done;

