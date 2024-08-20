from abc import ABC, abstractmethod
from typing import Any


class Coordinator(ABC):
    def __init__(self, backend: Any = None, pass_manager: Any = None):
        self.backend = backend
        self.pass_manager = pass_manager
    @abstractmethod
    def get_counts(self):
        pass
