"""Messages between the AP client process and the PCSX2 worker process.

Every message is a tuple ``(kind, *args)`` of picklable values. The client owns the
server connection and GUI; the worker owns PINE, Core and every memory read/write,
so a stalled emulator can only stall the worker.
"""

import logging

# Client -> worker
CONNECTED = "connected"            # (payload: dict)
AP_DISCONNECTED = "ap_disconnected"
LOCATIONS = "locations"            # (checked: set[int], server: set[int])
RECEIVED_ITEMS = "received_items"  # (items: list[NetworkItem], index: int)
STORED = "stored"                  # (updated: dict[str, Any])
BOUNCED = "bounced"                # (data: dict)
VENDOR_REWARDS = "vendor_rewards"  # (rewards: dict[int, VendorReward])
ITEM_SENT = "item_sent"            # (item_name: str, player_name: str)
CALL = "call"                      # (method: str, args: tuple) -- only worker cmd_* methods
SHUTDOWN = "shutdown"

# Worker -> client
LOG = "log"                        # (logger_name: str, level: int, text: str)
SEND_MSGS = "send_msgs"            # (msgs: list[dict])
CHECK_LOCATIONS = "check_locations"  # (location_ids: list[int])
SET_NOTIFY = "set_notify"          # (keys: list[str])
UPDATE_DEATH_LINK = "update_death_link"  # (enabled: bool)
UPDATE_LINK_TAG = "update_link_tag"      # (tag: str, enabled: bool)
GUI_ERROR = "gui_error"            # (text: str)


class ForwardingLogHandler(logging.Handler):
    """Worker-side handler that ships each record to the client's loggers."""

    def __init__(self, post) -> None:
        super().__init__()
        self.post = post
        self.setFormatter(logging.Formatter("%(message)s"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.post((LOG, record.name, record.levelno, self.format(record)))
        except Exception:
            self.handleError(record)
