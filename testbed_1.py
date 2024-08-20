from abc import ABC, abstractmethod

class AbstractBackend(ABC):
    @property
    @abstractmethod
    def backend(self):
        """
        抽象属性，子类需要实现这个属性。
        """
        pass

# 示例子类
class ConcreteBackend(AbstractBackend):
    def __init__(self, backend_instance):
        self._backend_instance = backend_instance

    @property
    def backend(self):
        """
        实现抽象属性，返回具体的后端实例。
        """
        return self._backend_instance

# 使用示例
backend_instance = ConcreteBackend("my_backend_instance")
print(backend_instance.backend)
