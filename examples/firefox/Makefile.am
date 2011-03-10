
install-exec-local:
	mkdir -p $(DESTDIR)$(pkgdatadir)/examples/firefox
	install -m 0644 $(srcdir)/ml-firefox.desktop $(DESTDIR)$(pkgdatadir)/examples/firefox
	install -m 0755 $(srcdir)/ml-firefox $(DESTDIR)$(pkgdatadir)/examples/firefox
	install -m 0755 $(srcdir)/install.sh $(DESTDIR)$(pkgdatadir)/examples/firefox
	install -m 0755 $(srcdir)/uninstall.sh $(DESTDIR)$(pkgdatadir)/examples/firefox

uninstall-local:
	rm -fr $(DESTDIR)$(pkgdatadir)/examples/firefox
