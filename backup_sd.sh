sudo dd if=/dev/mmcblk0 of=rpi_sail_station.img bs=4M status=progress
tar -czvf rpi_sail_station.img.tar.gz rpi_sail_station.img