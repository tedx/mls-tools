VERSION=$(shell awk '/Version:/ { print $$2 }' mls-tools.spec)
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
	rm -f mls-tools*tar.gz

tarball: clean
	-tar --create --transform='s,^mls-tools,mls-tools-$(VERSION),' --show-transformed --file=mls-tools-$(VERSION).tar.gz --directory=.. -z --exclude-vcs --exclude=mls-tools-$(VERSION).tar.gz -v mls-tools

srpm: tarball
	mkdir -p ~/rpmbuild/SOURCES 
	mkdir -p ~/rpmbuild/SRPMS
	mv mls-tools-$(VERSION).tar.gz ~/rpmbuild/SOURCES
	rpmbuild -bs mls-tools.spec