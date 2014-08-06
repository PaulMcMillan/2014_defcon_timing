echo "Setting cpu 0 and 1 to performance governor"
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
sudo sh -c "echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
sudo tcpdump -i eth1 -j adapter --time-stamp-precision=nanoseconds -w data/out.pcap
