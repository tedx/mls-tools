SUBDIRS = ml-launch po examples

INTLTOOL_FILES = \
  intltool-extract.in \
  intltool-merge.in \
  intltool-update.in

DISTCLEANFILES = \
  intltool-extract \
  intltool-merge \
  intltool-update \
  po/.intltool-merge-cache

clean:
	list='$(SUBDIRS)'; for subdir in $$list; do \
		test "$$subdir" = . || ($(am__cd) $$subdir && $(MAKE) $(AM_MAKEFLAGS) clean); \
	done
	rm -Rf autom4te.cache
	rm -f *.log
	rm -f *~
