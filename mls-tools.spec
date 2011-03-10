Summary: Tools to run applications at specified MLS level
Name: mls-tools
Version: 0.0.1
Release: 1%{dist}
License: GPLv2
BuildArch: noarch
Group: Applications
URL: http://txtoth.dyndns.org
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: pygtk2
Requires: python >= 2.5
Requires: selinux-policy-mls mcstrans policycoreutils-newrole
Requires: pexpect
BuildRequires: policycoreutils

%description
mls-tools

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buiildroot}
make DESTDIR=%{buildroot} install

%post
%{__python} -c 'import compileall; compileall.compile_dir("%{_datadir}/%{name}", 1, "/", 1)' > /dev/null 
semodule -i %{_datadir}/%{name}/ml_launch.pp
#
#  restore context of files
#
/sbin/restorecon -R %{_datadir}/%{name}
[ $? -eq 0 ] || exit 1
/sbin/restorecon %{_bindir}/ml-launch
[ $? -eq 0 ] || exit 1


%postun
if [ $1 -eq 0 ]; then
   semodule -r ml_launch
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}/examples/*
%{_datadir}/%{name}/*.py
%{_datadir}/%{name}/*.glade
%{_datadir}/locale/en/LC_MESSAGES/mls-tools.mo
%{_datadir}/locale/ko/LC_MESSAGES/mls-tools.mo
%{_datadir}/locale/ja/LC_MESSAGES/mls-tools.mo
%{_datadir}/%{name}/*.pp
%{_datadir}/selinux/devel/include/admin/*.if
%{_mandir}/man1/ml-launch.1*
%defattr(755,root,root)
%{_bindir}/ml-launch
%{_datadir}/%{name}/label-dialog
%{_datadir}/%{name}/get-file-level
%{_datadir}/%{name}/check-dominance
%doc COPYING


%changelog
* Wed Jan 26 2011 tedx <tedx@localhost.localdomain> - mls-tools-1
- Initial build.

