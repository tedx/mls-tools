import selinux

def new_context():
    return ":::"

def get_raw_con(con):
    (rc, raw_con) = selinux.selinux_trans_to_raw_context(con)
    return raw_con

def get_raw_range(con):
    (rc, raw_con) = selinux.selinux_trans_to_raw_context(con)
    raw_con_range = raw_con.replace(":", " ", 3).split(" ")[3]
    return raw_con_range

def get_range(con):
    con_range = con.split(":")[3]
    return con_range

def get_level(con):
    range = con.split(":")[3]
    level = range.split("-")[0]
    return level

def get_role(con):
    return con.split(":")[1]

def get_user(con):
    return con.split(":")[0]

def get_type(con):
    return con.split(":")[2]

def set_range(con, range):
    con_array = con.split(":")
    con_array[3] = range
    con = ":".join(con_array)
    return con

def set_type(con, type):
    con_array = con.split(":")
    con_array[2] = type
    con = ":".join(con_array)
    return con

def set_user(con, user):
    con_array = con.split(":")
    con_array[0] = user
    con = ":".join(con_array)
    return con

def set_role(con, role):
    con_array = con.split(":")
    con_array[1] = role
    con = ":".join(con_array)
    return con

