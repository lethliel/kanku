# Install openvswitch and openvswitch-switch

'''zypper -n in openvswitch openvswitch-switch'''

# Enable and start openvswitch
'''
systemctl enable openvswitch
systemctl start openvswitch
'''

# Adept/Create libvirt network hook script

Please be aware that the location of the network hook script depends on your installation.

ATTENTION: The following command overwrites your local modifications in /etc/libvirt/hooks/network

Example:

'''
cat <<EOF > /etc/libvirt/hooks/network
#!/bin/bash

/usr/bin/perl /opt/kanku/bin/kanku-network-setup.pl \$@
EOF
chmod 755 /etc/libvirt/hooks/network
systemctl restart libvirtd.service

virsh net-define  dist/kanku-ovs.xml
virsh net-start kanku-ovs
virsh net-autostart kanku-ovs
'''
