# Raspberry PI sail station

Multiplex all boat data to wifi access point. (https://www.youtube.com/watch?v=vdmb49YoF0g)

<img src="https://user-images.githubusercontent.com/1060425/144998274-dc84c163-21de-4a79-884c-eac48d8ab764.jpg?s=150" height="250"> | <img src="https://user-images.githubusercontent.com/1060425/144998294-8879c9f1-f3ce-4b34-b867-25683005da76.jpg?s=150" height="250">

Inputs:
- AIS 
- GPS
- Seatalk/NMEA

Outputs:
- TCP
- UDP broadcast
- Log file


## Release links

```
cd ~
rm -rf sail-station
wget https://github.com/dakk/sail-station/archive/refs/heads/master.zip
unzip master.zip
mv sail-station-master sail-station
rm -rf master.zip
cd sail-station
sudo bash install.sh
```

## Install

Write lite raspbian image to RPI.

Enable ssh using a screen and a keyboard:

```bash
systemctl enable ssh
systemctl start ssh
```

or simply create an empty ssh file on boot partition.

Connect all devices and install the configuration. To connect many usb devices, use an hub with additional
usb power.

```bash
sudo bash install.sh
```

Check if the installation worked fine:

```bash
bash check.sh
```

You will now see an ap called DIVERSA_NMEA; connect to it using password "password"


## Usage

After the system is set up, connect using your device to the new ap using password "password". Use 192.168.3.1 ip and port 10110 as TCP source. 
The system will also log all nmea data to ```/home/pi/data.nmea```, useful to analyze data at home.

<img src="https://user-images.githubusercontent.com/1060425/144998326-00799f41-287e-4f48-927e-8e1be99fad2b.jpg" width="250px">


## Stalk interface for raspberry

<img src="https://user-images.githubusercontent.com/1060425/144998349-d8c1aecc-723a-491a-8f82-6e9ede4e8ee1.jpg" width="300px">


## References

- https://andersonsabroad.com/blog/raspberry-pi-marine-computer/step-4-install-kplex-nmea-multiplexer/
- https://github.com/SignalK/signalk-server/blob/master/Seatalk(GPIO).md
- https://github.com/marcobergman/seatalk_convert
- https://pysselilivet.blogspot.com/2020/06/seatalk1-to-nmea-0183-converter-diy.html
