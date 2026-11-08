# Contributing

Start with one clearly described issue. This repository currently contains documentation and templates, not a runnable application or hardware-control package.

## You do not need to code

- Report confusing wording or a failed documented step using [the test-report template](templates/test-report.md).
- Suggest one concrete musical task and its smallest useful result.
- Supply an official manual link and relevant section. Documentation supports a documented capability, not a hardware-test pass.

Issues, pull requests and their attachments are public. Remove private data before posting. Do not submit personal recordings, device/network identifiers, original projects, credentials or private correspondence.

## Small changes are easiest to review

1. Describe the intended change in an issue before doing substantial implementation work.
2. Work on one module or coherent behavior at a time. Preserve existing routing and working project originals.
3. When application code is added, follow its actual checked-in setup and test instructions. There is currently no app in this repository to install or run.
4. Record the exact revision and each check as passed, failed, blocked or not run. A browser simulation is not a hardware test.
5. Update [module status](docs/MODULE_STATUS.md), its [machine-readable registry](verification/module-status.json), and [the changelog](CHANGELOG.md) when behavior or evidence changes.
6. Submit a **draft** pull request for review. Approval and merging are separate from release or deployment.

No contributor license agreement or software license is imposed by this draft. Propose and resolve the appropriate licensing before substantial code contributions. Third-party code requires compatible rights and attribution; a public repository alone does not supply them.

See [the developer/test setup](docs/DEVELOPMENT_SETUP.md) for Mac/iPad automation roles, version inventory, reproduction, and the separate end-user requirements.

## Hardware-control contributions

Complete [the device-profile template](templates/device-profile.md) and meet [the acceptance gates](docs/ACCEPTANCE.md) before describing a module as hardware verified. Include actual message mappings, encoding, destination, feedback, safe failure behavior, and precise software/hardware versions.

Keep input gain, mixer level, mute and pan distinct. Verify that headphones and main output behave independently. Display uncertain hardware state honestly instead of guessing. Do not improvise a hardware setup from a future browser demo.

A test report applies only to the stated module, profile and revision. Preserve failures and limits. Do not generalize a single-model result to every RME device or from iPad to iPhone.
