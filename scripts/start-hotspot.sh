sudo cp /home/pi/notipiServer/configs/dhcpcd.conf.hotspot /etc/dhcpcd.conf
sudo systemctl restart dhcpcd
sudo systemctl enable hostapd
sudo systemctl start hostapd
