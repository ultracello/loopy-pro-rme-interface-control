# Loopy READ reaches READY / LOCKED

Date: **8 November 2026**. Evidence level: **project-reported, scoped native device observation**. This follows the [passive reception checkpoint](2026-11-08-passive-ipad-reception.md); it is not a released hardware-control profile or an independently repeated test.

## Observed result

One clock-only read test used the existing **v06 Loopy controls** and the newly verified MidiFire return path. The audio clip was stopped and the metronome was off. After starting the clock and pressing READ once, the actual StreamByter panel displayed **BEREIT / GESPERRT (READY / LOCKED)**. Stopping the clock returned the panel to **LESEN / GESPERRT (READ / LOCKED)** as intended.

- The Loopy output monitor showed one fixed seven-byte state request: `F0 00 20 0D 10 10 F7`.
- The input monitor contained complete **227/207/207-byte replies**.
- A separately subscribed passive receiver, configured with `requestState=false`, captured five CoreMIDI chunks of **9, 75, 143, 207 and 207 bytes**. They reassembled into exactly **227, 207 and 207 bytes**, without an incomplete remainder. The diagnostic receiver did not send a second request.
- No arm, output-gain, mute, audio-clip, rule-installation, widget-assignment or Loopy/TotalMix-routing operation was performed. Observed output-gain fields stayed at their existing values.
- The tested return path was saved as a new native MidiFire scene. The original scene was restored afterwards. After the check, clip and transport were stopped, and temporary remote-control services were shut down.

This establishes one successful native read/readiness observation for that test setup. READY / LOCKED is an observed controller state, not independent proof of every decoded field or permission to arm the controller. The timed reply window is not a protocol transaction identifier.

## Tested paths

**Return path:** Babyface Port 2 MIDI source → MidiFire Event Monitor → MidiFire 1 virtual destination → existing Loopy StreamByter.

**Read request:** existing Loopy READ widget / StreamByter → Babyface Port 2 MIDI destination.

The MidiFire scene contains no script stage and no Babyface hardware destination. The Mac supplied UI automation and passive observation; it was **not a MIDI relay**. This does not establish that the whole workflow is independent of every development service or of TotalMix.

The three-block return scene was saved natively, but a new portable MFR export has not yet been obtained. The scene, existing Loopy controls and raw captures are not distributed with this report, so it is not a standalone installation package or a complete reproduction recipe.

## Limits

- **No new gain, mute or fader validation:** the result is one read/readiness check, not a finished live-control release.
- **TotalMix remained running in the background.** It was not foregrounded for this follow-up, but a test with TotalMix explicitly terminated was not performed. The result therefore does not establish TotalMix-independent operation.
- **No release profile:** exact firmware, OS/app/plugin versions, full source revision and portable receiver artifacts are not supplied in this public checkpoint. Product names and v06 identify context, not a complete versioned profile.
- **Further lifecycle checks remain:** reload, physical reconnect, longer operation, widget feedback and additional TotalMix functions require their own tests. Earlier prototype results must not be generalized to this exact follow-up.
- **The previous disconnect remains unexplained.** Physical reconnection recovered detection, but there is no established general device/software defect. These were discrete checks, not continuous monitoring.
- Private captures, screenshots and their metadata are not included. This documentation update did not operate or retest a device.

## Next validation area

A separately reviewed level-changing test can use the saved return path, obtain fresh current state, then check a small headphone reduction and exact restoration. Fader and toggle-feedback checks are separate work. None of those results is claimed here; do not infer safe levels or device commands from this report.

See the [hardware acceptance gates](../ACCEPTANCE.md) and [module status](../MODULE_STATUS.md). This milestone advances state-query/readiness evidence without promoting any executable control module to a verified release.
