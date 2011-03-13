#!/bin/bash

replace_conf()
{
awk -v mime_type="$1" -v desktop="$2" 'BEGIN { found = 0; regex = sprintf("^%s=", mime_type) }
$0 ~ regex { printf("%s=%s\n", mime_type, desktop) }
$0 !~ regex { print $0 }
' /usr/share/applications/defaults.list > temp ; mv temp /usr/share/applications/defaults.list
}

if [ ! -f /usr/share/applications/defaults.list.orig ]
then
    cp /usr/share/applications/defaults.list /usr/share/applications/defaults.list.orig
fi

grep -q "application/vnd.oassis.opendocument.graphics" /usr/share/applications/defaults.list
if [ $? -eq 1 ]; then
   echo "application/vnd.oasis.opendocument.graphics=ml-oo-draw.desktop" >> /usr/share/applications/defaults.list
fi

replace_conf "application/vnd.ms-word" "ml-oo-writer.desktop" 
replace_conf "application/vnd.wordperfect" "ml-oo-writer.desktop"
replace_conf "application/vnd.sun.xml.writer" "ml-oo-writer.desktop"
replace_conf "application/vnd.sun.xml.writer.global" "ml-oo-writer.desktop"
replace_conf "application/vnd.stardivision.writer" "ml-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text" "ml-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-template" "ml-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-web" "ml-oo-writer.desktop"
replace_conf "application/vnd.oasis.opendocument.text-master" "ml-oo-writer.desktop"
replace_conf "application/vnd.ms-excel" "ml-oo-calc.desktop"
replace_conf "application/vnd.stardivision.calc" "ml-oo-calc.desktop"
replace_conf "application/vnd.sun.xml.calc" "ml-oo-calc.desktop"
replace_conf "application/vnd.sun.xml.calc.template" "ml-oo-calc.desktop"
replace_conf "application/vnd.oasis.opendocument.spreadsheet" "ml-oo-calc.desktop"
replace_conf "application/vnd.oasis.opendocument.spreadsheet-template" "ml-oo-calc.desktop"
replace_conf "application/vnd.ms-powerpoint" "ml-oo-impress.desktop"
replace_conf "application/vnd.stardivision.impress" "ml-oo-impress.desktop"
replace_conf "application/vnd.sun.xml.impress" "ml-oo-impress.desktop"
replace_conf "application/vnd.sun.xml.impress.template" "ml-oo-impress.desktop"
replace_conf "application/vnd.oasis.opendocument.presentation" "ml-oo-impress.desktop"
replace_conf "application/vnd.oasis.opendocument.presentation-template" "ml-oo-impress.desktop"
replace_conf "application/vnd.stardivision.draw" "ml-oo-draw.desktop"
replace_conf "application/vnd.sun.xml.draw" "ml-oo-draw.desktop"
replace_conf "application/vnd.sun.xml.draw.template" "ml-oo-draw.desktop"
replace_conf "application/vnd.oasis.opendocument.graphics" "ml-oo-draw.desktop"
replace_conf "application/vnd.oasis.opendocument.graphics-template" "ml-oo-draw.desktop"
replace_conf "application/pdf" "ml-evince.desktop"
replace_conf "application/postscript" "ml-evince.desktop"
replace_conf "application/x-dvi" "ml-evince.desktop"

cp ml-oo-calc.desktop /usr/share/applications
cp ml-oo-impress.desktop /usr/share/applications
cp ml-oo-draw.desktop /usr/share/applications
cp ml-oo-writer.desktop /usr/share/applications
