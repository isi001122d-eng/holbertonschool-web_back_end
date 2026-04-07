#!/usr/bin/env python3
"""Module that defines an async generator."""

import asyncio
import random
from typing import AsyncGenerator


async def async_generator() -> AsyncGenerator[float, None]:
    """Yield 10 random numbers asynchronously."""
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
