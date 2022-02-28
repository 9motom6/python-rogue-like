class BaseComponent:

    def __init__(self, entity):
        self.entity = entity
    
    @property
    def engine(self):
        return self.entity.gamemap.engine