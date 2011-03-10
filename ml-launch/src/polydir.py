#!/usr/bin/env python
import os, os.path
import sys
import selinux
import md5
from context import *

def make_polydir_name(dir_name, context):
    (rc, dircon) = selinux.getfilecon(dir_name)
    if rc < 0:
        raise Exception("Error in getting directory context: %s " % (dir_name))
    context_array = dircon.split(":")
    # Only generate polyinstantiated name based on the level not the range
    context_array[3] = get_level(context)
    newcontext = ':'.join(context_array)
    (rc, full_dir) = selinux.selinux_trans_to_raw_context(newcontext)
    if rc < 0:
        raise Exception("Error translating context: %s " % (newcontext))
    m = md5.new()
    m.update(full_dir)
    return dir_name + ".inst/" + m.hexdigest()
    
def mkpolydir(dir_name, poly_dir_name, level):
        dir_context = None
        (rc, context) = selinux.getcon()
        if rc < 0:
            raise Exception("Error getting context.")
        rc = selinux.matchpathcon_init(None)
        if rc < 0:
            raise Exception("Error calling matchpathcon_init.")
        (rc, dir_context) = selinux.matchpathcon(dir_name, 0)
        selinux.matchpathcon_fini()
        if rc < 0:
            raise Exception("Error in matchpathcon for %s." % (dir_name))
        
        (rc, dir_context) = selinux.security_compute_create(context, dir_context, selinux.SECCLASS_FILE)
        if rc < 0:
            raise Exception("Error in security_compute_create context: %s directory context: %s" % (context, dir_context))
        
        context_array = dir_context.split(":")
        context_array[3] = level
        dir_context = ':'.join(context_array)
        rc = selinux.setfscreatecon(dir_context)
        if rc < 0:
            raise Exception("Error in setfscreatecon for %s %s." % (poly_dir_name, dir_context))
        try:
		if not os.path.isdir(poly_dir_name):
			os.mkdir(poly_dir_name)
	except (IOError, OSError), (errno, strerror):
		raise Exception("Error creating directory %s with context %s: %s %s" % (poly_dir_name, dir_context, errno, strerror))
