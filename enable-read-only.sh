#!/bin/bash -e

# Disable swap file
dphys-swapfile swapoff
dphys-swapfile uninstall
systemctl disable dphys-swapfile.service

# Remove unwanted packages
apt-get remove -y --purge logrotate fake-hwclock

# Disable apt activities
systemctl disable apt-daily-upgrade.timer
systemctl disable apt-daily.timer
systemctl disable man-db.timer

# Move resolv.conf to /run
mv /etc/resolv.conf /run/resolvconf/resolv.conf
ln -s /run/resolvconf/resolv.conf /etc/resolv.conf

# Enable tmpfs /tmp and /var/tmp
echo -e "D /tmp 1777 root root -\nq /var/tmp 1777 root root -" > /etc/tmpfiles.d/tmp.conf
cp /usr/share/systemd/tmp.mount /etc/systemd/system/
systemctl enable tmp.mount

# Clean up /var
rm -rf /var/cache/apt /var/cache/debconf /var/lib/apt/lists

# Adjust kernel command line
sed -i.backup -e 's/rootwait$/rootwait fsck.mode=skip noswap ro systemd.volatile=state/' /boot/cmdline.txt

# Edit the file system table
sed -i.backup -e 's/vfat\s*defaults\s/vfat defaults,ro/; s/ext4\s*defaults,noatime\s/ext4 defaults,noatime,ro/' /etc/fstab
