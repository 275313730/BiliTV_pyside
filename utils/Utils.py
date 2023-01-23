from threading import Timer


class Utils:
    @staticmethod
    def set_timeout(ms: float, fn: callable, *args, **kwargs):
        t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
        t.start()
        return t
