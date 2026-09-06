# Durango: Wild Lands — Modern Android Compatibility

An independent preservation and compatibility project focused on documenting
and developing tools that help a **legally obtained copy** of the original
Durango: Wild Lands Android client run on newer Android versions.

> This repository does **not** contain or distribute the Durango APK, game
> assets, AssetBundles, proprietary Nexon binaries, signing keys, credentials,
> or other copyrighted game data.

## Project goals

- Document compatibility problems on modern Android.
- Develop reproducible compatibility patches and tooling.
- Document local AssetBundle/cache behavior needed for preservation testing.
- Preserve clean-room interoperability research that may help future
  replacement-server development.
- Keep proprietary game files outside the repository.

## Current status

| Area | Status |
|---|---|
| Original ARM64 / IL2CPP client research | Working |
| Android 16 startup compatibility | Working in current test environment |
| Local AssetBundle redirection | Working |
| Unity cache investigation/repair | Working |
| Creative Island / Creative World | Reachable in current tests |
| Original MMO replacement server | Research / not implemented |

Reaching Creative Island uses behavior already present in the original client
and **does not mean the original MMO backend has been recreated**.

## Repository layout

```text
docs/
  ANDROID_COMPATIBILITY.md
  ANDROID16_FIX.md
  ASSETS.md
  CACHE_FIX.md
  PRIVATE_SERVER_RESEARCH.md
  PROTOCOL.md

patches/
  android16/

server/
  gateway.py
  gameserver.py
  protocol.py
  messages/

tools/
  build_asset_repo.py

examples/
  config.example.json
```

## Android compatibility

The tested legacy client uses Unity 2017.4 and IL2CPP. One compatibility issue
observed on Android 16 involves a newer Android service-connection callback
shape reaching an old JNI bridge implementation.

The research workaround adapts that callback to the legacy form expected by
the client. See [docs/ANDROID16_FIX.md](docs/ANDROID16_FIX.md).

The repository documents the technique rather than distributing a modified
game APK.

## Assets

The project does not provide game assets.

Preservation testing assumes the user already possesses their own archived
client/cache data. Local tools may build references to those user-supplied
files without copying them into Git.

See [docs/ASSETS.md](docs/ASSETS.md) and
[docs/CACHE_FIX.md](docs/CACHE_FIX.md).

## Private-server research

Durango contains networking and offline/Creative World components that are
useful references for interoperability research. A future replacement server
would be an independently implemented service speaking the protocol expected
by the client.

The current `server/` directory is only a clean-room research skeleton. It is
**not a functional recreation of the original MMO service**.

See [docs/PRIVATE_SERVER_RESEARCH.md](docs/PRIVATE_SERVER_RESEARCH.md) and
[docs/PROTOCOL.md](docs/PROTOCOL.md).

## What must not be committed

Do not commit:

- original or modified Durango APKs;
- `libil2cpp.so` or other proprietary native libraries;
- `global-metadata.dat`;
- original AssetBundles or UnityCache data;
- extracted/decompiled game assemblies or large code dumps;
- signing keystores or credentials;
- third-party copyrighted game assets.

The included `.gitignore` blocks common examples, but contributors are still
responsible for checking commits before pushing.

## Development principles

1. Keep original game data user-supplied and local.
2. Commit original project code, patches, tooling, and documentation only.
3. Document observed behavior needed for compatibility/interoperability.
4. Do not interact with or attempt to bypass access controls on legacy/live
   third-party infrastructure.
5. Do not publish recovered credentials or secrets.

## Disclaimer

Durango: Wild Lands and related names/assets belong to their respective
rights holders. This is an independent, unofficial preservation and
interoperability research project and is not affiliated with or endorsed by
Nexon.

The repository's license applies only to original code and documentation
created for this project. It does not grant rights to third-party game
software, assets, trademarks, or other proprietary material.
