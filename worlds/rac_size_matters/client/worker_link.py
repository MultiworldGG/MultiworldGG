"""Client-side handle on the PCSX2 worker process."""

import asyncio
import multiprocessing
import queue
import threading
from collections.abc import Callable

from . import protocol
from .worker import worker_main

_SHUTDOWN_TIMEOUT_S = 5.0


class WorkerLink:
    """Starts the worker and relays its messages onto the client's event loop without blocking it."""

    def __init__(self, on_message: Callable[[tuple], None], on_exit: Callable[[int | None], None]) -> None:
        self._on_message = on_message
        self._on_exit = on_exit
        self._process = None
        self._inbox = None
        self._stop: threading.Event | None = None

    @property
    def alive(self) -> bool:
        return self._process is not None and self._process.is_alive()

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        # Spawn on every platform: a forked child would inherit the GUI and server sockets.
        mp = multiprocessing.get_context("spawn")
        self._inbox, outbox = mp.Queue(), mp.Queue()
        self._process = mp.Process(target=worker_main, args=(self._inbox, outbox),
                                   name="RAC PCSX2 worker", daemon=True)
        self._process.start()
        self._stop = threading.Event()
        threading.Thread(target=self._pump, args=(loop, self._process, outbox, self._stop),
                         name="RAC worker outbox", daemon=True).start()

    def _pump(self, loop, process, outbox, stop: threading.Event) -> None:
        while not stop.is_set():
            try:
                message = outbox.get(timeout=0.25)
            except queue.Empty:
                if not process.is_alive():
                    if not stop.is_set():
                        loop.call_soon_threadsafe(self._on_exit, process.exitcode)
                    return
                continue
            loop.call_soon_threadsafe(self._on_message, message)

    def send(self, message: tuple) -> None:
        if self.alive:
            self._inbox.put(message)

    def stop(self) -> None:
        """Ask the worker to release the loader gate and exit; terminate it if it doesn't."""
        if self._stop is not None:
            self._stop.set()
        if self._process is None:
            return
        if self._process.is_alive():
            self._inbox.put((protocol.SHUTDOWN,))
            self._process.join(_SHUTDOWN_TIMEOUT_S)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join(1.0)
        self._process = None
