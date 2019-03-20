# coding : utf-8
class UnknownDatasetError(Exception):
    def __init__(self,message):
        self.message = message

class FetchError(Exception):
    def __init__(self,message):
        self.message = message

class LevelError(Exception):
    def __init__(self,message):
        self.message = message

class VariableError(Exception):
    def __init__(self,message):
        self.message = message

class ParameterError(Exception):
    def __init__(self,message):
        self.message = message

class AreaError(Exception):
    def __init__(self,message):
        self.message = message
