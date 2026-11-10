# Restricted Main/Phones step-width follow-up

Completed 10 November 2026 (UTC), following an initial cohort on 9 November. Evidence: project-reported, bounded native iPad/Babyface Pro FS observations across distinct test cohorts. This is a facts-only follow-up to the [Restricted control and Interface integration checkpoint](2026-11-09-restricted-control-interface-integration.md), not a controller-source, license or installable-profile release.

The Restricted LIVE1 rule was unchanged: SHA-256 `6d1149cc2e798d3de28426d658b28945af1f671cf8d67493c2ea86635b4639b7`. The earlier half-dB and fader results retain their separate scope; this follow-up did not repeat those tests.

## First cohort: four Main cases passed, Phones return failed

Four stereo Main reduction-and-return cases passed. Each used fresh device-state readback, left Phones unchanged, and returned exactly to the current-session baseline. These are mapped register/display values, not a new acoustic calibration.

| Requested Main step | Observed Main sequence | Phones |
|---|---|---|
| 1 dB | −8.0 → −9.0 → −8.0 dB | Unchanged |
| 2 dB | −8.0 → −10.0 → −8.0 dB | Unchanged |
| 3 dB | −8.0 → −11.0 → −8.0 dB | Unchanged |
| 6 dB | −8.0 → −14.0 → −8.0 dB | Unchanged |

The following Phones 1-dB case was **not a pass**. Its reduction was verified, but its attempted increase produced no valid complete hardware observation. The batch stopped; exact restoration was not verified and its restore authority was revoked. No blind continuation or automatic error-path upward compensation was allowed. That case remains failed and is not relabeled by later successful operations.

A later fixed read observed Main raw227/227 and Phones raw220/220. Timing records put the earlier READ-to-step interval at approximately **10.257 seconds**, beyond the rule's 10-second freshness window after two test-harness guard calls. Freshness expiry is a **probable explanation, not a causally established diagnosis**. This does not prove an AU-input, output, USB or device fault.

## Separate fresh-identity target and Phones cohort

The old host was retired with the failed record and its revoked authority retained. A distinct copy with a fresh AU identity loaded the same rule after a host restart. Host-process absence does not establish out-of-process AU destruction, USB queue continuity or crash-safe recovery.

A **new explicit normal-gain target**, separately read and checked, moved Phones raw220/220 to raw222/222 while Main remained raw227/227. The observed READ-to-step interval was approximately 5.553 seconds. This was a new intent, not replay of the failed case, reset of its revocation or reinstatement of an old saved restore reference. The old case remains failed.

The later Phones cohort passed all four bounded reduction-and-return pairs. Fresh readback confirmed each direction, a separate final read confirmed exact return, and Main remained unchanged. READ-to-step intervals for these eight actions were approximately 5.34–5.70 seconds. Those observations do not establish a general latency bound or change the earlier failure's classification.

| Requested Phones step | Observed Phones sequence | Main |
|---|---|---|
| 1 dB | −10.5 → −11.5 → −10.5 dB | Unchanged |
| 2 dB | −10.5 → −12.5 → −10.5 dB | Unchanged |
| 3 dB | −10.5 → −13.5 → −10.5 dB | Unchanged |
| 6 dB | −10.5 → −16.5 → −10.5 dB | Unchanged |

These four Phones passes and the earlier four Main passes are distinct cohorts. They do not turn the original interrupted batch into a complete pass, erase the failed Phones return or validate arbitrary rapid sequences. No further Main, half-dB or fader cases were repeated in the fresh Phones cohort.

## Final state and remaining boundaries

The original project and previous MidiFire scene were restored. The original's four central project files matched the saved baseline byte-for-byte. A fixed read after project and scene restoration confirmed Main raw227/227 and Phones raw222/222, mapped to −8.0 and −10.5 dB. No gain action was used during this closeout.

The temporary helper was absent from a fresh device-process inventory, owned diagnostic services and local ports were closed, and temporary access was retired. The installed helper's metadata was unchanged. These checks establish this run's recorded closeout, not general receiver continuity or crash-safe automatic recovery.

Gain-mute and the old saved-level restore path remain blocked. No new half-dB, fader, gain-mute, acoustic, physical USB reconnect or endurance test is claimed. Distinct dated cohorts and their failed records must remain distinct. Faster test-harness ordering does not solve silent receiver replacement, causal query correlation or crash-safe automatic restoration.

No general live approval, complete TotalMix coverage or independently installable integration is released. Private native projects, scenes, recordings, captures, device identifiers and automation credentials are excluded. This report contains no controller implementation or new license grant. The [acceptance gates](../ACCEPTANCE.md) continue to apply.
