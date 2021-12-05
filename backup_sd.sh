rm -rf ~/rpi_sail_station.img.tar.gz
sudo dd if=/dev/mmcblk0 of=~/rpi_sail_station.img bs=32M status=progress
tar -czvf ~/rpi_sail_station.img.tar.gz ~/rpi_sail_station.img
rm ~/rpi_sail_station.img