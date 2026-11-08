# Planning website tests and browser checklist

The [public planning website](https://ultracello.github.io/loopy-pro-rme-interface-control/) and its [source](../website/) are available. It is a browser-only planner, not a hardware controller. This checklist guides new reports; it does not mean every browser, device or step has passed.

## Recorded software evidence

- Website revision `dfd5dc10a32f4ba5dcb4e837b1c4a6cd024df9e9` (0.2.1): the website maintainer reported all 12 tests passing and a successful TypeScript/production build. [GitHub Actions run 42494183417](https://github.com/ultracello/loopy-pro-rme-interface-control/actions/runs/42494183417) completed successfully.
- The earlier deployment at revision `c38bdce903682fde556abfe93e21c7458847ca5c` was checked live for independent preview/mute behavior, JSON download and three documentation links. [Run 42491058463, second attempt](https://github.com/ultracello/loopy-pro-rme-interface-control/actions/runs/42491058463) succeeded. This is a scoped recorded browser check, not proof that every checklist item below passed on the later revision.
- Physical iPad Safari, iPhone and audio hardware were not validated by those website checks. The [passive iPad MIDI milestone](milestones/2026-11-08-passive-ipad-reception.md) is separate evidence and does not count as a website test.
- This documentation update did not rerun website or device tests. See [website/README.md](../website/README.md) for current local test/build commands.

**Do not connect an interface, send MIDI/OSC, import a script, or change routing for this checklist.** A planning preview does not test your audio hardware. If the page unexpectedly asks for device or microphone access, stop and report it.

## Five-minute browser check

1. Open the planning website. Record the displayed version, browser, OS, and supplied revision/build identifier. It should clearly identify its planning-only scope.
2. Select **Headphones**. Confirm that only the three headphone controls are selected. Select **Both outputs** and confirm that all six controls appear.
3. Toggle one control off and on. Confirm that only that part of the preview changes. Try **Start empty** and confirm that downloads are unavailable until a control is selected.
4. With both outputs selected, move one preview fader and try its up/down buttons. The other output's preview value should remain unchanged. Repeated presses should stay within the displayed demo limits.
5. Mute and unmute each preview output independently. Check that changing volume does not silently switch its mute state or the other output's state. This is a UI check, not proof of hardware feedback.
6. Change the requested step size. Confirm the brief records the chosen request without calling it a calibrated hardware step.
7. Review each setup path. The TotalMix FX for iPad path must retain its remote-control limitation. Desktop protocol support must not be presented as a tested Loopy setup.
8. Download both the checklist and JSON. Open them as text. Confirm the selected controls, versions, planning-only warnings, and `executable: false` / `hardwareTested: false`. The checklist should have real line breaks, not visible `\n` sequences. Exporting a brief must not claim to install anything.
9. Reload the page. Check saved choices. Try the preview's reset controls and verify the behavior matches their labels. Browser-local saving is not a cloud backup or hardware state.
10. On iPad or a narrow browser window, check that labels, controls, downloads, focus, and text remain usable. If you did not test a device or keyboard path, record **not run**.

For every failure, note the step, expectation, actual result, and a minimal way to reproduce it. Record partial passes honestly.

## Send a useful report in one minute

Copy [this short form](../templates/test-report.md), fill in what you know, and use the repository's **Test report or bug** form. Unknown is a valid answer. Reports are public: sanitize them before posting. Do not contact vendors on behalf of the project.

## Hardware testing comes later

There is no approved hardware test procedure in this repository. It must be written for the exact device profile, reviewed separately, preserve the existing project and routing, and define safe monitoring and stop conditions. A tester must not improvise from the browser demo.
