#!/usr/bin/env python
import logging
import sys, traceback
import gtk
import gtk.glade
import gobject
import mcstrans
import threading
import math
import gconf
import os
import os.path
#import locale
import getopt
from selinux import *
from odict import OrderedDict
import cPickle as pickle
import copy
import warnings
warnings.filterwarnings('ignore', category=Warning)
from jcdx.dominance import *
from jcdx import *

DOMAIN = "label-dialog"
import gettext
_ = lambda x: gettext.ldgettext(DOMAIN, x)
import __builtin__
__builtin__.__dict__['_'] = _

gtk.glade.bindtextdomain (DOMAIN)
gtk.glade.textdomain(DOMAIN)

preserve_environment = True

def getSensitivity(domain, context, debug=False):
    if debug:
        print("getSensitivity: %s" % context)
    range = context.split(":")[3]
    clearance = range.split("-")[len(range.split("-"))-1]
    if debug:
        print("getSensitivity: %s" % clearance)

    # Put all of the levels in list and sort them by length
    levels = copy.copy(domain.sensitivities.values())
    for key in domain.baseClassifications.keys():
        for sensitivity in domain.baseClassifications[key].sensitivities.values():
            levels.append(sensitivity)
    levels.sort( lambda a,b:-cmp(len(a),len(b)) )

    found_level = None
    for level in levels:
        if clearance.startswith(level):
            found_level = level
            break
    
    if debug:
        print "getSensitivity: %s" % found_level

    return found_level

(rc, context) = selinux.getcon()
if rc < 0:
#    print >>sys.stderr, "Error getting context"
    error_dialog("Failed to get process context, exiting")
    sys.exit(-1)

try:
    history_file_name = polydir.make_polydir_name(os.environ['HOME'] + "/.mlrc", context) + "/label-dialog.history"
    try:
            src = open(history_file_name, "a")
            src.close()
    except:
        history_file_name = os.environ['HOME'] + "/.mlrc/label-dialog.history"
except Exception, ex:
#    print >>sys.stderr, ex
    error_dialog("Error creating history file: %s : %s" % ( sys.exc_info()[0], traceback.format_exc()))
    
class Label:
    def __init__(self, domain):
        self.level = ""
        self.domain = domain
        self.codewords = OrderedDict()
        for key in self.domain.groups.keys():
            self.codewords[key] = []
        self.handEdited = False

    def addCodeWord(self, group, word):
        if self.handEdited == False:
            self.codewords[group.name].append(word)

    def removeCodeWord(self, group, word):
        if self.handEdited == False:
            self.codewords[group.name].remove(word)

    def setLevel(self, level):
        self.level = level

    def isWordSelected(self, group, codeword):
        if self.handEdited:
            return False
        else:
#        print >>sys.stderr, "isWordSelected %s group %s" % (codeword, group.name)
            codewords = self.codewords[group.name]
            try:
                if codewords.index(codeword) > -1:
                    return True
            except ValueError:
                return False

    def str(self):
        str = self.level
        if self.handEdited == False:
            for key in self.codewords.keys():
                group = self.domain.groups[key]
                codewords = self.codewords[key]
                if len(codewords) > 0:
                    if len(group.prefixes) > 0:
                        str = str + " " + group.prefixes[0]
                firstCodeWord = True
                for codeword in codewords:
                    if firstCodeWord == False:
                        if group.join != "":
                            str = str + group.join
                        else:
                            str = str + " "
                    else:
                        str = str + " "
                    str = str + codeword
                    firstCodeWord = False
                if len(codewords) > 0:
                    if len(group.suffixes) > 0:
                        str = str + " " + group.suffixes[0]
#        print >>sys.stderr, "Label.str %s" % (str)
        return str
        
    def __str__(self):
        str = ""
        str = str + "Level: %s\n" % (self.level)
        if self.handEdited == False:
            for key in self.codewords.keys():
                group = self.domain.groups[key]
                str = str + "group: %s\n" % (group.name)
                codewords = self.codewords[key]
                if len(codewords) > 0:
                    if len(group.prefixes) > 0:
                        str = str + "prefix: %s\n" % (group.prefixes[0])
                if group.join != "":
                    str = str + "join: %s\n" % (group.join)

                for codeword in codewords:
                    str = str + "codeword: %s\n" % (codeword)

                if len(codewords) > 0:
                    if len(group.suffixes) > 0:
                        str = str + "suffix: %s\n" % (group.suffixes[0])
        return str

    def handEdited(self):
        if self.handEdited == False:
            self.level = self.str()
            self.handEdited = True


def parse(domain, label, debug):
    if debug:
        print "parse label %s" % label
    context = "a:b:c:" + label
    (rc, raw) = selinux_trans_to_raw_context(context)
    if raw == context:
        error_dialog("Label parsing error at %s" % ( label ))
        return None
    
    (rc, context) = selinux_raw_to_trans_context(raw)

    label = context.lstrip("a:b:c:")
    if debug:
        print "parse transformed label %s" % label

    # Put all of the levels in list and sort them by length
    levels = copy.copy(domain.sensitivities.values())
    for key in domain.baseClassifications.keys():
        for sensitivity in domain.baseClassifications[key].sensitivities.values():
            levels.append(sensitivity)
    levels.sort( lambda a,b:-cmp(len(a),len(b)) )

    found_level = None
    for level in levels:
        if label.startswith(level):
            found_level = level
            break

    if found_level == None:
        error_dialog("Label parsing error at %s" % ( label ))
        return None

    labelObj = Label(domain)
    labelObj.setLevel(found_level)

    label = label[len(found_level):]
    label = label.lstrip()
    
    while len(label) > 0:
        label_len = len(label)
        for group in domain.groups.values():
            if len(group.prefixes) > 0:
                prefixes = copy.copy(group.prefixes)
                prefixes.sort( lambda a,b:-cmp(len(a),len(b)) )
                matched_prefix = False
                for prefix in prefixes:
                    if label.startswith(prefix + " "):
                        if debug:
                            print "matched prefix %s" % prefix
                        label = label[len(prefix):]
                        label = label.lstrip()
                        matched_prefix = True
                if not matched_prefix:
                    continue

            codewords = copy.copy(group.wordDict.values())
            codewords.sort( lambda a,b:-cmp(len(a.word),len(b.word)) )
            codeword_found = True
            while codeword_found:
                codeword_found = False
                for codeword in codewords:
                    if label.startswith(codeword.word):
                        if debug:
                            print "matched word %s" % codeword.word
                        label = label[len(codeword.word):]
                        label = label.lstrip()
                        labelObj.addCodeWord(group, codeword.word)
                        # if there is a join character and it is the next character
                        # remove it
                        if group.join != "":
                            if debug:
                                print "group join character %s %s" % (group.join, label[0:1])
                            if label[0:1] == group.join:
                                label = label[1:]
                        if debug:
                            print "next character %s" % (label[0:1])
                        codeword_found = True

            if len(group.suffixes) > 0:
                suffixes = copy.copy(group.suffixes)
                suffixes.sort( lambda a,b:-cmp(len(a),len(b)) )
                for suffix in suffixes:
                    if label.startswith(suffix):
                        label = label[len(suffix):]
                        label = label.lstrip()
        # Was anything comsumed this time round?
        if len(label) == label_len:
            break

    if label != "":
        error_dialog("Label parsing error at %s" % ( label ))
        return None

    if debug:
        logging.debug(str(labelObj))
    return labelObj
        

class WordDialog:

    def dialogClose(self, dialog):
        self.dialogWindow.hide()
        return True

    def close(self, dialog, foo):
        dialog.hide_all()
        return True

    def __init__(self, gladeFile, label, debug):
        self.debug = debug
        if self.debug:
            print("WordDialog.__init__: %s" % gladeFile);
        if os.access (gladeFile, os.F_OK):
            self.tree = gtk.glade.XML(gladeFile, domain="label-dialog")
        else:
            self.tree = gtk.glade.XML("/usr/share/ml-launch/" + gladeFile, domain="label-dialog")
        if self.debug:
            print("WordDialog.__init__: ", self.tree);
        closeButton = self.tree.get_widget('closeButton')
        closeButton.connect('clicked', self.dialogClose)
        self.dialogWindow = self.tree.get_widget('wordDialog')
        self.dialogWindow.connect('close', self.close)
        self.dialogWindow.connect('delete_event', self.close)
        self.table = None
        self.previouslyUsedTable = None
        self.entry = None
        self.group = None
        self.label = label

    def show(self, *args):
        self.dialogWindow.show()

    def destroy(self):
        self.dialogWindow.destroy()
        gtk.gdk.flush()

    def calc_dimensions(self, length):
        x = math.sqrt(length)
        y = int(x)
# Work out a reasonable size for the popup dialog
        if y == 1:
            columns = 1
            rows = length
        if x-y == 0:
            rows = y
            columns = y
        else:
            rows = y
            columns = y+2

        return rows,columns

# Add a checkbox for each 'word' to the table.
    def populate(self, group, entry):
        if self.debug:
            logging.debug("WordDialog.populate");
        self.entry = entry
        self.group = group
        self.dialogWindow.set_title(self.group.name)

        (rows, columns) = self.calc_dimensions(len(group.wordDict.values()))

        if self.table == None:
            self.table = gtk.Table(rows, columns)
            self.tree.get_widget('dialog-hbox1').add(self.table)
            self.table.show()
        else:
            self.table.resize(rows, columns)

        used_codewords = self.group.get_used_codeword()
        unused_codewords = self.group.get_unused_codeword()
# Populate the table with check buttons one for each 'word'
        for i in range(rows):
            for j in range(columns):
                codeword = None
                try:
                    codeword = used_codewords.next()
                except StopIteration:
                    try:
                        codeword = unused_codewords.next()
                    except StopIteration:
                        return

                self.label.addCodeWord(self.group, codeword.word)
                context = "a:b:c:" + self.label.str()
                self.label.removeCodeWord(self.group, codeword.word)
                (rc, raw) = selinux_trans_to_raw_context(context)
                button = gtk.CheckButton(codeword.word, False)
                if codeword.comment != None:
                    tooltip = gtk.Tooltips()
                    tooltip.set_tip(button, codeword.comment)
                if codeword.used:
                    label = button.get_child()
                    label.set_markup("<b>" + codeword.word + "</b>");
                self.table.attach(button, i, i+1, j, j+1)
                if self.label.isWordSelected(self.group, codeword.word):
                    button.set_active(True)
                button.connect("toggled", self.entry_toggle_editable)
                if context == raw:
                    button.set_sensitive(False)
                button.show()

# Handler for the 'word' checkbox click events
    def entry_toggle_editable(self, checkbutton):
        if checkbutton.get_active() == True:
# 'word' checkbox selected. Add the word to the level string in the entry field.
            self.label.addCodeWord(self.group, checkbutton.get_label())
        else:
# 'word' checkbox deselected. Remove the word from the level string in 
# the entry field
            self.label.removeCodeWord(self.group, checkbutton.get_label())
        self.entry.set_text(self.label.str())


class LabelDialog(gobject.GObject):
    __gsignals__ = {
        "selection-cancelled" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        "selected" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, [gobject.TYPE_STRING]),
        }

    def dialogClose(self, dialog):
        if self.debug:
            logging.debug("dialogClose")
        self.emit("selection-cancelled")
        gtk.main_quit()
        return True

    def close(self, dialog, foo):
        if self.debug:
            logging.debug("close")
        sys.stdout.write("Cancel")
        gtk.main_quit()
        return True

    def open(self):
        if self.debug:
            print("open")
        self.show()
        gtk.gdk.threads_init()
        gtk.gdk.threads_enter()
        gtk.main()
        gtk.gdk.threads_leave()

    def destroy(self):
        if self.debug:
            logging.debug("destroy")
        self.dialogWindow.hide()
        self.dialogWindow.destroy()
        gtk.gdk.flush()
        gtk.main_quit()
        return True
        
    def __init__(self, title, debug):
        gobject.GObject.__init__(self)
        self.debug = debug
        if self.debug:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(levelname)s %(message)s %(filename)s',
                                filename='/tmp/ml-launch.log',
                                filemode='w')
        try:
            mcstrans.process_file("/etc/selinux/mls/setrans.conf", False)
        except Exception, ex:
            if debug:
                print traceback.format_exc()
            error_dialog("Error read mcstrans configuration data.")
            sys.exit(-1)
        self.domain = mcstrans.domains["Military Message"]
        if debug:
            print "__init__ call getSensitvity"
        try:
            self.sensitivity = getSensitivity(self.domain, context, debug)
        except:
            print("Error : %s : %s" % ( sys.exc_info()[0], traceback.format_exc()))

        self.init_preferences()

        self.widgets = OrderedDict()
        dialog = gtk.Dialog('Build Label')
        self.widgets['launchLevelDialog'] = dialog
        cancel = dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_NONE)
        self.widgets['cancelButton'] = cancel
        ok = dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_NONE)
        self.widgets['okButton'] = ok
        dialog.set_default_size(400,140)
        table = gtk.Table(4,2,False)
        levelcomboboxentry = gtk.combo_box_entry_new_text()
        self.widgets['levelComboBoxEntry'] = levelcomboboxentry
        table.attach(levelcomboboxentry, 1, 2, 0, 1, yoptions=0)
        levelcomboboxentry.show()
        separator1 = gtk.HSeparator()
        table.attach(separator1, 1, 2, 1, 2, yoptions=0)
        separator1.show()
        levelcombobox = gtk.combo_box_new_text()
        self.widgets['levelComboBox'] = levelcombobox
        table.attach(levelcombobox, 1, 2, 2, 3, yoptions=0)
        levelcombobox.show()
        groupcombobox = gtk.combo_box_new_text()
        self.widgets['groupComboBox'] = groupcombobox
        table.attach(groupcombobox, 1, 2, 3, 4, yoptions=0)
        groupcombobox.show()

        labellabel = gtk.Label("Label")
        table.attach(labellabel, 0, 1, 0, 1, xoptions=0, yoptions=0)
        labellabel.show()
        separator2 = gtk.HSeparator()
        table.attach(separator2, 0, 1, 1, 2, xoptions=gtk.FILL, yoptions=0)
        separator2.show()
        levellabel = gtk.Label("Level")
        table.attach(levellabel, 0, 1, 2, 3, xoptions=0, yoptions=0)
        levellabel.show()
        grouplabel = gtk.Label("Words")
        table.attach(grouplabel, 0, 1, 3, 4, xoptions=0, yoptions=0)
        grouplabel.show()

        table.show()
        dialog.vbox.pack_start(table)
        self.dialogWindow = self.widgets['launchLevelDialog']
        self.title = title
        self.label = Label(self.domain)
        self.wordDialog = None
        self.run()

    def run ( self ):
        if self.title:
            if self.debug:
                logging.debug(_("title %s") % (self.title))
            self.dialogWindow.set_title(self.title)

        closeButton = self.widgets['cancelButton']
        closeButton.connect('clicked', self.dialogClose)
        self.okButton = self.widgets['okButton']
        self.okButtonHandlerId = self.okButton.connect('clicked', self.Ok)
        self.dialogWindow.connect('close', self.close)
        self.dialogWindow.connect('delete_event', self.close)
        self.dialogWindow.set_position(gtk.WIN_POS_MOUSE)

# Populate the levels combobox
        self.levels_combobox = self.widgets['levelComboBox']
        self.levels_combobox.set_tooltip_text("Select level for new label.")
        for key in self.domain.sensitivities.keys():
            if self.domain.sensitivities[key].find("-") == -1:
                if self.debug:
                    print("%s %s" % (self.sensitivity, self.domain.sensitivities[key]))
                if check_level_dominance2(self.sensitivity, self.domain.sensitivities[key]):
                    self.levels_combobox.append_text(self.domain.sensitivities[key])
        for key in self.domain.baseClassifications.keys():
            for sensitivity in self.domain.baseClassifications[key].sensitivities.keys():
                if check_level_dominance2(self.sensitivity, self.domain.baseClassifications[key].sensitivities[sensitivity]):
                    self.levels_combobox.append_text(self.domain.baseClassifications[key].sensitivities[sensitivity])
        self.levels_combobox.connect("changed", self.level_selection_changed )

# Populate the group combobox
        self.groups_combobox = self.widgets['groupComboBox']
        self.groups_combobox.set_tooltip_text("Set words on new label.")    
        for key in self.domain.groups.keys():
            self.groups_combobox.append_text(key)

        self.groups_combobox.connect("changed", self.group_selection_changed )
        self.groups_combobox.connect('button-press-event', self.on_cb_clicked)
        self.groups_combobox.set_sensitive(False)
        self.groups_combobox.show()

# Load history

        self.history = OrderedDict()
        self.load_history(True)
# Populate the 
        self.history_combobox = self.widgets['levelComboBoxEntry']
        self.history_combobox.set_tooltip_text("History list of previously used labels.")
        for label in self.history.keys():
            if check_level_dominance(label, False):
                self.history_combobox.append_text(label)
        self.history_combobox.connect("changed", self.history_selection_changed )
        self.entry = self.widgets['levelComboBoxEntry'].child
        self.entry.connect("delete-text", self.delete_text, self)
        self.entry.connect("insert-text", self.insert_text, self)
        self.history_combobox.show()
        self.label = Label(self.domain)
        self.wordDialog = None
        self.build_used_codeword_list()

        
    def build_used_codeword_list(self, debug=False):
        for label in self.history.keys():
            labelObj = self.history[label]
            for key in self.domain.groups.keys():
                group = self.domain.groups[key]
                if debug:
                    print "group: ", group
                codewords = labelObj.codewords[key]
                if len(codewords) > 0:
                    for codeword in codewords:
                        if debug:
                            print "codeword: ", codeword
                        for cw in group.wordDict.values():
                            if cw.word == codeword:
                                cw.used = True


    def load_pickle_iter(self, src):
        while 1:
            try:
                yield pickle.load(src)
            except EOFError:
                break

    def delete_text(self, editable, start, end, dialog):
#        print >>sys.stderr, "delete %d %d" % (start, end)
        if start != end and start != 0:
            dialog.switch_to_validate(dialog.okButton)

    def insert_text(self, editable, new_text, length, pos, dialog):
#        print >>sys.stderr, "insert %d" % (length)
        if length == 1:
            dialog.switch_to_validate(dialog.okButton)

    def switch_to_validate(self, okButton):
        if okButton.get_label() != "Validate":
            okButton.set_label("Validate")
            okButton.disconnect(self.okButtonHandlerId)
            self.okButtonHandlerId  = okButton.connect('clicked', self.validate_label)

    def switch_to_ok(self):
        if self.okButton.get_label() != "Ok":
            self.okButton.set_label("Ok")
            self.okButton.disconnect(self.okButtonHandlerId)
            self.okButtonHandlerId  = self.okButton.connect('clicked', self.Ok)

    def validate_label(self, widget):
        self.entry.set_text(self.entry.get_text().upper())
        label = parse(self.domain, self.entry.get_text(), self.debug)
        if label != None:
            self.entry.set_text(label.str())
            if not check_level_dominance(label.str(), self.debug):
                error_dialog("Invalid label")
                return
            context = "a:b:c:" + label.str()
            (rc, raw) = selinux_trans_to_raw_context(context)
            if raw == context:
                error_dialog("Invalid label")
                return
            self.label = label
            self.set_sensitivity_level()
            self.switch_to_ok()

    def save_history(self, debug=False):
        global history_file_name
        try:
            os.remove(history_file_name)
        except:
            pass

        try:
            src = open(history_file_name, "w")
            i = 0
            iter = self.history.iterkeys()
            count = len(self.history)
#            if debug:
#                print "history length %d" % count
            while i <= self.saved_labels_max and i < count:
                key = iter.next()
                if debug:
                    print "save ",self.history[key]
                pickle.dump(self.history[key], src)
#                    print >>sys.stderr, self.history[key]
                i = i + 1
            src.close()
        except:
            error_dialog("Error saving history: %s : %s" % ( sys.exc_info()[0], traceback.format_exc()))
            return

    def load_history(self, debug=False):
        try:
            src = open(history_file_name, "r")
            for obj in self.load_pickle_iter(src):
#                print >>sys.stderr, str(obj)
#                if not check_level_dominance(obj.str(), debug):
#                    continue
                # Don't load invalid labels
                context = "a:b:c:" + obj.str()
                (rc, raw) = selinux_trans_to_raw_context(context)
                if raw == context:
                    continue
                self.history[obj.str()] = obj
#                if debug:
#                    print "history length %d" % len(self.history)
        except Exception, ex:
            print "exception", ex
            return

    def show(self, *args):
        self.dialogWindow.show()

    def on_cb_clicked(self):
        print >>sys.stderr, "combobox clicked"

    def level_selection_changed( self, selection ):
        index = selection.get_active()
        if self.debug:
            print("level_selection_changed: %s" % (selection.get_model()[index][0]))
        self.label.setLevel(selection.get_model()[index][0])
        self.set_entry_level()

        if self.debug:
            print "set active -1"
        self.groups_combobox.set_active(-1)
        if self.domain.findSensitivityByName(selection.get_model()[index][0]) == None:
            self.groups_combobox.set_sensitive(True)
        else:
            self.groups_combobox.set_sensitive(False)
        self.switch_to_ok()

    def set_entry_level(self):
        entry = self.widgets['levelComboBoxEntry'].child
        if self.debug:
            logging.debug("set_entry_level %s" % (self.label.str()))
        entry.set_text(self.label.str())

    def history_selection_changed( self, selection ):
        index = selection.get_active()
        if index != -1:
            self.label = copy.deepcopy(self.history[selection.get_model()[index][0]])
            self.set_entry_level()
            self.set_sensitivity_level()
        return True

    def test_level(self, model, path, iter, user_data):
        if user_data == model.get_value(iter, 0):
            self.levels_combobox.set_active(path[0])
            return True

    def set_sensitivity_level(self):
        # find the index of the sensitivity level
        model = self.levels_combobox.get_model()
        model.foreach(self.test_level, self.label.level)

    def group_popup( self, widget, data=None):
        if self.debug:
            print "popup"
        widget.set_active(-1)


    def group_selection_changed( self, selection ):
        index = selection.get_active()
        if self.debug:
            print("LabelDialog.group_selection_changed %d" % index);
        if index == -1:
            return
        if self.wordDialog != None:
            self.wordDialog.destroy()
# Reset the level entry field
        if self.debug:
            print("Create WordDialog");
        try:
            self.wordDialog = WordDialog("codeword.glade", self.label, self.debug)
            self.wordDialog.populate(self.domain.groups[selection.get_model()[index][0]], self.widgets['levelComboBoxEntry'].child)
            self.wordDialog.show()
            selection.set_active(-1)
        except:
            error_dialog("LabelDialog.group_selection_changed: %s : %s" % ( sys.exc_info()[0], traceback.format_exc()))
            
        return True

    def Ok( self, widget ):
        rc = 0
        entry = self.widgets['levelComboBoxEntry'].child
        self.label = parse(self.domain, entry.get_text(), self.debug)
        
        if self.label == None:
            return

        if entry.get_text() != "":
            self.load_history(True)
            if self.history.has_key(self.label.str()):
                del self.history[self.label.str()]
            if self.debug:
                print "add %s to histrory" % self.label.str()
            self.history.insert(0, self.label.str(), self.label)

            self.save_history()
            if self.debug:
                logging.debug("emit selected")
            self.emit('selected', self.label.str())
#            gtk.main_quit()
    #
    # If the current users doesn't have any preferences establish
    # a default set.
    #
    def init_preferences(self):
        try:
            self.preferences = gconf.client_get_default()
            self.saved_labels_max = self.preferences.get_int("/apps/label-dialog/saved_labels_max")
            if self.saved_labels_max == None or self.saved_labels_max == 0:
                self.saved_labels_max = 20
                self.preferences.set_int("/apps/label-dialog/saved_labels_max", self.saved_labels_max)
        except:
            self.saved_labels_max = 20
            
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

def selected(dialog, level):
    sys.stdout.write(level)
    gtk.main_quit()

def cancelled(dialog):
    sys.stdout.write("Cancel")
    gtk.main_quit()
    

def label_dialog():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:dh", ["title=","debug", "help"])
    except getopt.GetoptError:
        error_dialog( _("An error occurred while processing command line arguments."))
        print "usage: label-dialog [--title=<window title> --debug --help]"
        sys.exit(-1)
    
    title = None
    debug = False
    argptr = 0
    for o, a in opts:
        if o in ("-t", "--title"):
            title = a
            argptr = argptr + 1
        if o in ("-d", "--debug"):
            debug = True
            argptr = argptr + 1
        if o in ("-h", "--help"):
            error_dialog("usage: label-dialog [--title=<window title> --debug] <command> <command arguments ...>")
            sys.exit(-1)

    launchLevelDialog = LabelDialog(title, debug)
    launchLevelDialog.connect("selected", selected)
    launchLevelDialog.connect("selection-cancelled", cancelled)
    launchLevelDialog.open()


if __name__ == "__main__":
    label_dialog()
