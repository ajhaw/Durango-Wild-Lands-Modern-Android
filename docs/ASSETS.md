# AssetBundle Preservation

## Local testing

For preservation testing, the client can be configured to request required
AssetBundles from a user-controlled local HTTP service instead of relying on
historical third-party infrastructure.

Example local root:

```text
http://127.0.0.1:18080/
```

For an Android device connected through ADB:

```bash
adb reverse tcp:18080 tcp:18080
```

## Archived cache mapping

A user-supplied Unity cache may contain entries shaped like:

```text
UnityCache/Shared/<NAME>.<CRC>/<HASH>/__data
```

The included `tools/build_asset_repo.py` can create a symlink-only HTTP view
from those local files. It does not provide or download game assets.

Do not commit the resulting asset repository.

## Important cache behavior

Do not assume a manifest's logical size field is identical to the physical
cached `__data` length. When validating preserved files, compare against the
user's known-good archived copy using actual byte length and a cryptographic
hash.

Never make a diagnostic HTTP server return one arbitrary AssetBundle for
multiple requested names. Unity can cache that response under the requested
identity, producing misleading duplicate-bundle errors later.
