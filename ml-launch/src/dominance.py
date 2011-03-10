import logging
import selinux

SECCLASS_CONTEXT = selinux.string_to_security_class("context")
CONTEXT__CONTAINS = selinux.string_to_av_perm(SECCLASS_CONTEXT, "contains")

(rc, dom_context) = selinux.getcon()
(rc, dom_raw_context) = selinux.selinux_trans_to_raw_context(dom_context)

def check_level_dominance2(level1, level2, debug=False):
    context_array = dom_context.split(":")
    context_array[3] = level1
    level1_con = ':'.join(context_array)
    context_array[3] = level2
    level2_con = ':'.join(context_array)
    return check_dominance2(level1_con, level2_con, debug)

def check_level_dominance(level, debug=False):
    context_array = dom_context.split(":")
    context_array[3] = level
    con = ':'.join(context_array)
    if debug:
        logging.debug("check_level_dominance: %s" % (con))
    return check_dominance(con, debug)

def check_dominance(con, debug=False):
    (rc, raw_con) = selinux.selinux_trans_to_raw_context(con)
    if rc != 0:
        raise Exception("selinux.selinux_trans_to_raw_context failed: %d" % rc)
 
    avd = selinux.av_decision()
    selinux.avc_reset()
    if debug:
        logging.debug("check_dominance: %s %s" % (dom_raw_context, raw_con))
    rc = selinux.security_compute_av_raw(dom_raw_context, raw_con, SECCLASS_CONTEXT, CONTEXT__CONTAINS, avd)
    if rc < 0:
        raise Exception("selinux.security_compute_av_raw failed")
    if (avd.allowed & CONTEXT__CONTAINS) == CONTEXT__CONTAINS:
        if debug:
            logging.debug("check_dominance: returned True")
        return True
    else:
        if debug:
            logging.debug("check_dominance: returned False")
        return False

def check_dominance2(con1, con2, debug=False):
    (rc, raw_con1) = selinux.selinux_trans_to_raw_context(con1)
    (rc, raw_con2) = selinux.selinux_trans_to_raw_context(con2)

    avd = selinux.av_decision()
    selinux.avc_reset()
    if debug:
        logging.debug("check_dominance2: " + raw_con1 + " " + raw_con2)
    rc = selinux.security_compute_av_raw(raw_con1, raw_con2, SECCLASS_CONTEXT, CONTEXT__CONTAINS, avd)
    if rc < 0:
        raise Exception("selinux.security_compute_av_raw failed")
    if (avd.allowed & CONTEXT__CONTAINS) == CONTEXT__CONTAINS:
        return True
    else:
        return False


#if __name__ == "__main__":
#    print check_dominance("user_u:user_r:user_t:CONFIDENTIAL")
#    print check_level_dominance("CONFIDENTIAL")
