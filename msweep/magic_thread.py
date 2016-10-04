
import threading


def threaded(f):
    def rv(*args, **kwargs):
        t = threading.Thread(target=f, args=(args), kwargs=kwargs)
        t.daemon = True
        t.start()
    return rv




