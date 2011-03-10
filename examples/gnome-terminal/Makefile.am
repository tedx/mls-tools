install-exec-local:
	mkdir -p $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal
	install -m 0644 $(srcdir)/ml-terminal.desktop $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal/
	install -m 0755 $(srcdir)/gnome-terminal-disable-factory $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal/
	install -m 0755 $(srcdir)/install.sh $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal/
	install -m 0755 $(srcdir)/uninstall.sh $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal/

uninstall-local:
	rm -fr $(DESTDIR)$(pkgdatadir)/examples/gnome-terminal
