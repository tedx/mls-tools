import sys
import sys, traceback
from dominance import *
from selinux_login import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Error - no level given")
        sys.exit(2)

    try:
        user_range = get_range()
#        print("check_dominance: " +  sys.argv[1] + " " + user_range)
        if check_level_dominance2(user_range, sys.argv[1]):
            sys.exit(0)
        else:
            sys.exit("Dominance check failed")
    except Exception, ex:
        message = "Error checking dominance: %s : %s" % ( sys.exc_info()[0], traceback.format_exc())
        print >>sys.stderr, message
        sys.exit(message)
        
