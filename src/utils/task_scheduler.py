import asyncio
import concurrent.futures
import threading
from asyncio import AbstractEventLoop
from collections.abc import Coroutine

from src.utils.singleton import singleton


@singleton
class TaskScheduler:
    def __init__(self) -> None:
        self.loop: AbstractEventLoop | None = None
        self.loop_thread: threading.Thread | None = None
        self._loop_started = threading.Event()

    def start(self) -> None:
        if self.is_running():
            return  # Already running

        self._loop_started.clear()
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()

        # Wait a moment to make sure loop is running
        # this can take a few seconds
        while not self.loop.is_running():
            threading.Event().wait(0.1)

    def _run_event_loop(self) -> None:
        if self.loop:
            asyncio.set_event_loop(self.loop)
            try:
                self.loop.run_forever()
            finally:
                self.loop.close()
        else:
            raise RuntimeError("Loop is not running")

    def schedule_async_task(self, task: Coroutine) -> concurrent.futures.Future | None:
        if self.loop and self.loop.is_running():
            return asyncio.run_coroutine_threadsafe(task, self.loop)
        else:
            raise RuntimeError("Loop is not running")

    def is_running(self) -> bool:
        return self.loop is not None and self.loop.is_running()

    async def _cancel_all_tasks(self, timeout: float | None) -> None:
        """A coroutine that handles the graceful cancellation of tasks."""
        tasks = [t for t in asyncio.all_tasks(self.loop) if t is not asyncio.current_task(self.loop)]
        if not tasks:
            return

        # Give tasks some time to finish
        _, pending = await asyncio.wait(tasks, timeout=timeout)

        # Cancel all the tasks that did not finish
        for task in pending:
            task.cancel()

        # Wait for all tasks to complete their cancellation
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)

    def shutdown(self, timeout: float | None = None) -> None:
        """Gracefully shuts down the event loop and all running tasks."""
        if not self.is_running() or self.loop is None:
            return

        # Step 1: Cancel all running tasks gracefully.
        try:
            future = asyncio.run_coroutine_threadsafe(self._cancel_all_tasks(timeout), self.loop)
            # Wait for task cancellation to complete.
            future.result(timeout=timeout)
        except (concurrent.futures.TimeoutError, RuntimeError):
            # If it times out or the loop is already shut down, continue.
            pass

        # Step 2: Stop the event loop.
        if self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)

        # Step 3: Wait for the event loop thread to finish.
        if self.loop_thread and self.loop_thread.is_alive():
            self.loop_thread.join()
