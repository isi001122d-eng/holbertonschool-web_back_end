#!/usr/bin/env python3
"""Module for measuring runtime of async comprehensions."""

import asyncio
import time

async_comprehension = __import__(
    '1-async_comprehension'
).async_comprehension


async def measure_runtime() -> float:
    """Return total runtime for four parallel comprehensions."""
    start = time.perf_counter()

    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )

    return time.perf_counter() - start
