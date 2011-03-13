#!/bin/bash
# Restore the  backups
if [ -f /etc/pam.d/newrole.orig ];
then
    sudo mv -f /etc/pam.d/newrole.orig /etc/pam.d/newrole
fi
if [ -f /etc/pam.d/gdm.orig ];
then
    sudo mv -f /etc/pam.d/gdm.orig /etc/pam.d/gdm
fi
if [ -f /etc/pam.d/gdm-autologin.orig ];
then
    sudo mv -f /etc/pam.d/gdm-autologin.orig /etc/pam.d/gdm-autologin
fi
if [ -f /etc/pam.d/gdm-password.orig ];
then
    sudo mv -f /etc/pam.d/gdm-password.orig /etc/pam.d/gdm-password
fi
if [ -f /etc/security/namespace.conf.orig ];
then
    sudo mv -f /etc/security/namespace.conf.orig  /etc/security/namespace.conf
fi


#uninstall the added policy
sudo semodule -r mls-tools-example

sudo sh -c "cd oo; ./uninstall.sh"
sudo sh -c "cd firefox; ./uninstall.sh"
sudo sh -c "cd gnome-terminal; ./uninstall.sh"

echo "Log out and after logging back in run:"
echo "/usr/share/mls-tools/examples/uninstall-poly.sh"
echo "to clean up polyinstantiated directories."
