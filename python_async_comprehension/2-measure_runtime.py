#!/usr/bin/env python3
"""Module for measuring the runtime of async comprehensions."""

import asyncio
from time import perf_counter

async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """Measure total runtime of executing async_comprehension four times."""
    start = perf_counter()
    await asyncio.gather(
        async_comprehension(),
        async_comprehension(),
        async_comprehension(),
        async_comprehension()
    )
    end = perf_counter()
    return end - start
