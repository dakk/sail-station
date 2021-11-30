import socket 
import pynmea2

# Connect to tcp server localhost 10110
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 10110))

windspeed = 0
windangle = 0
watertemp = 0

f = None 

while True:
    data = s.recv().split('\n')

    for x in data:
        msg = pynmea2.parse(x)

        # If message is a GGA containing date and time, open a file
        if msg.sentence_type == 'GGA':
            if f is None:
                f = open('/home/pi/gpx/' + msg.timestamp.strftime('%Y%m%d_%H%M%S') + '.gpx', 'w')
                f.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
                f.write('<gpx version="1.1" creator="gpx_logger" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/1" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">\n')
                f.write('<trk>\n')
                f.write('<trkseg>\n')

            # If message is a GGA containing lat and lon, write to file
            if f and msg.latitude is not None and msg.longitude is not None:
                f.write('<trkpt lat="' + str(msg.latitude) + '" lon="' + str(msg.longitude) + '">\n')
                f.write('<ele>' + str(msg.altitude) + '</ele>\n')
                f.write('<time>' + msg.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ') + '</time>\n')
                f.write('</trkpt>\n')

        # If message contains wind information, set to ws and wt
        if msg.sentence_type == 'MWV':
            ws = msg.wind_speed
            wd = msg.wind_angle
        
        # If message contains water temperature, set to wa
        if msg.sentence_type == 'MTW':
            wa = msg.temperature


        print(msg)


