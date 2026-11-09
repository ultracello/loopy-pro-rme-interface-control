export const PUBLIC_REPOSITORY = {
  url: 'https://github.com/ultracello/loopy-pro-rme-interface-control',
  branch: 'main',
  reviewedCommit: '1ef2df430da16d4bd4e175634ab31afbcb3abb52',
  reviewedDate: '2026-11-09',
  reviewedFile: 'README.md, module status, scoped device milestones, step-selection simulation and output-gain evidence',
  visibility: 'public',
  status: 'Sync LIVE1 adds three correct fader startups, bounded Main/Phones fader writes with independent exact restoration, transport-stop locking and missing-return activation blocking. Auxiliary feedback, gain-mute lifecycle, physical USB reconnect and duration remain open. Earlier step-button and gain-mute checkpoints retain their own scope. No released installable controller or reproducible hardware-validation package is included.',
} as const;
const pinned = (path: string) => `${PUBLIC_REPOSITORY.url}/blob/${PUBLIC_REPOSITORY.reviewedCommit}/${path}`;
export const REPORTS = {
  liveFaders: pinned('docs/milestones/2026-11-09-live-faders-startup-gates.md'),
  mainPhones: pinned('docs/milestones/2026-11-09-main-phones-steps-gain-mute.md'),
  v09b3: pinned('docs/milestones/2026-11-09-phones-v09b3-follow-up.md'),
  stepSimulation: pinned('docs/milestones/2026-11-08-native-step-simulation.md'),
  faderWrite: pinned('docs/milestones/2026-11-08-phones-fader-write-restore.md'),
  display: pinned('docs/milestones/2026-11-08-native-fader-display.md'),
  step: pinned('docs/milestones/2026-11-08-phones-step-restore.md'),
  mapping: pinned('docs/protocol/output-gain-evidence.md'),
  overview: pinned('docs/PROJECT_OVERVIEW.md'),
} as const;
export const EVIDENCE = [
  {id:'rme-ipad-app', title:'RME TotalMix FX for iPad', type:'Official product description', url:'https://apps.apple.com/us/app/totalmix-fx-for-ipad/id739965887', finding:'The app excludes MIDI/OSC and TCP/IP remote control. This does not establish whether a separate direct hardware-control path exists.'},
  {id:'rme-midi', title:'RME MIDI remote reference', type:'Official protocol documentation', url:'https://docs.rme-audio.com/aoxm/850-1c_midi_remote_tmfx/', finding:'Desktop TotalMix MIDI remote mappings are documented. Device, operating mode, destination and feedback still need validation.'},
  {id:'loopy-manual', title:'Loopy Pro manual', type:'Official application documentation', url:'https://loopypro.com/manual/', finding:'Loopy provides MIDI actions and custom controls. The receiving hardware path must be established separately.'},
  {id:'project-status', title:'Reviewed project README', type:'Public project status, pinned revision', url:pinned('README.md'), finding:PUBLIC_REPOSITORY.status},
  {id:'sync-live1-faders', title:'Sync LIVE1 fader startup, writes and activation gates', type:'Project-reported scoped device checks', url:REPORTS.liveFaders, finding:'Three starts showed correct current fader values without prior contact. Main and Phones were reduced/increased and independently restored exactly, with the other group unchanged. Transport stop locked controls; missing return input blocked activation. Auxiliary feedback, mute lifecycle, physical USB reconnect and duration remain open.'},
  {id:'main-phones-steps-gain-mute', title:'Main/Phones physical steps and gain-mute restoration', type:'Project-reported scoped device tests', url:REPORTS.mainPhones, finding:'Each stereo group passed 0.5/1/2/3/6-dB reduction/restore pairs with the other group unchanged. XLR2 was checked separately. Gain-mute/restore and following half-dB checks passed per group. That checkpoint did not establish native hardware mute bits, confirmed button feedback, free faders or lifecycle safety; later fader/gate checks are listed separately.'},
  {id:'phones-v09b3', title:'v09b3 Phones test with automatic follow-up reads', type:'Project-reported bounded device observation', url:REPORTS.v09b3, finding:'After more than 75 seconds of transport runtime, both Phones channels -10.5 → -11.0 → -10.5 dB. Automatic follow-up queries at 101/100 ms received successful replies and separate queries confirmed both operations. Main stayed at -8.0 dB. Not general live or long-duration validation.'},
  {id:'phones-fader-write', title:'One native Phones-fader reduction and restoration', type:'Project-reported bounded device/register observation', url:REPORTS.faderWrite, finding:'Both Phones channels -10.5 → -11.0 → -10.5 dB; fresh full readback before restore, Main unchanged. No acoustic measurement or new complete outbound trace. Not a full-range fader release.'},
  {id:'native-display', title:'Native Loopy fader display', type:'Project-reported UI/read-feedback observation', url:REPORTS.display, finding:'Actual Main/Phones levels updated visible Loopy sliders through UI-only feedback after a helper-triggered query, not the Loopy READ widget. This separate display checkpoint made no gain writes.'},
  {id:'phones-step', title:'Filtered reception and one Phones step/restore', type:'Project-reported fixed-button/register observation', url:REPORTS.step, finding:'Three Loopy READ checks, one paired raw-unit reduction and exact restoration; Main unchanged. No new mute or acoustic test.'},
  {id:'step-simulation', title:'Step selection: offline checks and native widget simulation', type:'Project-reported send-free UI simulation, not hardware evidence', url:REPORTS.stepSimulation, finding:'Five 0.5/1/2/3/6-dB choices passed ten native widget-only direction cases, inert startup, unknown-default inactivity and reload. Separate backend compiled natively; its preview commands were not run at native runtime. No real sender or larger physical step was tested.'},
  {id:'output-mapping', title:'Output-gain mapping and tested points', type:'Project-reviewed model-specific mapping', url:REPORTS.mapping, finding:'One raw unit maps to 0.5 dB at the documented test points. Display conversion is not an independent acoustic calibration or proof of a full hardware range.'},
] as const;
export const CONTROL_BOUNDARIES = [
  {name:'Interface control', detail:'Loopy control → verified MIDI/control transport → exact RME model and operating mode. Scoped tests do not yet establish operation with TotalMix terminated.'},
  {name:'Audio', detail:'The audio connection and existing mix routing are separate from the control messages. This planner does not alter either.'},
  {name:'Developer testing', detail:'Mac-based UI automation can support development, but it is not an established requirement for musicians using a future released profile.'},
] as const;
export const RELEASE_GATES = [
  'Record the exact model, firmware, host, app versions and operating mode.',
  'Read the current hardware state before any control can apply a saved value.',
  'Verify headphones and main output independently, including mute semantics and feedback.',
  'Validate each requested dB step, its mapping, bounds and fresh-state delta; distinguish displayed values from acoustic measurements.',
  'Test restart, reconnect and safe recovery, then publish a reproducible profile and simple installation guide.',
  'Separate incoming display feedback from human write intent; verify freshness, pickup and full-range native behavior.',
] as const;
export const STEP_SIMULATION = {
  id:'step-simulation', revision:'Widget SIM', level:'Send-free native widget simulation',
  title:'Step selection tested without a sender.',
  stepSizesDb:[0.5,1,2,3,6],
  offline:{groups:6,cases:34102,additionalRegressions:1792,repeatedSameCaseSet:true,publiclyRerunnable:false},
  backend:{nativeCompilation:true,nativeRuntimeCommandsTested:false,senderConnected:false},
  widgets:{nativeCases:10,widgetOnly:true,inertStartup:true,unknownDefaultNoop:true,reloadPreservedStepDb:6},
  newHardwareTest:false, largerPhysicalStepsTested:false,
  result:'Ten Loopy-only widget cases checked 0.5 / 1 / 2 / 3 / 6 dB in both directions from simulated -10.5 dB. Selection and internal stores agreed; startup without selection and unknown defaults stayed inert. Save/reload preserved 6 dB without a nudge. Separately, six offline groups / 34,102 cases plus 1,792 additional regressions were reported; the no-SND backend text matched and compiled natively.',
  boundary:'The StreamByter preview commands were not executed at native runtime. The synthetic repeat used the same 34,102 cases, not another distinct case set. Native widgets had no MIDI targets or send bindings and were not connected to that backend or a real sender. Reset restored a simulation reference, not a device factory default. No larger physical step or expanded hardware range was tested.',
  sourceUrl:REPORTS.stepSimulation,
} as const;
export const V09B3_CHECKPOINT = {
  id:'phones-v09b3', revision:'v09b3', level:'Bounded device test with automatic follow-up reads',
  title:'Phones restored. Automatic follow-up confirmed.',
  transportRuntimeSecondsGreaterThan:75, phonesSequenceDb:[-10.5,-11.0,-10.5],
  automaticFollowUpQueryDelaysMs:[101,100], separateConfirmationQueriesPassed:true,
  mainDb:-8, originalProjectAndSceneRestored:true, generalLiveReadinessVerified:false,
  result:'After more than 75 seconds of transport runtime, both Phones channels -10.5 → -11.0 → -10.5 dB. Automatic follow-up queries after 101/100 ms received successful replies; separate device queries confirmed both operations. StreamByter showed BEREIT / AKTIV. Main stayed unchanged at -8.0 dB. The original project and scene were restored; diagnostic processes ended.',
  boundary:'Exactly one reduction and one restoration. Mapped device/display values, not acoustic calibration. Two successful follow-up reads are not a latency distribution, full-range fader pass, long-duration test or general live approval. This checkpoint did not verify native button/selector integration, larger steps, mute, stereo Main, suspend/reconnect or an installable profile; later tests are listed separately.',
  sourceUrl:REPORTS.v09b3,
} as const;
export const MAIN_PHONES_CHECKPOINT = {
  id:'main-phones-steps-gain-mute', revision:'Main + Phones · 9 Nov', level:'Scoped physical step-button and gain-mute tests',
  title:'Five step sizes. Both output groups. Exact restoration.',
  stepSizesDb:[0.5,1,2,3,6], testedStepPattern:'reduction then exact restoration',
  phonesPairStepsPassed:true, mainStereoStepsPassed:true, otherGroupUnchangedDuringStepTests:true,
  xlr2SeparateHalfDbRestorePassed:true, gainMuteRestorePassed:['main','phones'],
  postGainMuteHalfDbChecksPassed:true, nativeHardwareMuteBitsVerified:false,
  buttonIndicatorsVerified:false, freeFadersVerified:false, transportStopSafetyVerified:false,
  connectionChangeSafetyVerified:false, savedButtonActionCount:22, fullReloadRecoveryVerified:false,
  originalProjectAndSceneRestored:true, generalLiveReadinessVerified:false,
  result:'Paired Phones and stereo Main each passed 0.5 / 1 / 2 / 3 / 6 dB reductions followed by exact restoration; the other output group stayed unchanged. XLR2 was verified separately. One gain-mute/restore toggle per group and the following 0.5-dB checks passed. Complete code and 22 button actions were checked in the saved candidate. Original project and previous MidiFire scene were restored; diagnostics ended.',
  boundary:'Gain-mute is level reduction with a saved restore value, not a verified hardware mute bit or acoustic silence. At that checkpoint, button indicators, free faders, transport-stop and connection-change safety were unverified. Saved contents do not prove complete reload recovery. Current candidate: READ → ARM; clear its own gain-mute before lock/transport stop. No general live approval or public installable profile.',
  sourceUrl:REPORTS.mainPhones,
} as const;
export const LIVE_FADERS_CHECKPOINT = {
  id:'sync-live1-faders', revision:'Sync LIVE1 · 9 Nov', level:'Bounded native faders, startup and activation gates',
  title:'Current values at startup. Both faders tested. Exact restore.',
  correctStartupChecks:3, initialFaderTouchRequired:false, boundedNativeFadersTested:['main','phones'],
  independentExactRestoreConfirmed:true, otherGroupUnchangedDuringFaderTests:true,
  transportStopLocksControlsObserved:true, missingReturnPreventsActivationObserved:true,
  missingReturnCheckedInWriteCandidate:true, returnRestorationLeftLevelsUnchanged:true,
  testedCopySaved:true, originalProjectAndSceneRestored:true, auxiliaryDisplaysVerified:false,
  gainMuteLifecycleVerified:false, physicalUsbReconnectVerified:false, longDurationVerified:false,
  fullRangeFadersVerified:false, completeRecoveryMatrixVerified:false, generalLiveReadinessVerified:false,
  result:'Three project starts showed correct current device values without touching a fader first. Main and Phones were each reduced and increased by native fader, independently checked and restored exactly; the other output group stayed unchanged. Transport stop locked controls. Missing return input blocked activation, including in the write-enabled candidate; restoring that input left levels unchanged. The tested copy was saved, original project/scene restored and diagnostics ended.',
  boundary:'Bounded gestures and three starts, not a full-range pass or complete recovery matrix. Missing-return blocking is not physical USB reconnect validation. Auxiliary displays, gain-mute lifecycle and USB reconnect/duration remain open. Gain-mute is not a verified hardware mute bit; clear its own gain-mute before lock/transport stop. No full live approval or public installable profile.',
  sourceUrl:REPORTS.liveFaders,
} as const;
export const LAB_STATUS = {
  reviewedDate: '2026-11-09',
  evidenceType: 'Project-reported scoped experiments, linked to dated public reports. Raw captures and installable controller artifacts are not bundled with this planner.',
  releaseReady: false,
  entries: [
    LIVE_FADERS_CHECKPOINT,
    MAIN_PHONES_CHECKPOINT,
    V09B3_CHECKPOINT,
    {id:'phones-fader-write',revision:'v09 TEST',level:'Bounded native write / restore',title:'One Phones fader gesture. Exact restore.',result:'Both Phones channels -10.5 → -11.0 → -10.5 dB. Fresh full register readback confirmed the target before restoration; Main stayed unchanged. The original project and scene were restored.',boundary:'One mapped half-dB operation, not a full-range fader pass. No acoustic measurement or new complete outbound trace. Native step-selector sender integration, new mute toggles and lifecycle tests were not part of this checkpoint.',sourceUrl:REPORTS.faderWrite},
    STEP_SIMULATION,
    {id:'native-display',revision:'UI feedback',level:'Separate native display checkpoint',title:'Actual levels reached the visible sliders.',result:'Main -8.0 dB and Phones -10.5 dB automatically updated the native Loopy display through an iPad-only return path. The state-to-UI decoder accepted complete valid 227-byte states. 2,506 offline cases were reported passed.',boundary:'A temporary helper triggered the query, not the Loopy READ widget. No gain writes occurred in this display checkpoint. It does not establish freshness, pickup, TotalMix-independent operation or long-running feedback reliability.',sourceUrl:REPORTS.display},
    {id:'phones-step',revision:'v06 filter',level:'Separate fixed-button / readback checkpoint',title:'One paired step, then the exact baseline.',result:'Three separate Loopy READs passed. One Phones-minus raw unit changed both channels; a fresh full state confirmed the target before exact restoration. Main stayed unchanged. The observed trace contained four expected Phones writes and readback requests.',boundary:'The mapping supports a mapped 0.5-dB step, not an acoustic measurement. No new mute test or validation of other selectable step sizes. This fixed-button test and the later display/fader tests are separate experiments.',sourceUrl:REPORTS.step},
    {id:'earlier-v06',revision:'Earlier v06',level:'Historical scoped iPad observation',title:'Earlier step and custom mute experiments.',result:'Relative 0.5 dB steps and custom mute/restore were reported tested. Headphones addressed left and right together; the XLR control addressed output 1 only.',boundary:'This does not verify stereo main-output control or native TotalMix mute synchronization, and does not validate the later receiver or v09 candidate.',sourceUrl:REPORTS.overview},
    {id:'earlier-v08',revision:'Earlier v08',level:'Historical offline tests only',title:'Earlier software checks, not device proof.',result:'Eleven offline test groups covering 34,304 fader cases were recorded in the earlier website evidence snapshot.',boundary:'Those counts alone did not establish native widget or hardware behavior. Later scoped device observations are listed separately; none is a released reusable profile.',sourceUrl:`${PUBLIC_REPOSITORY.url}/blob/dfd5dc10a32f4ba5dcb4e837b1c4a6cd024df9e9/website/src/lib/evidence.ts`},
  ],
  remaining:['Full-range native faders and pickup','Auxiliary displays and confirmed button-state feedback','Arbitrary or rapid step sequences beyond the tested reduction/restore pairs','Native hardware mute bits and TotalMix mute synchronization','Gain-mute recovery across lock or transport stop','Broad freshness, query-correlation and feedback-separation guarantees','Physical USB reconnect and long-duration behavior','TotalMix-independent operation','Full iPhone workflow','Exact reproducible profile and installable release'],
} as const;
export const LATEST_MILESTONE = LAB_STATUS.entries[0];
