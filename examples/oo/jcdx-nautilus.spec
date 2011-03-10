Summary: JCDX extensions to Nautilus
Name: jcdx-nautilus
Version: 0.0.6
Release: 2%{dist}
URL: http://www.jcdx.org
License: GPL
Group: User Interface/Desktops
BuildRoot: %{_topdir}/BUILD

BuildRequires: python
Requires: python >= 2.0
Requires: jcdx-base
Requires(post): jcdx-base
Requires: jcdx-config-poly
Requires: nautilus-python >= 0.5.1-2
Requires: GConf2

%description
JCDX extensions to Nautilus

%post
. /opt/jcdx/bin/config-edit-functions

replace_conf()
{
awk -v mime_type="$1" -v desktop="$2" 'BEGIN { found = 0; regex = sprintf("^%s=", mime_type) }
$0 ~ regex { printf("%s=%s\n", mime_type, desktop) }
$0 !~ regex { print $0 }
' /usr/share/applications/defaults.list > temp ; mv temp /usr/share/applications/defaults.list
}

grep -q "application/vnd.oassis.opendocument.graphics" /usr/share/applications/defaults.list
if [ $? -eq 1 ]; then
   echo "application/vnd.oasis.opendocument.graphics=jcdx-oo-draw.desktop" >> /usr/share/applications/defaults.list
fi

replace_conf "application/vnd.ms-word" "jcdx-oo-writer.desktop" 
replace_conf "application/vnd.wordperfect" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.sun.xml.writer" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.sun.xml.writer.global" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.stardivision.writer" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-template" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-web" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-master" "jcdx-oo-writer.desktop"
replace_conf "application/vnd.ms-excel" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.stardivision.calc" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.sun.xml.calc" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.sun.xml.calc.template" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.oasis.opendocument.spreadsheet" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.oasis.opendocument.spreadsheet-template" "jcdx-oo-calc.desktop"
replace_conf "application/vnd.ms-powerpoint" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.stardivision.impress" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.sun.xml.impress" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.sun.xml.impress.template" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.oasis.opendocument.presentation" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.oasis.opendocument.presentation-template" "jcdx-oo-impress.desktop"
replace_conf "application/vnd.stardivision.draw" "jcdx-oo-draw.desktop"
replace_conf "application/vnd.sun.xml.draw" "jcdx-oo-draw.desktop"
replace_conf "application/vnd.sun.xml.draw.template" "jcdx-oo-draw.desktop"
replace_conf "application/vnd.oasis.opendocument.graphics" "jcdx-oo-draw.desktop"
replace_conf "application/vnd.oasis.opendocument.graphics-template" "jcdx-oo-draw.desktop"
replace_conf "application/pdf" "jcdx-evince.desktop"
replace_conf "application/postscript" "jcdx-evince.desktop"
replace_conf "application/x-dvi" "jcdx-evince.desktop"

add_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-calc"           "jcdx-poly-app"
add_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-draw"           "jcdx-poly-app"
add_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-impress"           "jcdx-poly-app"
add_newrole_pam_conf "/usr/bin/nautilus"           "jcdx-poly-app"
add_newrole_pam_conf "/usr/bin/evince"           "jcdx-poly-app"

if [ ! -d /etc/skel/Desktop ]; then
   mkdir -p /etc/skel/Desktop
fi

gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/nautilus/preferences/default_folder_viewer list_view
gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type list --list-type string --set /apps/nautilus/list_view/default_visible_columns "[name,size,type,date_modified,level]"
gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type list --list-type string --set /apps/nautilus/list_view/default_column_order "[name,size,type,date_modified,level]"

 %{__python} -c "import compileall; compileall.compile_dir('/usr/lib64/nautilus/extensions-2.0/python', 1)" > /dev/null 2>&1

semodule -i /opt/jcdx/policy/jcdx_nautilus_helper.pp
[ $? -eq 0 ] || exit 1

restorecon -R /etc/selinux/mls/modules
[ $? -eq 0 ] || exit 1

restorecon -R /opt/jcdx/bin/processdirs
[ $? -eq 0 ] || exit 1

restorecon -R /opt/jcdx/bin/processfiles
[ $? -eq 0 ] || exit 1

restorecon -R /usr/lib64/nautilus/extensions-2.0/python
[ $? -eq 0 ] || exit 1

%postun
if [ $1 -eq 0 ]; then
   . /opt/jcdx/bin/config-edit-functions
   remove_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-calc"
   remove_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-impress"
   remove_newrole_pam_conf "/opt/jcdx/bin/jcdx-oo-draw"
   remove_newrole_pam_conf "/usr/bin/nautilus"
   remove_newrole_pam_conf "/usr/bin/evince"
   rm -Rf /etc/skel/Desktop
   gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type string --set /apps/nautilus/preferences/default_folder_viewer icon_view
   gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type list --list-type string --set /apps/nautilus/list_view/default_visible_columns "[name,size,type,date_modified]"
   gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.defaults --type list --list-type string --set /apps/nautilus/list_view/default_column_order "[name,size,type,date_modified]"

   semodule -r jcdx_nautilus_helper
   restorecon -R /etc/selinux/mls/modules
   rm -f /usr/lib64/nautilus/extensions-2.0/python/jcdx_menu.pyc
   rm -f /usr/lib64/nautilus/extensions-2.0/python/level_column.pyc
fi

%files
%defattr (0755,root,root)
/opt/jcdx/bin/jcdx-oo-writer
/opt/jcdx/bin/jcdx-oo-calc
/opt/jcdx/bin/jcdx-oo-draw
/opt/jcdx/bin/jcdx-oo-impress
/opt/jcdx/bin/jcdx-evince
/opt/jcdx/bin/processdirs
/opt/jcdx/bin/processfiles
%defattr(-,root,root)
%{_libdir}/nautilus/extensions-2.0/python/level_column.py
%{_libdir}/nautilus/extensions-2.0/python/jcdx_menu.py
/usr/share/applications/jcdx-oo-writer.desktop
/usr/share/applications/jcdx-oo-calc.desktop
/usr/share/applications/jcdx-oo-draw.desktop
/usr/share/applications/jcdx-oo-impress.desktop
/usr/share/applications/jcdx-evince.desktop
/usr/share/applications/nautilus.desktop
%defattr(644,root,root)
/opt/jcdx/policy/jcdx_nautilus_helper.pp
/opt/jcdx/bin/processfiles.py

%changelog
* Fri Oct 17 2008 tedx <tedx@comms> - 0.0.1-1
- Initial version.
