#!/bin/sh

# Enable SoftAP hotspot

apt install -y --no-install-recommends hostapd

echo "interface wlan0" >> /etc/dhcpcd.conf
echo "static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf

cat <<'EOF' > /etc/hostapd/hostapd.conf
interface=wlan0
driver=nl80211
ssid=Raspberry Pi
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=raspberry
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' > /etc/default/hostapd
