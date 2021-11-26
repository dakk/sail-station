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


## Install

Write lite raspbian image to RPI.

Enable ssh using a screen and a keyboard:

```bash
systemctl enable ssh
systemctl start ssh
```

Connect all devices and install the configuration. To connect many usb devices, use an hub with additional
usb power.

```bash
sudo bash install.sh
```

Check if the installation worked fine:

```bash
bash check.sh
```

You will now see an ap called DIVERSA_NMEA; connect to it.


## Usage

After the system is set up, connect using your device to the new ap. Use 192.168.2.1 ip and port 10110 as TCP source.


