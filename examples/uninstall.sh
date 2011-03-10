#!/bin/bash
# Restore the  backups
sudo mv /etc/pam.d/newrole.orig /etc/pam.d/newrole
sudo mv /etc/pam.d/gdm.orig /etc/pam.d/gdm
sudo mv /etc/pam.d/gdm-autologin.orig /etc/pam.d/gdm-autologin
sudo mv /etc/pam.d/gdm-password.orig /etc/pam.d/gdm-password
sudo mv /etc/security/namespace.conf.orig  /etc/security/namespace.conf

# Remove the polyinstantiation instance directories
rm -Rf ~/.dbus.inst
rm -Rf ~/.gconf.inst
rm -Rf ~/.gconfd.inst
rm -Rf ~/.gnome2.isnt
rm -Rf ~/.mozilla.inst
#rm -Rf ~/.metacity.inst
rm -Rf ~/.openoffice.org.inst

sudo rm -Rf /tmp.inst

#uninstall the added policy
sudo semodule -r mls-tools-example