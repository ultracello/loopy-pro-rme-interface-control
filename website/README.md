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

The browser interface is implemented and software-tested. The requested hardware controls are not provided as a tested installable module. The current evidence snapshot links three separate checkpoints: one bounded native Phones-fader reduction/restore, actual-level display feedback and a fixed-button step/restore. The fader result is both Phones channels -10.5 → -11.0 → -10.5 dB with fresh register readback before restore and Main unchanged. These are project-reported observations, not a full-range fader release or an acoustic measurement. Full-range behavior, native step selection, new mute toggles, stereo Main, freshness/reconnect/long-duration behavior, TotalMix-independent operation and the full iPhone workflow remain open. Each report and the output mapping are pinned to the reviewed documentation revision in `src/lib/evidence.ts`; historical observations remain separate.

The same distinction applies to exports: `hardwareTested: false` describes the selected exported configuration, not a claim that no project experiment has ever occurred. No control-code export is unlocked.

## Privacy

The site is public. User-entered model/version labels and selections remain in the browser's local storage until reset or cleared. Export files are generated in that browser and are not uploaded. There is no analytics, server API, external font, authentication or device transport in the app. GitHub may process ordinary hosting requests under its own policies. Public issues and attachments must be sanitized separately.

## Maintenance

Keep `src/lib/evidence.ts` scoped and dated. Protocol documentation, offline tests and hardware observations are different evidence levels. Do not promote a module without its exact reproducible device profile. Update the changelog, tests and generated-plan wording together.

This project has not selected a source-code license. Adding source here does not grant rights to third-party material.
