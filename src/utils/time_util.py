import time
class TimeUtil:
    time_start = 0
    time_stop = 0
    single_time_ms = 0
    all_time_ms = 0
    counter = 0
    def __init__(self) -> None:
        self.time_start = int(round(time.time() * 1000))
        pass

    def start(self):
        self.time_start = int(round(time.time() * 1000))
        self.counter += 1

    def stop(self):
        self.time_stop = int(round(time.time() * 1000))
        self.single_time_ms = self.time_stop - self.time_start
        self.all_time_ms += self.single_time_ms

    def get_single_time_ms(self):
        return self.single_time_ms
    
    def get_all_time_ms(self):
        return self.all_time_ms

    def get_avg_time_ms(self):
        if self.counter > 0:
            return self.all_time_ms * 1.0 / self.counter
        else:
            return 0

    def get_current_time(self):
        return round(time.time() * 1000)