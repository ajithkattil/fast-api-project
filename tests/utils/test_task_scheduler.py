from collections.abc import Generator
from typing import Any

import pytest

from src.utils.task_scheduler import TaskScheduler


@pytest.fixture
def task_scheduler() -> Generator[TaskScheduler, Any, None]:
    scheduler = TaskScheduler()
    scheduler.start()
    yield scheduler
    scheduler.shutdown(5)


def test_task_scheduler_start_and_is_running(task_scheduler: TaskScheduler) -> None:
    assert task_scheduler.is_running() is True


def test_task_scheduler_double_start(task_scheduler: TaskScheduler) -> None:
    # Starting scheduler again should not throw error and it should keep running
    task_scheduler.start()
    assert task_scheduler.is_running() is True


def test_task_scheduler_schedule_async_task_success(task_scheduler: TaskScheduler) -> None:
    async def sample_coroutine() -> str:
        return "Task completed"

    future = task_scheduler.schedule_async_task(sample_coroutine())
    assert future.result(timeout=2) == "Task completed"  # type: ignore[union-attr]


def test_task_scheduler_schedule_async_task_without_start() -> None:
    scheduler = TaskScheduler()

    async def sample_coroutine() -> str:
        return "Task completed"

    with pytest.raises(RuntimeError, match="Loop is not running"):
        scheduler.schedule_async_task(sample_coroutine())


def test_task_scheduler_graceful_shutdown() -> None:
    t = TaskScheduler()
    t.start()
    t.shutdown(10)
    assert not t.is_running()
