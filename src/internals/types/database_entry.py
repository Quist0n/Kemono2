from abc import abstractmethod
from dataclasses import dataclass, fields

from typing import Dict
from src.internals.types import AbstractDataclass

@dataclass
class DatabaseEntry(AbstractDataclass):
    
    @classmethod
    def init_from_dict(cls, d: Dict):
        """
        Init a dataclass instance off a dictionary.
        """
        instance = cls(**{ key: value
            for key, value in d.items()
            if key in { i.name for i in fields(cls) }
        })
        return instance
    
    # @abstractmethod
    # def serialize():
    #     """
    #     Serialize python-specific property types.
    #     Mostly used for Redis caching.
    #     """
    #     pass
    
    # @abstractmethod
    # def deserialize():
    #     """
    #     Deserialize certain properties into python-specific types.
    #     Mostly for transforming the results returned by Redis cache.
    #     `Psycopg` already transforms between types where applicable.
    #     """
    #     pass
