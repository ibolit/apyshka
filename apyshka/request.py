class Request:
    def __init__(self):
        self.url = None


    def __bool__(self):
        return bool(self.url)


    def __str__(self):
        return self.url
