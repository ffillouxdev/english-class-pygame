class Counter:
    def __init__(self, count=0):
        self.count = count

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0
