#!/bin/bash
# Make backups
if [ ! -f /etc/pam.d/newrole.orig ];
then
    sudo cp /etc/pam.d/newrole /etc/pam.d/newrole.orig
fi
if [ ! -f /etc/pam.d/gdm.orig ];
then
    sudo cp /etc/pam.d/gdm /etc/pam.d/gdm.orig
fi
if [ ! -f /etc/pam.d/gdm-autologin.orig ];
then
    sudo cp /etc/pam.d/gdm-autologin /etc/pam.d/gdm-autologin.orig
fi
if [ ! -f /etc/pam.d/gdm-password.orig ];
then
    sudo cp /etc/pam.d/gdm-password /etc/pam.d/gdm-password.orig
fi
if [ ! -f /etc/security/namespace.conf.orig ];
then
    sudo cp /etc/security/namespace.conf  /etc/security/namespace.conf.orig
fi
#
sudo cp gdm /etc/pam.d
sudo cp gdm-password /etc/pam.d
sudo cp gdm-autologin /etc/pam.d
sudo cp newrole /etc/pam.d
sudo cp namespace.conf  /etc/security/namespace.conf

# Make polyinstantiation instance directories
if [ ! -d ~/.dbus.inst ];
then
    mkdir ~/.dbus.inst
fi
if [ ! -d ~/.gconf.inst ];
then
    mkdir ~/.gconf.inst
    chcon -t gconf_home_t ~/.gconf.inst
fi
if [ ! -d ~/.gconfd.inst ];
then
    mkdir ~/.gconfd.inst
    chcon -t gconf_home_t ~/.gconfd.inst
fi
if [ ! -d ~/.gnome2.isnt ];
then
    mkdir ~/.gnome2.inst
    chcon -t gnome_home_t ~/.gnome2.inst
fi
if [ ! -d ~/.mozilla.inst ];
then
    mkdir ~/.mozilla.inst
    chcon -t mozilla_home_t ~/.mozilla.inst
fi
#mkdir ~/.metacity.inst
if [ ! -d ~/.openoffice.org.inst ];
then
    mkdir ~/.openoffice.org.inst
fi
if [ ! -d /tmp.inst ];
then
    sudo mkdir /tmp.inst
fi

# build and install the additional policy for examples to work
sudo make -f /usr/share/selinux/devel/Makefile
sudo semodule -i mls-tools-example.pp
sudo rm -Rf tmp

sudo sh -c "cd oo; ./install.sh"
sudo sh -c "cd firefox; ./install.sh"
sudo sh -c "cd gnome-terminal; ./install.sh"

echo "Log out and then back in again to enable directory polyinstantiation."
echo "When you are done experimenting with the examples run uninstall.sh to uninstall."