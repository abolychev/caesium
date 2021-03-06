import os, codecs, time, base64, hashlib

def get_echo_length(echo):
    if os.path.exists("echo/" + echo):
        echo_length = len(open ("echo/" + echo, "r").read().split("\n")) - 1
    else:
        echo_length = 0
    return echo_length

def get_echocount(echoarea):
    return len(open("echo/" + echoarea, "r").read().split("\n")) - 1

def save_to_favorites(msgid, msg):
    if os.path.exists("echo/favorites"):
        favorites = open("echo/favorites", "r").read().split("\n")
    else:
        favorites = []
    if not msgid in favorites:
        open("echo/favorites", "a").write(msgid + "\n")
        return True
    else:
        return False

def get_echo_msgids(echo):
    if os.path.exists("echo/" + echo):
        msgids = open("echo/" + echo, "r").read().split("\n")[:-1]
    else:
        msgids = []
    return msgids

def get_carbonarea():
    try:
        msgids = []
        for msgid in open("echo/carbonarea", "r").read().split("\n"):
            if len(msgid) == 20:
                msgids.append(msgid)
        return msgids
    except:
        return []

def add_to_carbonarea(msgid, msgbody):
    if os.path.exists("echo/carbonarea"):
        return codecs.open("echo/carbonarea", "a", "utf-8").write(msgid + "\n")
    else:
        return []

def save_to_carbonarea(fr, subj, body):
    msgbody = ["ii/ok", "carbonarea", str(round(time.time())), fr, "local", "", subj, "", body]
    msgid = base64.urlsafe_b64encode(hashlib.sha256("\n".join(msgbody).encode()).digest()).decode("utf-8").replace("-", "A").replace("_", "z")[:20]
    codecs.open("msg/%s" % msgid, "w", "utf-8").write("\n".join(msgbody))
    open("echo/carbonarea", "a").write(msgid + "\n")

def save_message(raw, node, to):
    try:
        carbonarea = get_carbonarea()
    except:
        carbonarea = []
    for msg in raw:
        msgid = msg[0]
        msgbody = msg[1]
        codecs.open("echo/" + msgbody[1], "a", "utf-8").write(msgid + "\n")
        codecs.open("msg/" + msgid, "w", "utf-8").write("\n".join(msgbody))
        if to:    
            for name in to:
                if name in msgbody[5] and not msgid in carbonarea:
                    add_to_carbonarea(msgid, msgbody)

def get_favorites_list():
    try:
        msgids = []
        for msgid in open("echo/favorites", "r").read().split("\n"):
            if len(msgid) == 20:
                msgids.append(msgid)
        return msgids
    except:
        return []

def remove_from_favorites(msgid):
    favorites_list = get_favorites_list()
    favorites_list.remove(msgid)
    open("echo/favorites", "w").write("\n".join(favorites_list))

def remove_echoarea(echoarea):
    try:
        echoarea = open("echo/%s" % echoarea, "r").read().split("\n")
    except:
        echoarea = []
    for msgid in echoarea:
        try:
            os.remove("msg/%s" % msgid)
        except:
            None
    try:
        os.remove("echo/%s" % echoarea)
    except:
        None


def read_msg(msgid, echoarea):
    size = "0b"
    if os.path.exists("msg/" + msgid) and msgid != "":
        msg = open("msg/" + msgid, "r").read().split("\n")
        size = os.stat("msg/" + msgid).st_size
        if size < 1024:
            size = str(size) + " B"
        else:
            size = str(format(size / 1024, ".2f")) + " KB"
    else:
        msg = ["", "", "", "", "", "", "", "", "Сообщение отсутствует в базе"]
    return msg, size
