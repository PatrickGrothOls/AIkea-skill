"""Scope: Route optional construction events without coupling builders to a viewer."""

from contextvars import ContextVar


class LiveBuildProgress:
    """An opt-in observer; ordinary builds have no display dependency."""

    current = ContextVar("aikea_live_build", default=None)

    def __init__(self, observer):
        self.observer = observer

    def __enter__(self):
        self.token = self.current.set(self.observer)
        return self

    def __exit__(self, *_error):
        self.current.reset(self.token)

    @classmethod
    def started(cls, spec):
        observer = cls.current.get()
        if observer:
            observer.started(spec)

    @classmethod
    def part(cls, spec, part):
        observer = cls.current.get()
        if observer:
            observer.part(spec, part)


class LiveBuildChild:
    """Supply a child's declared frame before its builder starts running."""

    def __init__(self, spec):
        self.spec = spec

    def __enter__(self):
        self.observer = LiveBuildProgress.current.get()
        if self.observer:
            self.observer.push(self.spec)

    def __exit__(self, *_error):
        if self.observer:
            self.observer.pop()
