#!/bin/bash
# Make backups
sudo cp /etc/pam.d/newrole /etc/pam.d/newrole.orig
sudo cp /etc/pam.d/gdm /etc/pam.d/gdm.orig
sudo cp /etc/pam.d/gdm-autologin /etc/pam.d/gdm-autologin.orig
sudo cp /etc/pam.d/gdm-password /etc/pam.d/gdm-password.orig
sudo cp /etc/security/namespace.conf  /etc/security/namespace.conf.orig

#
sudo cp gdm /etc/pam.d
sudo cp gdm-password /etc/pam.d
sudo cp gdm-autologin /etc/pam.d
sudo cp newrole /etc/pam.d
sudo cp namespace.conf  /etc/security/namespace.conf

# Make polyinstantiation instance directories
mkdir ~/.dbus.inst
mkdir ~/.gconf.inst
chcon -t gconf_home_t .gconf.inst
mkdir ~/.gconfd.inst
chcon -t gconf_home_t .gconfd.inst
mkdir ~/.gnome2.isnt
chcon -t gnome_home_t .gnome2.inst
mkdir ~/.mozilla.inst
chcon -t mozilla_home_t .mozilla.inst
#mkdir ~/.metacity.inst
mkdir ~/.openoffice.org.inst

sudo mkdir /tmp.inst

# build and install the additional policy for examples to work
sudo make -f /usr/share/selinux/devel/Makefile
sudo semodule semodule -i mls-tools-example.pp
sudo rmdir tmp
