#!/usr/bin/env python3
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
import sys
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args"
        method: The method being decorated.

    Returns:
        The wrapped method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that adds the input parameters of a method to a
    list in Redis and stores its output into another list.

    Args:
        method: The method being decorated.

    Returns:
        The wrapped method.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper for the decorated method """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    Cache class that stores data in Redis & provides retrieval methods
    """


    def __init__(self):
        """
        Initializes the Redis client and flushes the database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores the input data in Redis with a randomly generated key

        Args:
            data to be stored. Can be of type str, bytes, int, or float

        Returns:
            The randomly generated key used to store the data
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        Retrieves the stored data from Redis & may apply a conversion function.

        Args:
            key: The key used to retrieve the data from Redis.
            fn: Optional conversion function to apply to the retrieved data.

        Returns:
            The retrieved data, may be converted based on d given conversion func
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """get a number"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Retrieves a UTF-8 string from Redis.

        Args:
            key: The key used to retrieve the data from Redis.

        Returns:
            The retrieved data as a UTF-8 string.
        """
        return self.decode("utf-8")
