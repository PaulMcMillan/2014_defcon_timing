while true; do
    nc -l 4567 > `date +%s`.pcap
done
