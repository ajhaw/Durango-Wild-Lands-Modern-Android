# Android Compatibility

## Tested target

Current preservation testing focuses on the original ARM64 IL2CPP Android
client on modern Android, including Android 16.

The client was built with an older Unity generation, so incompatibilities may
appear in Android framework/JNI behavior even when the native game code itself
still starts correctly.

## Current results

- Legacy client can start after the documented Android 16 compatibility fix.
- Local AssetBundle redirection works in the current test environment.
- Creative Island / Creative World can be reached with the preserved client
  and required user-supplied data.
- This does not recreate the original online MMO service.

## Testing guidance

Keep an untouched backup of all legally obtained client/cache files before
testing modifications. Avoid uninstalling or clearing application data during
cache research unless a clean-state test specifically requires it.

Compatibility on other Android versions/devices is not yet guaranteed.
