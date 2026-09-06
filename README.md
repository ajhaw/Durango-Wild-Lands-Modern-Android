# Durango: Wild Lands — Preservation & Private Server Research

Reverse-engineering and preservation research for the original
**Durango: Wild Lands 5.2.1 Android client**.

> **Status:** the original client runs on Android 16, loads archived
> AssetBundles from a local server, and can enter the built-in Creative
> Island/Creative World. The current goal is a clean-room implementation
> of the original **Online/MMO bootstrap and game server**, not an
> extension of Creative Island.

## Scope

This project is intended for software preservation, protocol research,
interoperability, and clean-room server emulation. The repository should
**not** distribute Nexon APKs, `libil2cpp.so`, `global-metadata.dat`,
AssetBundles, game assets, credentials, or signing secrets. Users must
supply their own legally obtained client/archive data.

## Tested client

| Property    | Value                      |
|-------------|----------------------------|
| Package     | `com.nexon.durango.global` |
| Version     | `5.2.1` / `50201`          |
| Engine      | Unity `2017.4.34f1`        |
| Runtime     | IL2CPP, ARM64              |
| Metadata    | Version 24                 |
| Test OS     | Android 16                 |
| Test device | POCO F6 (`peridot`)        |

Reference hashes:

``` text
libil2cpp.so
247b21587fb661946775bc3cba5dfb3d1f0f543ce5182ec61daae71cece25eae

global-metadata.dat
2e9cab572b3f822df066bb7e6d7d3305a69e4f140e057b0629e4584b6d8c3727
```

The binaries themselves are not part of the repository.

## Current status

``` text
Android 16 client              WORKING
Android compatibility patch    WORKING
Local AssetBundle server       WORKING
Archived AssetBundles          WORKING
Wwise / SoundBanks             WORKING
Creative Island                PLAYABLE
Embedded HTTP :8190            CONFIRMED
Embedded TCP :8191             CONFIRMED
TCP packet header              RECOVERED
MessagePack + Snappy           RECOVERED
Basic handshake                RECOVERED
Online state machine           IDENTIFIED
Online HTTP schemas            IN PROGRESS
MMO private server             NOT YET IMPLEMENTED
```

## 1. IL2CPP research

Il2CppDumper successfully processed the ARM64 client.

``` text
CodeRegistration     0x51EB5F0
MetadataRegistration 0x51EB660
```

Useful output:

``` text
dump/dump.cs
dump/script.json
dump/stringliteral.json
dump/il2cpp.h
```

Raw `strings` output should not be treated as authoritative for IL2CPP
string literals because adjacent metadata literals can appear
concatenated. For example, these are separate literals:

``` text
assetbundle_url_root
http://durango-assetbundles.akamaized.net/{0}/{1}/
{}
user_id
```

## 2. Android 16 compatibility

The 2019 client originally crashes on Android 16 around
`ServiceConnection.onServiceConnected` through
`bitter.jnibridge.JNIBridge`.

The compatibility patch translates the newer three-argument callback
into the legacy two-argument form expected by the old Unity/native
implementation before forwarding it to native code.

Result:

``` text
Durango 5.2.1 + Unity 2017.4.34f1 + Android 16 = launches successfully
```

The patched APK is kept locally and is intentionally not distributed.

## 3. AssetBundle system

Important client literals:

``` text
http://assetbundles.k.nexon.com/{0}/{1}/Info.5.2.1.json
http://durango-assetbundles.akamaized.net/{0}/{1}/
assetbundle_index_url
assetbundle_url_root
```

Recovered `Info.5.2.1.json` information:

``` text
ItemList:     4302
FileList:     2152
PreloadHash:  45fc886f6a6238364c01a91381dc0ab9
PreloadCrc:   09fced165c9bf5ee2bb14ea9906b0c26
```

`AssetBundleManager.CreateTargetUrl` ultimately uses the bundle name,
CRC, and root. Observed request names follow:

``` text
<bundle-name-without-.bundle>.<CRC>.bundle
```

Example:

``` text
soundbanks$android$en_us$voice_event.bnk.bytes.64ba4ac9ab6dd76bc66e40aa82796d55.bundle
```

### Local AssetBundle root

For preservation testing, the AssetBundle root was patched to:

``` text
http://127.0.0.1:18080/
```

During USB development:

``` bash
adb reverse tcp:18080 tcp:18080
```

Archived UnityCache data is mapped from:

``` text
UnityCache/Shared/<NAME>.<CRC>/<HASH>/__data
```

to local HTTP names such as:

``` text
asset-repo/<NAME>.<CRC>.bundle
```

## 4. Cache corruption incident

An early diagnostic server accidentally returned the **SoundBanksInfo**
bundle for every URL containing `soundbanks`. This polluted UnityCache.

The affected `voice_event` cache contained:

``` text
size   206469
sha256 1472f166023e13f837a498844deefa513a552a1aa9c6ab6bfb1a7f7d5acee7a0
```

That was actually the SoundBanksInfo data.

Correct archived `voice_event`:

``` text
size   7369
sha256 03866f0b5bb6f29fc5f4d53e498db0fbcd0cc8de3b7bb6a693dea1bd87f9a5f6
```

A plain `adb push` over the larger file did not truncate the stale tail.
The successful repair was:

``` bash
adb shell "truncate -s 0 '$DST'"
adb push "$SRC" "$DST"
```

After restoring the exact archived bytes, `CheckSoundManager` passed and
the client entered the game.

**Important:** manifest `Size` is not necessarily the physical cached
`__data` length. Validate cache integrity against the original archived
`__data` using actual size and SHA-256.

The active cache on the tested device is:

``` text
/sdcard/Android/data/com.nexon.durango.global/files/UnityCache
```

## 5. Creative Island vs MMO

Reaching a playable scene initially appeared to prove the MMO offline
server was working. Further testing showed that the embedded offline
stack is associated with **Creative Island / Creative World**.

This still gives us a valuable known-good baseline:

- Unity runtime works on Android 16.
- AssetBundle loading works.
- YAML/sprite initialization works.
- Wwise/SoundBanks work.
- Embedded HTTP/TCP networking works.
- The original serialization code executes correctly.

The MMO private server therefore follows the separate **Online** path.

## 6. Embedded offline server

Recovered classes include:

``` text
Durango.Offline.Gateway
Durango.Offline.GameServer
Durango.Offline.Listener
```

Default ports:

| Service        |   Port |
|----------------|-------:|
| HTTP Gateway   | `8190` |
| TCP GameServer | `8191` |

Recovered offline HTTP routes include:

``` text
GET  /knock
GET  /notice
POST /sessions
GET  /admission
GET  /entry
POST /players
GET  /terrains/1
GET  /terrains/1/whole_biomes
```

When Creative World is active, the **original client itself** opens
ports 8190 and 8191. Do not run replacement Python servers on these
ports during embedded-server testing.

## 7. TCP protocol

The wire packet header is exactly 24 bytes:

| Offset | Size | Field                             |
|--------|-----:|-----------------------------------|
| `0x00` |    8 | time in milliseconds, `uint64 LE` |
| `0x08` |    4 | sequence, `uint32 LE`             |
| `0x0C` |    4 | reply-of, `uint32 LE`             |
| `0x10` |    4 | TypeCode, `uint32 LE`             |
| `0x14` |    4 | payload size, `uint32 LE`         |

Python representation:

``` python
import struct

def make_header(time_seconds, seq, reply_of, type_code, payload_size):
    return struct.pack(
        "<QIIII",
        int(time_seconds * 1000.0),
        seq,
        reply_of,
        type_code,
        payload_size,
    )
```

The managed `PacketHeader` layout is different from the actual wire
representation.

### Payload pipeline

``` text
MessagePack
    ↓
raw Snappy
    ↓
24-byte Durango header
    ↓
TCP
```

TypeCode is carried in the packet header. Normal message packing uses
the payload without duplicating the TypeCode.

## 8. Known handshake

Recovered TypeCodes:

| Message    | TypeCode |
|------------|---------:|
| `Auth`     |      `1` |
| `Ready`    |     `20` |
| `Welcome`  |     `22` |
| `Abort`    |   `1024` |
| `OK`       |   `1231` |
| `GetClock` |   `4000` |
| `Clock`    |   `4001` |

Observed basic flow:

``` text
Client                              Server

GetClock (4000, seq=A)  ---------->
                         <---------- Clock (4001, replyOf=A)

Auth (1, seq=B)          ---------->
                         <---------- Welcome (22, replyOf=B)

Ready (20, seq=C)        ---------->
                         <---------- OK (1231, replyOf=C)
```

Known `Auth` fields:

``` text
EntityId
SessionToken
ClientVersion
DeviceModel
```

Without TypeCode, `GetClock` and `Clock` are represented conceptually
as:

``` text
GetClock: [Time]
Clock:    [ClientTime, ServerTime]
Ready:    []
```

Recovered `Welcome` has ten elements:

``` text
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

The embedded Creative World implementation is reference material; its
minimal `Welcome` must not yet be assumed sufficient for the MMO
backend.

## 9. Online state machine

Recovered `TitleMenuGroup.State`:

``` text
-1 Invalid
 0 Initial
 1 GetClusterList
 2 SelectCluster
 3 SelectPlayer
 4 Knock
 5 CheckDataLoaded
 6 CheckSoundManager
 7 CheckSpriteManager
 8 GetUser
 9 NPAGetUser
10 FadeOutPrologue
11 PrologueLoading
12 CheckPrerequsite
13 PostPrerequsite
14 GetAdmission
15 GetFrontend
16 TryConnect
17 Connecting
18 Welcome
19 FadeOutLoading
20 Loading
21 Error
22 IdleInHardcapPosition
23 GetTimedTicketInfo
24 IdleInTimedTicketWaiting
```

The target MMO path is therefore approximately:

``` text
GetClusterList
    ↓
SelectCluster / SelectPlayer
    ↓
Knock
    ↓
asset + prerequisite checks
    ↓
GetUser
    ↓
GetAdmission
    ↓
GetFrontend
    ↓
TryConnect
    ↓
TCP frontend
    ↓
Auth / Welcome / Ready
    ↓
world/gameplay packets
```

## 10. Online bootstrap targets

Important native functions:

| Function           |         RVA |
|--------------------|------------:|
| `RequestUrl`       | `0x175CED0` |
| `RequestHttpUrl`   | `0x175D3A4` |
| `RquestEntry`      | `0x175D4B0` |
| `ProcessState`     | `0x175E2A0` |
| `ProcessResponse`  | `0x175E96C` |
| `OnRequestSucceed` | `0x175EB74` |
| `CheckError`       | `0x175F944` |
| `ParseAddresses`   | `0x1760440` |

The networking layer also exposes:

``` text
ConnectAsync(string host, int port)
```

`ParseAddresses(JArray)` is therefore one of the key functions for
reconstructing the HTTP response that supplies the TCP frontend
endpoints.

The immediate research task is to recover the exact JSON contracts
rather than inventing responses.

### Native disassembly

GNU `objdump` returned only the ELF header for these ARM64 ranges. The
next attempt uses LLVM:

``` bash
sudo apt update
sudo apt install -y llvm

cd ~/durango-re

{
  echo '===== ProcessState 0x175E2A0 ====='
  llvm-objdump -d --start-address=0x175E2A0 --stop-address=0x175E96C libil2cpp.so

  echo '===== ProcessResponse 0x175E96C ====='
  llvm-objdump -d --start-address=0x175E96C --stop-address=0x175EB74 libil2cpp.so

  echo '===== OnRequestSucceed 0x175EB74 ====='
  llvm-objdump -d --start-address=0x175EB74 --stop-address=0x175FD68 libil2cpp.so

  echo '===== ParseAddresses 0x1760440 ====='
  llvm-objdump -d --start-address=0x1760440 --stop-address=0x1760788 libil2cpp.so
} > online-bootstrap-native-v2.txt
```

Expected output should contain AArch64 instructions such as `stp`,
`ldr`, `adrp`, `bl`, and `cbz`, rather than only
`file format elf64-little`.

## 11. Planned private-server architecture

``` text
+-----------------------+
| Original Durango APK  |
+-----------+-----------+
            |
       HTTP bootstrap
            |
            v
+-----------+-----------+
| Durango HTTP Service  |
|                       |
| clusters / knock      |
| sessions / admission  |
| entry / players       |
+-----------+-----------+
            |
    frontend_addresses
            |
            v
+-----------+-----------+
| Durango TCP Frontend  |
|                       |
| 24-byte header        |
| MessagePack + Snappy  |
| Seq / ReplyOf         |
| TypeCode              |
+-----------+-----------+
            |
            v
+-----------+-----------+
| Game Server Logic     |
| world / player        |
| entities / inventory  |
| movement / gameplay   |
+-----------------------+
```

The first milestone for the clean-room MMO server is:

``` text
client discovers private frontend
→ TCP connection succeeds
→ GetClock
→ Auth
→ Welcome
→ Ready
```

Gameplay packet implementation comes after this works reliably.

## Roadmap

- [x] Identify Durango 5.2.1 Android client
- [x] Dump IL2CPP metadata
- [x] Recover classes, TypeCodes and RVAs
- [x] Patch Android 16 JNI compatibility
- [x] Redirect AssetBundle root to localhost
- [x] Build local archived AssetBundle repository
- [x] Repair corrupted SoundBank cache
- [x] Reach playable Creative Island
- [x] Identify embedded Gateway/GameServer
- [x] Recover 24-byte TCP header
- [x] Recover MessagePack + Snappy transport
- [x] Recover basic handshake
- [x] Identify Online title-menu state machine
- [ ] Disassemble Online bootstrap functions
- [ ] Recover exact cluster-list schema
- [ ] Recover `/knock` response
- [ ] Recover user/session response
- [ ] Recover admission response
- [ ] Recover frontend/entry response
- [ ] Implement clean-room HTTP bootstrap
- [ ] Redirect Online mode to private bootstrap
- [ ] Establish Online TCP frontend connection
- [ ] Complete Auth → Welcome → Ready
- [ ] Identify minimum world-loading messages
- [ ] Implement persistent player/world state
- [ ] Implement movement/entity synchronization
- [ ] Expand inventory, crafting and gameplay systems

## Development notes

During current testing:

1.  Do **not** clear working application data/UnityCache unnecessarily.
2.  Do **not** use the old `asset_probe.py`; it caused cache pollution.
3.  Use the proper local AssetBundle server on port `18080`.
4.  Keep `adb reverse tcp:18080 tcp:18080` active while uncached assets
    are required.
5.  Do not run external servers on 8190/8191 while testing embedded
    Creative World.
6.  Back up known-good cache data before experiments.
7.  When overwriting a larger cached `__data`, truncate it before
    `adb push`.
8.  Never commit proprietary game data, APKs, private keys, or
    credentials.

Suggested `.gitignore`:

``` gitignore
*.apk
*.so
*.keystore
global-metadata*.dat
asset-repo/
local-assets/
dump/
UnityCache/
__pycache__/
*.log
```

## Legal / preservation notice

This is an independent preservation and interoperability project and is
not affiliated with or endorsed by Nexon.

The goal is to document the discontinued client’s behavior and build a
clean-room compatible server. Proprietary client binaries, copyrighted
game assets, credentials, and signing secrets should not be distributed
through this repository.
