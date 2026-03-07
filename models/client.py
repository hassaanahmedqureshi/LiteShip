class Client:
    def __init__(self, id=None, name=None, code=None):
        self.id = id
        self.name = name
        self.code = code

    def __repr__(self):
        return f"Client(id={self.id}, name = `{self.name}`, code=`{self.code}`)"