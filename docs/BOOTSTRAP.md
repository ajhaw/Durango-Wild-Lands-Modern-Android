# Online Bootstrap

## Goal

Reconstruct the HTTP bootstrap used by the original Online/MMO path before
implementing gameplay services.

## Recovered title states

```text
0  Initial
1  GetClusterList
2  SelectCluster
3  SelectPlayer
4  Knock
5  CheckDataLoaded
6  CheckSoundManager
7  CheckSpriteManager
8  GetUser
9  NPAGetUser
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

Expected high-level Online flow:

```text
cluster selection
 -> knock
 -> asset/prerequisite checks
 -> user/session
 -> admission
 -> frontend discovery
 -> TCP connect
 -> GetClock/Auth/Welcome/Ready
```

## Important native functions

| Function | RVA |
|---|---:|
| RequestUrl | `0x175CED0` |
| RequestHttpUrl | `0x175D3A4` |
| RquestEntry | `0x175D4B0` |
| ProcessState | `0x175E2A0` |
| ProcessResponse | `0x175E96C` |
| OnRequestSucceed | `0x175EB74` |
| CheckError | `0x175F944` |
| ParseAddresses | `0x1760440` |

`ParseAddresses(JArray)` is a key target because the networking layer
eventually consumes host/port pairs through `ConnectAsync(string host, int port)`.

## Current research task

Recover the exact JSON schemas for:

- cluster list;
- knock;
- user/session;
- admission;
- frontend/entry.

Do not implement guessed production schemas. Document fields from client
behavior/native analysis first, then add them to the clean-room server.
