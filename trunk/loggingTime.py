"""Сейчас файл не используется."""

from datetime import datetime


# Singleton class for time checking (debug only)
class LogTime(object):
    """Класс для контроля времени. (Надо решить, нужен ли он нам)"""
    instance = None

    def __new__(cls, enabled=True):
        if cls.instance is None:
            cls.instance = super(LogTime, cls).__new__(cls)
            cls.enabled = enabled
            cls._start_time = datetime.now()
        return cls.instance

    # dict_words<string, int> must be already 'sorted'.
    def __init__(self, enabled=True):
        self.enabled = enabled
        self._start_time = datetime.now()

    def start(self) -> None:
        if self.enabled is False:
            pass

        self._start_time = datetime.now()

    def stop(self, hint: str = "") -> None:
        if self.enabled is False:
            pass

        print(str(datetime.now() - self._start_time) + '\'s ' + hint)
