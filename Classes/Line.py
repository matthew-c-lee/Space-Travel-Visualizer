class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y

        self.end_x = end_x
        self.end_y = end_y

        self.line = None

    def get_start_x(self):
        return self.start_x

    def get_start_y(self):
        return self.start_y

    def get_end_x(self):
        return self.end_x

    def get_end_y(self):
        return self.end_y