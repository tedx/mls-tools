import gtk

def error_dialog(message, use_threads=False):
	if use_threads:
		gtk.gdk.threads_enter()

        dialog = gtk.MessageDialog(
                parent         = None,
                flags          = gtk.DIALOG_MODAL,
                type           = gtk.MESSAGE_ERROR,
                buttons        = gtk.BUTTONS_OK,
                message_format = message)
        dialog.set_title("Error")
        dialog.set_default_response(gtk.RESPONSE_OK)
        dialog.run()
        dialog.destroy()
        gtk.gdk.flush()

	if use_threads:
		gtk.gdk.threads_leave()

                                
