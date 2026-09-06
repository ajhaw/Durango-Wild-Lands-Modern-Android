# Replacement Server Research

This is clean-room interoperability research for a future replacement service.
It is separate from the primary goal of modern-Android client compatibility.

## Confirmed architecture

The client contains an embedded Creative World implementation with two
distinct services:

```text
HTTP gateway : 8190
TCP game     : 8191
```

That implementation is useful as a behavioral reference. Successfully entering
Creative Island does **not** demonstrate recreation of the original MMO
backend.

## Online path

The recovered high-level title flow includes:

```text
cluster discovery
 -> cluster selection
 -> knock
 -> client-data checks
 -> user/session
 -> admission
 -> frontend discovery
 -> TCP connection
 -> welcome/loading
```

The exact Online HTTP response schemas are still under investigation. The
project should not invent or claim compatibility with schemas that have not
been verified.

## Implementation direction

A replacement service should consist only of independently written code:

```text
original client owned by user
        |
        +--> clean-room HTTP bootstrap
        |
        +--> clean-room TCP frontend
                  |
                  +--> protocol/message implementation
                  +--> future world/game systems
```

Historical third-party services are not required and should not be probed as
part of this project.
