# Raspberry PI sail station
Multiplex all boat data to wifi ap.

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


## Stalk interface for raspberry

![Schematics]()

## References

- https://andersonsabroad.com/blog/raspberry-pi-marine-computer/step-4-install-kplex-nmea-multiplexer/
- https://github.com/SignalK/signalk-server/blob/master/Seatalk(GPIO).md
- https://github.com/marcobergman/seatalk_convert
- https://pysselilivet.blogspot.com/2020/06/seatalk1-to-nmea-0183-converter-diy.html