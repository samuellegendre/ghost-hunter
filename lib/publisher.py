class Publisher:
    def __init__(self, events):
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, subscriber, callback):
        self.get_subscribers(event)[subscriber] = callback

    def unregister(self, event, subscriber):
        del self.get_subscribers(event)[subscriber]

    def dispatch(self, event):
        for subscriber, callback in self.get_subscribers(event).items():
            callback()
