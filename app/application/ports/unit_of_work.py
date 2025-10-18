from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

@abstractmethod
class IUnitOfWork(AbstractContextManager["IUnitOfWork"], ABC):
    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def rollback(self) -> None: ...
