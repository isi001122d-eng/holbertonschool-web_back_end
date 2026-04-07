#!/usr/bin/env python3
"""Module for measuring runtime of async comprehensions."""

import asyncio
import time

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Return total runtime of 4 parallel async comprehensions."""
    start = time.perf_counter()

    await asyncio.gather(*[async_comprehension() for _ in range(4)])

    return time.perf_counter() - start
