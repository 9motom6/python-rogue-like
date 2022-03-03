class BaseComponent:

    def __init__(self, parent):
        self.parent = parent
    
    @property
    def engine(self):
        return self.gamemap.engine

    @property
    def gamemap(self):
        return self.parent.gamemap