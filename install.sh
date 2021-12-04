WIFI_AP=DIVERSA-NMEA
KPLEX_VERSION=1.4-1

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


echo Installing pigpio
apt-get install pigpio python3-pigpio
pip install pynmea2
systemctl enable pigpiod
systemctl restart pigpiod

echo Installing seatalk2nmea...
cp stalk_read/stalk_read.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable stalk_read
systemctl restart stalk_read

# echo Installing gpx_logger...
# mkdir /home/pi/gpx && chmod 777 /home/pi/gpx
# cp gpx_logger/gpx_logger.service /etc/systemd/system/
# systemctl daemon-reload
# systemctl enable gpx_logger
# systemctl restart gpx_logger

echo Installing kplex...

wget http://www.stripydog.com/download/kplex_`echo $KPLEX_VERSION`_armhf.deb
dpkg -i ./kplex_`echo $KPLEX_VERSION`_armhf.deb
mv /etc/init.d/kplex /usr/share/kplex/kplex.init
wget -O /etc/systemd/system/kplex.service http://stripydog.com/download/kplex.service
systemctl daemon-reload
systemctl enable kplex
cp kplex.conf /etc/kplex.conf
systemctl restart kplex
rm kplex_`echo $KPLEX_VERSION`_armhf.deb


echo Creating AP...
apt install dnsmasq hostapd
systemctl stop dnsmasq
systemctl stop hostapd
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cp wlan/dhcpcd.conf /etc/dhcpcd.conf
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cp wlan/dnsmasq.conf /etc/dnsmasq.conf
systemctl start dnsmasq
cp wlan/hostapd.conf /etc/hostapd/hostapd.conf
cp wlan/hostapd /etc/default/hostapd
service dhcpcd restart
systemctl unmask hostapd
systemctl enable hostapd
systemctl start hostapd


echo `echo $WIFI_AP` wifi network is ready
echo Done.
