# Durango TCP Protocol

## Status

This document records protocol behavior recovered during clean-room
interoperability research of the Durango 5.2.1 Android client.

## Wire packet

Every TCP packet begins with a 24-byte little-endian header.

| Offset | Size | Field |
|---|---:|---|
| `0x00` | 8 | Time in milliseconds (`uint64`) |
| `0x08` | 4 | Sequence (`uint32`) |
| `0x0C` | 4 | ReplyOf (`uint32`) |
| `0x10` | 4 | TypeCode (`uint32`) |
| `0x14` | 4 | PayloadSize (`uint32`) |

```python
struct.pack("<QIIII", time_ms, seq, reply_of, type_code, payload_size)
```

The managed `PacketHeader` structure is not identical to the wire layout.

## Payload

Observed serialization pipeline:

```text
MessagePack payload
    -> raw Snappy compression
    -> 24-byte header + compressed payload
    -> TCP
```

The TypeCode is stored in the packet header. Normal message payloads are
packed with the message TypeCode excluded.

## Known TypeCodes

| Message | TypeCode |
|---|---:|
| Auth | 1 |
| Ready | 20 |
| Welcome | 22 |
| Abort | 1024 |
| OK | 1231 |
| GetClock | 4000 |
| Clock | 4001 |

## Initial handshake

```text
Client                              Server
GetClock (4000, seq=A)  ---------->
                         <---------- Clock (4001, replyOf=A)
Auth (1, seq=B)          ---------->
                         <---------- Welcome (22, replyOf=B)
Ready (20, seq=C)        ---------->
                         <---------- OK (1231, replyOf=C)
```

Known `Auth` fields:

```text
EntityId
SessionToken
ClientVersion
DeviceModel
```

Payloads without embedded TypeCode:

```text
GetClock = [Time]
Clock    = [ClientTime, ServerTime]
Ready    = []
```

## Welcome

Recovered top-level layout:

```text
[
  UserId,
  Name,
  Region,
  Storage,
  Options,
  Archipelago?,
  PersonalRegionId,
  Seasons,
  SocialOptions,
  EngagementRewardSent
]
```

The minimal structure used by the embedded Creative World server is useful as
a protocol reference, but is not yet considered sufficient for the MMO path.
