# Unity Cache Repair Notes

A corrupted or incorrectly populated cache entry can survive later tests and
make a valid AssetBundle appear broken.

## Safe workflow

1. Keep a known-good archived copy.
2. Identify the exact cache entry being tested.
3. Compare its byte length and SHA-256 with the archived copy.
4. Replace only the affected user-owned cache entry.
5. Verify the resulting length/hash before launching the client.

When an existing destination file is larger than its intended replacement,
overwriting alone may leave stale trailing bytes. Truncate the destination
before writing the replacement:

```bash
adb shell "truncate -s 0 '$DST'"
adb push "$SRC" "$DST"
```

`SRC` and `DST` are intentionally placeholders. No game cache files are
distributed by this project.

Avoid clearing the complete cache when investigating a single known-bad entry;
doing so makes reproduction harder and may remove otherwise valid preserved
data.
