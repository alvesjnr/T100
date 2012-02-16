class SimulationError(Exception):
    def __init__(self, message=None):
        self.message = message


class QueueError(Exception):
    def __init__(self, message=None):
        self.message=message

class Straggler(Exception):
    """Yes, it happens!"""