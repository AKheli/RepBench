import time
class Timer:

    def __init__(self):
        self.total_time = 0
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def pause(self):
        assert self.start_time is not None
        self.total_time += time.time()-self.start_time
        self.start_time = None

    def get_time(self):
        if self.start_time is not None:
            return self.total_time +time.time()-self.start_time
        else:
            return self.total_time