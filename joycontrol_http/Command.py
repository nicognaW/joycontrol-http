class Command:
    def __init__(self, target: str, cmd: str, obj: object = None):
        self.target = target
        self.cmd = cmd
        self.obj = obj
