"""Low-level Durango packet framing.

Only the confirmed 24-byte header is implemented here. Snappy/MessagePack
message codecs will be added once the server bootstrap is implemented.
"""

from dataclasses import dataclass
import struct
import time

HEADER = struct.Struct("<QIIII")
HEADER_SIZE = HEADER.size


@dataclass(slots=True)
class PacketHeader:
    time_ms: int
    seq: int
    reply_of: int
    type_code: int
    payload_size: int

    def pack(self) -> bytes:
        return HEADER.pack(
            self.time_ms,
            self.seq,
            self.reply_of,
            self.type_code,
            self.payload_size,
        )

    @classmethod
    def unpack(cls, data: bytes) -> "PacketHeader":
        if len(data) != HEADER_SIZE:
            raise ValueError(f"header must be {HEADER_SIZE} bytes")
        return cls(*HEADER.unpack(data))


def make_header(seq: int, reply_of: int, type_code: int, payload_size: int,
                *, timestamp: float | None = None) -> bytes:
    if timestamp is None:
        timestamp = time.time()
    return HEADER.pack(
        int(timestamp * 1000.0),
        seq,
        reply_of,
        type_code,
        payload_size,
    )
