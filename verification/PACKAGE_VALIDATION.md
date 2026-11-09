# Documentation validation

Date: **2026-11-09**. Scope: publication of the completed, bounded v09b3 Phones result and synchronization of the public documentation and research registry. Base repository revision: `e193e9c1f9d2de08f393cdf4f0f8dcd3dcec2305`.

## Publication checks

- Relative Markdown file targets resolve within the publication package. This checks file targets, not remote availability or rendered anchors.
- Issue-template YAML remains unchanged and parses successfully.
- The JSON registry retains six distinct hardware-module IDs, no verified profiles and no executable artifacts. The new research record identifies v09b3 without promoting a module or borrowing older test counts/hashes.
- The sanitized report records paired Phones −10.5 → −11.0 → −10.5 dB, the 101/100 ms automatic follow-up queries, separate confirming reads, BEREIT / AKTIV, Main unchanged at −8.0 dB and restoration of the original project/scene.
- Public-content review excludes credentials, private conversation or thread identifiers, local filesystem/network details and original working projects.
- `SHA256SUMS` covers documentation and templates, excluding itself and website source. It establishes content integrity, not hardware behavior.

## Evidence boundaries

The publication did not access the device, issue a MIDI query or repeat the device test. The result is project-reported. Raw captures, complete native controller source, its checksum and a reproducible version/profile inventory are not included. Two successful automatic follow-up queries after more than 75 seconds of transport runtime do not prove long-duration, reconnect or general live readiness.

Website regression/build checks are recorded separately in [the website testing document](../docs/TESTING.md). Remote commit readback and Pages deployment must be checked after publication; this file does not predeclare their success.
