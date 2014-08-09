pactl exit
echo "clearing postrouting table and blocking outgoing acks"
sudo iptables -t mangle -F OUTPUT
sudo iptables -t mangle -A OUTPUT -o eth1 -p tcp --tcp-flags ALL ACK -j DROP

#iptables -t mangle -A POSTROUTING -o eth1 -p tcp --tcp-flags ALL ACK -j CLASSIFY --set-class 1:1
#tc qdisc del dev eth1 root
#tc qdisc add dev eth1 parent root handle 1: prio
#tc qdisc add dev eth1 parent 1:1 handle 10: netem delay 15ms

echo "Setting cpu 0 and 1 to performance governor. Enabling low latency mode."
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
sudo sh -c "echo 1 > /proc/sys/net/ipv4/tcp_low_latency"
sudo tcpdump -i eth1 -j adapter --time-stamp-precision=nanoseconds -w "data/out.pcap"
#sudo tcpdump -i eth1 -j adapter --time-stamp-precision=nanoseconds -G 30 -w "data/%Y-%m-%d-%H-%M-%S.pcap"
