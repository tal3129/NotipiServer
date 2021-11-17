sudo cp /home/pi/notipiServer/configs/dhcpcd.conf.wifi /etc/dhcpcd.conf
sudo systemctl restart dhcpcd
sudo systemctl stop hostapd
sudo systemctl disable hostapd
