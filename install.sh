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

wget http://www.stripydog.com/download/kplex_1.4-1_armhf.deb
dpkg -i ./kplex_1.4.1-1_armhf.deb
systemctl enable kplex
cp kplex.conf /etc/kplex.conf
systemctl start kplex


echo Creating AP...



echo Connect to DIVERSA-NMEA wifi network
echo Done.
