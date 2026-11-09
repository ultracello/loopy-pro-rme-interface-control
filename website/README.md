# Loopy Pro Interface Control planning website

Static React/Vite application for GitHub Pages. It lets visitors select desired Loopy Pro / RME controls, inspect compatibility boundaries, preview a local-only control surface and download a planning brief. No MIDI, OSC, audio, account access or hardware connection exists in this application.

## Run and verify

Use Node.js 22.13 or later. From this directory:

1. `npm ci`
2. `npm test`
3. `npm run build`
4. `npm run dev` for local preview, or `npm run preview` for the built files.

The output is `dist/`. Relative asset URLs support a GitHub project-site subdirectory. The root repository workflow builds and deploys only this output. In repository Settings → Pages, select **GitHub Actions** as the publishing source. The deployment URL is reported by the deployment job; do not treat an expected URL as proof of deployment.

## Status and boundaries

Planning release **0.2.6**, 9 November 2026, adds the [Sync LIVE1 fader/gate report](../docs/milestones/2026-11-09-live-faders-startup-gates.md). Three project starts showed correct current values without prior fader contact. Bounded Main/Phones fader reductions and increases were independently checked and restored exactly, with the other group unchanged. Transport stop locked controls; missing return input blocked activation, including in the write-enabled candidate. Restoring that input left output values unchanged. The tested copy was saved, original project/scene restored and diagnostics ended.

These are scoped observations, not full-range validation or a complete recovery matrix. Auxiliary displays, gain-mute lifecycle, physical USB reconnect and duration remain open. Missing-return blocking is not a physical USB reconnect test. The earlier restriction to clear the candidate's own gain-mute before lock/transport stop remains in place; no full live approval is given.

Earlier Main/Phones five-size step-button and gain-mute tests, v09b3 automatic reads and the other checkpoints retain their own dates and limits. Gain-mute is level reduction with a saved restore value, not a verified hardware mute bit or acoustic silence. Source reports are pinned in `src/lib/evidence.ts`. No private paths, original native projects, complete controller source or raw captures are released with the planner.

The browser interface is implemented and software-tested; it is not a hardware controller. Exported `hardwareTested: false` describes the selected planning configuration, not a denial of the scoped device experiments. No control-code export is unlocked. Public module promotion still requires an exact reproducible profile, reviewed artifacts and acceptance tests.

## Privacy

The site is public. User-entered model/version labels and selections remain in the browser's local storage until reset or cleared. Export files are generated in that browser and are not uploaded. There is no analytics, server API, external font, authentication or device transport in the app. GitHub may process ordinary hosting requests under its own policies. Public issues and attachments must be sanitized separately.

## Maintenance

Keep `src/lib/evidence.ts` scoped and dated. Protocol documentation, offline tests and hardware observations are different evidence levels. Do not promote a module without its exact reproducible device profile. Update the changelog, tests and generated-plan wording together.

This project has not selected a source-code license. Adding source here does not grant rights to third-party material.
