#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])
AC_INIT([mls-tools], [0.0.1])
AM_INIT_AUTOMAKE

# Checks for programs.
AC_PROG_LN_S
AC_PROG_INSTALL
AC_PROG_INTLTOOL
AM_PATH_PYTHON([2.5],, [:])

# ============== take care of some localization ======
AH_TEMPLATE([GETTEXT_PACKAGE], [Package name for gettext])
GETTEXT_PACKAGE=mls-tools # note that this is a command
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE")
AC_SUBST(GETTEXT_PACKAGE)
ALL_LINGUAS="en ja ko"
AM_GLIB_GNU_GETTEXT

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([Makefile
                 ml-launch/Makefile
		 ml-launch/src/Makefile
		 examples/Makefile
		 examples/oo/Makefile
		 examples/gnome-terminal/Makefile
		 examples/firefox/Makefile
		 po/Makefile.in])
AC_OUTPUT
