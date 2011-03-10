import logging
import selinux
import pwd
import os

def get_range():
	user = pwd.getpwuid(os.getuid()).pw_name
	(rc, seuser, level) = selinux.getseuserbyname(user)
	logging.debug("get_range: " + user + " " + seuser + " " + level)
	return level

def get_trans_range():
	range = get_range()
	(rc, tcon) = selinux.selinux_raw_to_trans_context("a:b:c:" + range)
        context_array = tcon.split(":")
        range = context_array[3]
	return range
