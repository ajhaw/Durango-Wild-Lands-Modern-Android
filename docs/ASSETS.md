# AssetBundle Preservation Notes

## Client endpoints

Known original literals include:

```text
http://assetbundles.k.nexon.com/{0}/{1}/Info.5.2.1.json
http://durango-assetbundles.akamaized.net/{0}/{1}/
```

For local preservation testing the AssetBundle root can be redirected to a
local service such as:

```text
http://127.0.0.1:18080/
```

with:

```bash
adb reverse tcp:18080 tcp:18080
```

## Archived cache mapping

Archived cache layout:

```text
UnityCache/Shared/<NAME>.<CRC>/<HASH>/__data
```

HTTP repository layout used by the research environment:

```text
asset-repo/<NAME>.<CRC>.bundle
```

Do not commit the archived `__data` files or proprietary AssetBundles.

## Cache integrity

Do not assume the manifest `Size` field equals the physical cached `__data`
length. Compare a cache entry against the user's archived original using
actual byte size and SHA-256.

If an existing Android cache file is larger than the intended replacement,
truncate it before `adb push`:

```bash
adb shell "truncate -s 0 '$DST'"
adb push "$SRC" "$DST"
```

## Known warning

Do not use a catch-all diagnostic response that serves one AssetBundle for
multiple requested paths. Unity may cache the wrong bundle under a valid URL,
causing confusing duplicate-AssetBundle errors later.
