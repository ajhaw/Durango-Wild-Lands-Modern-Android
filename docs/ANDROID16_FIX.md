# Android 16 Compatibility Fix

## Problem

During testing on Android 16, the legacy client could fail while handling an
Android service-connection callback through its old JNI bridge.

The observed failure involved a newer callback form carrying an additional
binder-session argument, while the legacy native bridge expected the older
two-argument callback form.

## Compatibility approach

The working research patch adds a small compatibility shim in the application's
Java/smali bridge layer:

```text
modern callback
(ComponentName, IBinder, additional session argument)

        ↓ compatibility shim

legacy callback
(ComponentName, IBinder)

        ↓

original native bridge
```

The shim is intentionally narrow: it adapts this compatibility boundary rather
than changing game logic.

## Distribution

This repository does not distribute a patched APK or proprietary application
files. Users performing preservation research must apply documented changes to
their own legally obtained copy.

Exact implementation artifacts can be added under `patches/android16/` only
when they contain original patch code/diffs and no proprietary game file.
