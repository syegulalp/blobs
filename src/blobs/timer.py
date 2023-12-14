from time import perf_counter as clock


class Timer:
    def __init__(self):
        self.avg = 0.0

    def __enter__(self):
        self.start = clock()

    def __exit__(self, *a):
        self.total = clock() - self.start
        if not self.avg:
            self.avg = self.total
        self.avg = (self.avg + self.total) / 2


timer = Timer()

def output(*a):
    timer
    print("Loop time", timer.avg, "%", timer.avg / (1 / 60) * 100)