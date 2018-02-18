# Raspberry Pi Camera Import

These instructions transform a Raspberry Pi to an automatic headless photo import device for digital cameras.

## Features

When a digital camera is plugged in the USB port, all new photos are copied to the Pi's SD card automatically. Use a reasonably large SD card and build a headless photo backup device.

The files are stored in the home directory and ordered by file date (usually the capture date):

`/home/pi/Pictures/Sony_ILCE-7_xxxxxxxx/2018-02-13/DSC01234.arw`

This way, the chance of duplicates is reduced (see "Restrictions").

## Requirements

- Raspberry Pi (B+, 2, 3, Zero, Zero W) with a free USB port
- Raspbian Stretch Lite (tested with version 2017-11-29)
- Digital Camera with PTP [supported by gphoto2](http://gphoto.org/proj/libgphoto2/support.php)

## Installation

```
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y --no-install-recommends git

git clone https://github.com/nicokaiser/rpi-camera-import.git
cd rpi-camera-import

sudo ./install-camera-import.sh
```

### Read-only mode

This puts the Raspbian filesystem into read-only mode and only remounts it to read-write when a camera is connected. So you can just pull the power plug when copying is done.

```
sudo ./enable-read-only.sh
```

## Limitations

- This only works with cameras supported by gphoto2 and with PTP mode (not USB mass storage mode).
- There could theoretically be filename duplicates. That usually is, when more than 10.000 photos are taken with the same camera on the same day.
- For some cameras, udev cannot determine a serial number. E.g. the folder for any Canon EOS 400D is always `Canon_Inc._Canon_Digital_Camera`. This may only be a problem when importing from more than one camera.

## Optional Components

### Wi-Fi Access Point

Make the Raspberry Pi open a Wi-Fi Access Point, so you can connect to it with your mobile phone (any SSH client) and check the files that were imported.

```
sudo ./install-hotspot.sh
```

### Announce SSH service via Bonjour

To find the device's IP address, you can make it announce via Avahi (Bonjour). SSH clients like Prompt or Termius (iOS) can find the device in the same network:

```
sudo cp /usr/share/doc/avahi-daemon/examples/ssh.service /etc/avahi/services/ssh.service
```

### Disable Bluetooth and Audio

Since no Bluetooth and Audio support is needed, these can be disabled:

```
systemctl disable bluetooth.service
systemctl disable hciuart.service

echo "dtparam=audio=off" >> /boot/config.txt
echo "dtoverplay=pi3-disable-bt" >> /boot/config.txt
```
