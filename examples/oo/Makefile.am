
install-exec-local:
	mkdir -p $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0644 $(srcdir)/ml-oo-calc.desktop $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/ml-oo-calc $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0644 $(srcdir)/ml-oo-draw.desktop $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/ml-oo-draw $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0644 $(srcdir)/ml-oo-impress.desktop $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/ml-oo-impress $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0644 $(srcdir)/ml-oo-writer.desktop $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/ml-oo-writer $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/install.sh $(DESTDIR)$(pkgdatadir)/examples/oo
	install -m 0755 $(srcdir)/uninstall.sh $(DESTDIR)$(pkgdatadir)/examples/oo

uninstall-local:
	rm -fr $(DESTDIR)$(pkgdatadir)/examples/oo
