import sys
from selinux import *
import selinux

def get_file_level(file_name):
    try:
        context = selinux.getfilecon(file_name)
        context_array = context[1].split(":")
        range = context_array[3]
        range_array = range.split("-")
        level = range_array[0]
    except Exception, ex:
        return "Cancel - getting file level for %s exception: %s" % (file_name, ex)

    return level

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stdout.write("Cancel - no file name given")
        sys.exit(-1)

    sys.stdout.write(get_file_level(sys.argv[1]))
