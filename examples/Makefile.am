SUBDIRS = firefox gnome-terminal oo

mls-tools-example.pp: mls-tools-example.te mls-tools-example.if mls-tools-example.fc
	make -f /usr/share/selinux/devel/Makefile

install-exec-local: mls-tools-example.pp
	mkdir -p $(DESTDIR)$(pkgdatadir)/examples
	install -m 0644 $(srcdir)/mls-tools-example.pp $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/mls-tools-example.te $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/mls-tools-example.if $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/mls-tools-example.fc $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/namespace.conf $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/newrole $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/gdm $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/gdm-autologin $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0644 $(srcdir)/gdm-password $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0755 $(srcdir)/install.sh $(DESTDIR)$(pkgdatadir)/examples/
	install -m 0755 $(srcdir)/uninstall.sh $(DESTDIR)$(pkgdatadir)/examples/

uninstall-local:
	rm -fr $(DESTDIR)$(pkgdatadir)/examples/

clean:
	list='$(SUBDIRS)'; for subdir in $$list; do \
		test "$$subdir" = . || ($(am__cd) $$subdir && $(MAKE) $(AM_MAKEFLAGS) clean); \
	done
