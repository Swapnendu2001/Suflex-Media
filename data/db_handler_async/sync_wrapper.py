import asyncio
from typing import Any
import threading
from functools import partial


class AsyncRunner:
    def __init__(self):
        self._loop = None
        self._thread = None
        self._lock = threading.Lock()

    def _start_loop(self):
        """Start the asyncio event loop in a separate thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _ensure_loop(self):
        """Ensure the asyncio event loop is running."""
        with self._lock:
            if self._loop is None or not self._loop.is_running():
                self._thread = threading.Thread(target=self._start_loop, daemon=True)
                self._thread.start()
                # Give the thread a moment to start the loop
                import time
                time.sleep(0.01)

    def run_async(self, async_func, *args, **kwargs):
        """Run an async function from synchronous code."""
        self._ensure_loop()
        
        # Create a future to hold the result
        future = asyncio.run_coroutine_threadsafe(
            async_func(*args, **kwargs), 
            self._loop
        )
        
        # Wait for the result
        return future.result()


# Global runner instance
_runner = AsyncRunner()


def run_async_function(async_func, *args, **kwargs):
    """Run an async function synchronously."""
    return _runner.run_async(async_func, *args, **kwargs)