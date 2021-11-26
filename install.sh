sudo wget http://www.stripydog.com/download/kplex_1.3.4-1_armhf.deb
sudo dpkg -i ./kplex_1.3.4-1_armhf.deb
sudo systemctl enable kplex
sudo cp kplex.conf /etc/kplex.conf
sudo systemctl start kplex
