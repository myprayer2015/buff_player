import time
class TimeUtils:
    time_start = 0
    time_stop = 0
    single_time_ms = 0
    all_time_ms = 0
    def __init__(self) -> None:
        self.time_start = int(round(time.time() * 1000))
        pass

    def start(self):
        self.time_start = int(round(time.time() * 1000))

    def stop(self):
        self.time_stop = int(round(time.time() * 1000))
        self.single_time_ms = self.time_stop - self.time_start
        self.all_time_ms += self.single_time_ms

    def get_single_time_ms(self):
        return self.single_time_ms
    
    def get_all_time_ms(self):
        return self.all_time_ms