WIFI_AP=DIVERSA-NMEA
KPLEX_VERSION=1.4-1

echo Installing pigpio
apt-get install pigpio
systemctl enable pigpiod
systemctl start pigpiod

echo Installing seatalk2nmea...
cp stalk_read.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable stalk_read
systemctl start stalk_read

echo Installing kplex...

wget http://www.stripydog.com/download/kplex_$(KPLEX_VERSION)_armhf.deb
dpkg -i ./kplex_$(KPLEX_VERSION)_armhf.deb
mv /etc/init.d/kplex /usr/share/kplex/kplex.init
wget -O /etc/systemd/system/kplex.service http://stripydog.com/download/kplex.service
systemctl daemon-reload
systemctl enable kplex
cp kplex.conf /etc/kplex.conf
systemctl start kplex
rm kplex_$(KPLEX_VERSION)_armhf.deb


echo Creating AP...



echo Connect to $(WIFI_AP) wifi network
echo Done.
