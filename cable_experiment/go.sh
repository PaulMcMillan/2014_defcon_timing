sudo tcpdump -c 30 -j adapter -i eth2 --time-stamp-precision=nanoseconds -w data2.pcap &
sudo tcpdump -c 30 -j adapter -i eth5 --time-stamp-precision=nanoseconds -w data5.pcap &
sleep 1
ping -c 30 -b -I eth2 169.254.0.0
