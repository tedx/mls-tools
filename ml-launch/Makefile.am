SUBDIRS = src

ml_launch.pp: ml_launch.te ml_launch.if ml_launch.fc
	make -f /usr/share/selinux/devel/Makefile

install-exec-local: ml_launch.pp
	mkdir -p $(DESTDIR)$(bindir) $(DESTDIR)$(pkgdatadir) $(DESTDIR)$(datadir)/selinux/devel/include/admin $(DESTDIR)$(mandir)/man1
	install -m 0644 $(srcdir)/ml_launch.if $(DESTDIR)$(datadir)/selinux/devel/include/admin/
	install -m 0644 $(srcdir)/ml_launch.pp $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/ml-launch.1 $(DESTDIR)$(mandir)/man1
	install -m 0755 $(srcdir)/check-dominance $(DESTDIR)$(pkgdatadir)/
	install -m 0755 $(srcdir)/get-file-level $(DESTDIR)$(pkgdatadir)/
	install -m 0755 $(srcdir)/label-dialog $(DESTDIR)$(pkgdatadir)/
	install -m 0755 $(srcdir)/ml-launch $(DESTDIR)$(bindir)/

uninstall-local:
	rm -fr $(DESTDIR)$(bindir) $(DESTDIR)$(pkgdatadir) $(DESTDIR)$(datadir)/selinux/devel/include/admin $(DESTDIR)$(mandir)/man1

clean:
	list='$(SUBDIRS)'; for subdir in $$list; do \
		test "$$subdir" = . || ($(am__cd) $$subdir && $(MAKE) $(AM_MAKEFLAGS) clean); \
	done
	rm -f *~
	rm -f ./#*
	rm -Rf tmp
