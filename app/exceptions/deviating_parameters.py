class DeviatingParametersError(Exception):
    def __init__(self, parameters):
        self.parameters = parameters
        super().__init__(f"Out of range parameters: {self.parameters}")
