
def screen(uid, uname, text, gid="me"):
    r = "[{} ({}) -> {}]: {}".format(uid, uname, gid, text)
    print(r)
