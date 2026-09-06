# Research Notes

## Client

```text
Package:          com.nexon.durango.global
Version:          5.2.1 (50201)
Unity:            2017.4.34f1
Runtime:          IL2CPP
Architecture:     ARM64
Metadata version: 24
```

## IL2CPP registrations

```text
CodeRegistration     0x51EB5F0
MetadataRegistration 0x51EB660
```

## Embedded Creative World server

Recovered components:

```text
Durango.Offline.Gateway
Durango.Offline.GameServer
Durango.Offline.Listener
```

Default ports:

```text
HTTP Gateway 8190
TCP GameServer 8191
```

Recovered routes include:

```text
GET  /knock
GET  /notice
POST /sessions
GET  /admission
GET  /entry
POST /players
GET  /terrains/1
GET  /terrains/1/whole_biomes
```

This embedded server has been confirmed to support Creative Island/Creative
World. It must not be described as proof of a complete offline MMO server.

## Asset manifest observations

For the archived 5.2.1 manifest examined during research:

```text
ItemList     4302
FileList     2152
PreloadHash  45fc886f6a6238364c01a91381dc0ab9
PreloadCrc   09fced165c9bf5ee2bb14ea9906b0c26
```

## Research discipline

Large proprietary dumps should stay outside Git. Extract only the information
needed to document interoperable behavior and implement original clean-room
code.
