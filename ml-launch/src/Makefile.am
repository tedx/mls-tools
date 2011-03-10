PYTHON_FILES = \
	check_dominance.py \
	mcstrans.py \
	odict.py \
	label_dialog.py \
	get_file_level.py \
	ml-launch.py

GLADE_FILES = codeword.glade ml-launch.glade

EXTRA_DIST = $(PYTHON_FILES) $(GLADE_FILES)

execdir = $(bindir)

gladedir = $(pkgdatadir)
glade_DATA = $(GLADE_FILES)

install-exec-local:
	mkdir -p $(DESTDIR)$(pkgdatadir)
	install -m 0644 $(srcdir)/ml_launch.py $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/get_file_level.py $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/label_dialog.py $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/odict.py $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/check_dominance.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/mcstrans.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/dominance.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/selinux_login.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/context.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/polydir.py  $(DESTDIR)$(pkgdatadir)/
	install -m 0644 $(srcdir)/error_dialog.py  $(DESTDIR)$(pkgdatadir)/

uninstall-local:
	rm -fr $(DESTDIR)$(pkgdatadir)

docs:
	cd $(srcdir)
	python @PYDOC@ -w $(PYTHON_FILES)

pycheck:
	pychecker -F $(top_srcdir)/pycheckrc $(PYTHON_FILES)

clean:
	rm -f *.pyo *.pyc
	rm -f ${BUILT_SOURCES}
