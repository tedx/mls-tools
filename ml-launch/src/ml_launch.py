#!/usr/bin/env python
import logging
import sys, traceback
import gtk
import os
import os.path
import gettext
import getopt
import selinux
from selinux import *
import pwd
import time
import subprocess
import signal
from dominance import *
from selinux_login import *

#
# Added because of GTK warning about assertion failure "text != NULL" from gtk_entry_set_text
# the source of which was not apparent.
#
import warnings
warnings.filterwarnings('ignore', category=Warning)
 	
DOMAIN = "ml-launch"
import gettext
_ = lambda x: gettext.ldgettext(DOMAIN, x)
import __builtin__
__builtin__.__dict__['_'] = _

preserve_environment = True
cmd = None
args = None
debug = False

def error_dialog(message):
    dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_MODAL,
        type           = gtk.MESSAGE_INFO,
        buttons        = gtk.BUTTONS_OK,
        message_format = message)
    dialog.set_title(_("Error"))
    dialog.set_default_response(gtk.RESPONSE_OK)
    dialog.run()
    dialog.destroy()
    gtk.gdk.flush()
        
def password_dialog(ui):
    dialog = gtk.MessageDialog(
        parent         = None,
        flags          = gtk.DIALOG_MODAL,
        type           = gtk.MESSAGE_QUESTION,
        buttons        = gtk.BUTTONS_OK_CANCEL,
        message_format = _("You are attempting to run a command which requires you to reauthenticate."))

    dialog.vbox.get_children()[0].get_children()[0].set_from_file("/usr/share/pixmaps/password.png")
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    dialog.set_title(_("Query"))
    table = gtk.Table(2, 1)
    label = gtk.Label(_("Password "))
    entry = gtk.Entry()
    entry.set_activates_default(True)
    entry.set_visibility(False)
    table.attach(label, 0, 1, 0, 1) 
    table.attach(entry, 1, 2, 0, 1) 
    dialog.vbox.pack_start(table)
    dialog.show_all()
    response = dialog.run()
    if response == gtk.RESPONSE_CANCEL:
        sys.exit(0)
    password = entry.get_text()
    dialog.hide()
    dialog.destroy()
    gtk.gdk.flush()
    return password

#
# internal "newrole"
#
#     Returns:  0 - Success, -1 - Failure
#

def newrole(context, program, args, ui):
    global debug
    newrole = "/usr/bin/newrole"
    if debug:
        print >>sys.stderr, ("program: %s\nargs: %s") % (program, args)
    for arg in args:
        program = program + " " + arg

    if context.find("-") == -1:
        context = context + "-" + context

    if preserve_environment:
        progargs = ["-l", context, "-p", "--", "-c", program]
    else:
        progargs = ["-l", context, "--", "-c", program]

    if debug:
#        logging.debug(_("%s %s") % (newrole, progargs))
        print >>sys.stderr, ("%s %s") % (newrole, progargs)

    import pexpect
    try:
        child = pexpect.spawn(newrole, progargs)
    except:
        print >>sys.stderr, "traceback: %s" % (traceback.format_exc())
        print >>sys.stderr, "exception: %s" % (sys.exc_info()[0])
        return -1

    while True:
        val = child.expect([_("Authenticating .*"), _("Password: "), "newrole:.*", "\n", pexpect.TIMEOUT, pexpect.EOF, _(".* is not a valid context"), _(".* you are not allowed to change levels on a non secure terminal"), "Error dropping capabilities,*"])
        if debug:
#            logging.debug("ml-launch.py: %s" % (child.after))
            print >> sys.stderr, ("ml-launch.py: %s" % (child.after))
            print >> sys.stderr, ("ml-launch.py: %d" % (val))

        if val == 0:
            if ui != None:
                ui.hide()
                gtk.gdk.flush()
            continue
        elif val == 1:
            password = password_dialog(ui)
            child.sendline(password)
            if ui != None:
                ui.hide()
                gtk.gdk.flush()
            continue
        elif val == 2:
            error_dialog("%s" % (child.after))
            child.close()
            sys.exit(child.exitstatus)
#            return -1
        elif val == 3:
            if debug:
                logging.debug("ml-launch.py: pexpect timeout")
            if ui != None:
                ui.hide()
                gtk.gdk.flush()
            continue
        elif val == 4:
            break
        elif val == 5:
            break
        elif val >= 6:
            error_dialog("%s" % (child.after))
            child.close()
            sys.exit(child.exitstatus)
#            return -1

    if child.isalive():
        if ui != None:
            ui.destroy()
            gtk.gdk.flush()
        try:
            child.wait()
        except:
            sys.exit(child.exitstatus)
#            sys.exit(0)

    else:
        if child.before != "":
            error_dialog("%s" % (child.before))
            child.close()
            sys.exit(child.exitstatus)
#            return -1

    child.close()
    sys.exit(child.exitstatus)
#   return 0

def newrole_execv(context, program, args, dont_background):
    global debug
    newrole = "/usr/bin/newrole"
    if debug:
        print >>sys.stderr, ("program: %s\nargs: %s") % (program, args)
    for arg in args:
        program = program + " " + arg
        
    if context.find("-") == -1:
        context = context + "-" + context

    if preserve_environment:
        if dont_background:
            progargs = [newrole, "-l", context, "-p", "--", "-c", program]
        else:
            progargs = [newrole, "-l", context, "-p", "--", "-c", program + " &"]
    else:
        if dont_background:
            progargs = [newrole, "-l", context, "--", "-c", program]
        else:
            progargs = [newrole, "-l", context, "--", "-c", program + " &"]

    if debug:
        print >>sys.stderr, (_("%s %s") % (newrole, progargs))
    try:
        os.execv(newrole, progargs)
    except e:
        print >>sys.stderr, _("Failed to exec new process: %d (%s)") % (e.errno, e.strerror)
        sys.exit(e.errno)

def selected(dialog, level):
    global cmd, args, debug
    if debug:
        logging.debug("destroy level dialog %s" % (dialog))
    dialog.destroy()
    newrole(level, cmd, args, None)

def cancelled(dialog):
    gtk.main_quit()
    
def get_file_level(file_name):
    global debug
    p = subprocess.Popen(["/usr/share/mls-tools/get-file-level", file_name], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    level = p.communicate()[0].strip()
    if debug:
        logging.debug("file-level: %s" % (level))
    if level.startswith == "Cancel":
        error_dialog("Error getting file level for %s" % file_name)
        sys.exit(1)
    print("file-level: %s %s" % (file_name, level))
    if check_level_dominance(level):
        error_dialog("ml-launch: attempting to run a command at a level beyond your clearance.")
        sys.exit(1)
    return level

def check_level_dominance(level):
    print "check_level_dominance: " + level
    return subprocess.call(["/usr/share/mls-tools/check-dominance", level])


def main():
    global preserve_environment, cmd, args, debug
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:m:t:cdnuf:shb", ["level=", "max-level-or-clearance=", "title=","current-level", "debug", "no-environment", "use-execv", "file-level=", "selinux-user-range", "clearance", "dont-background"])
    except getopt.GetoptError:
        error_dialog( _("An error occurred while processing command line arguments."))
        print "usage: ml-launch [--level=<level> --max-level-or-clearance=<level> --title=<window title> --current-level --debug --no-environment --use-execv --file-level=<file name> --selinux-user-range --clearance --dont-background] <command> <command arguments ...>"
        sys.exit(-1)

    if len(args) == 0:
        error_dialog("usage: ml-launch [--level=<level>] [--max-level-or-clearance=<level>] [--title=<window title>] [--debug] [--no-environment] [--use-execv] [--current-level] [--file-level=<file name>] [--selinux-user-range] [--clearance] {--dont-background] <command> <command arguments ...>")
        sys.exit(-1)
    
    level = None
    title = None
    use_execv = False
    dont_background = False
    argptr = 0
    for o, a in opts:
        if o in ("-l", "--level"):
            if level == None:
                level = a
            else:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            argptr = argptr + 1
        elif o in ("-b", "--dont-background"):
            dont_background = True
            argptr = argptr + 1
        elif o in ("-t", "--title"):
            title = a
            argptr = argptr + 1
        elif o in ("-f", "--file-level"):
            if level == None:
                level = get_file_level(a)
                if level.startswith("Cancel"):
                    error_dialog("ml-launch: error getting file level for %s" % level.split(" - ")[1])
                    sys.exit(-1)
            else:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            argptr = argptr + 1
        elif o in ("-d", "--debug"):
            debug = True
            argptr = argptr + 1
        elif o in ("-n", "--no-environment"):
            preserve_environment = False
            argptr = argptr + 1
        elif o in ("-u", "--use-execv"):
            use_execv = True
            argptr = argptr + 1
        elif o in ("-c", "--current-level"):
            if level != None:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            (rc, context) = selinux.getcon()
            context_array = context.split(":")
            range = context_array[3]
            range_array = range.split("-")
            level = range_array[0]
            argptr = argptr + 1
        elif o in ("-s", "--selinux-user-range"):
            if level != None:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            user = pwd.getpwuid(os.getuid()).pw_name
            (rc, seuser, level) = selinux.getseuserbyname(user)
            (rc, tcon) = selinux_raw_to_trans_context("a:b:c:" + level)
            context_array = tcon.split(":")
            level = context_array[3]
            argptr = argptr + 1
        elif o in ("-h", "--clearance"):
            if level != None:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            user_range = get_trans_range()
            range_array = user_range.split("-")
            level = range_array[1]
            argptr = argptr + 1
        elif o in ("-m", "--max-level-or-clearance"):
            if level != None:
                error_dialog("ml-launch: use only one level setting command argument")
                sys.exit(-1)
            level = a
            # if the users clearance doesn't dominate the specified level use the clearance
            if check_level_dominance(level):
                user_range = get_trans_range()
                range_array = user_range.split("-")
                level = range_array[1]
            argptr = argptr + 1
        else:
            error_dialog("usage: ml-launch [--level=<level>] [--max-level-or-clearance=<level>] [--title=<window title>] [--debug] [--no-environment] [--use-execv] [--current-level] [--file-level=<file name>] [--selinux-user-range] [--clearance] [--dont-background] <command> <command arguments ...>")
            sys.exit(-1)

    cmd = sys.argv[argptr+1]
    args = sys.argv[argptr+2:]
    if debug:
        print >>sys.stderr, ("cmd: %s\nargc: %s") % (cmd, args)

    signal.signal(signal.SIGCLD, signal.SIG_DFL)

    if level == None:
        p = subprocess.Popen(["/usr/share/mls-tools/label-dialog"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        level = p.communicate()[0].strip()
        if debug:
            logging.debug("label-dialog: %s" % (level))
        if level == "Cancel":
            sys.exit(1)

    if check_level_dominance(level):
        error_dialog("ml-launch: attempting to run a command at a level beyond your clearance.")
        sys.exit(1)

    if dont_background:
        pid = 0
    else:
        try:
            pid = os.fork()
        except e:
            print >>sys.stderr, _("Failed to fork new process: %d (%s)") % (e.errno, e.strerror)
            sys.exit(1)
        
    if not pid:
        if debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(levelname)s %(message)s %(filename)s',
                                filename='/tmp/ml-launch.log',
                                filemode='w')

        if use_execv:
            return newrole_execv(level, cmd, args, dont_background)
        else:
            return newrole(level, cmd, args, None)

if __name__ == "__main__":
    main()
