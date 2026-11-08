export const PUBLIC_REPOSITORY = {
  url: 'https://github.com/ultracello/loopy-pro-rme-interface-control',
  branch: 'main',
  reviewedCommit: '6f4e1a50fb9ce24027b29c2068b2cf38c503a3e1',
  reviewedDate: '2026-11-08',
  reviewedFile: 'README.md, module status, scoped device milestones, step-selection simulation and output-gain evidence',
  visibility: 'public',
  status: 'Public reports distinguish send-free native step-selection simulation from the earlier bounded Phones-fader hardware test, display feedback and fixed-button step/restore. No released installable controller or reproducible hardware-validation package is included.',
} as const;
const pinned = (path: string) => `${PUBLIC_REPOSITORY.url}/blob/${PUBLIC_REPOSITORY.reviewedCommit}/${path}`;
export const REPORTS = {
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
export const LAB_STATUS = {
  reviewedDate: '2026-11-08',
  evidenceType: 'Project-reported scoped experiments, linked to dated public reports. Raw captures and installable controller artifacts are not bundled with this planner.',
  releaseReady: false,
  entries: [
    {id:'phones-fader-write',revision:'v09 TEST',level:'Bounded native write / restore',title:'One Phones fader gesture. Exact restore.',result:'Both Phones channels -10.5 → -11.0 → -10.5 dB. Fresh full register readback confirmed the target before restoration; Main stayed unchanged. The original project and scene were restored.',boundary:'One mapped half-dB operation, not a full-range fader pass. No acoustic measurement or new complete outbound trace. Native step-selector sender integration, new mute toggles and lifecycle tests remain open.',sourceUrl:REPORTS.faderWrite},
    STEP_SIMULATION,
    {id:'native-display',revision:'UI feedback',level:'Separate native display checkpoint',title:'Actual levels reached the visible sliders.',result:'Main -8.0 dB and Phones -10.5 dB automatically updated the native Loopy display through an iPad-only return path. The state-to-UI decoder accepted complete valid 227-byte states. 2,506 offline cases were reported passed.',boundary:'A temporary helper triggered the query, not the Loopy READ widget. No gain writes occurred in this display checkpoint. It does not establish freshness, pickup, TotalMix-independent operation or long-running feedback reliability.',sourceUrl:REPORTS.display},
    {id:'phones-step',revision:'v06 filter',level:'Separate fixed-button / readback checkpoint',title:'One paired step, then the exact baseline.',result:'Three separate Loopy READs passed. One Phones-minus raw unit changed both channels; a fresh full state confirmed the target before exact restoration. Main stayed unchanged. The observed trace contained four expected Phones writes and readback requests.',boundary:'The mapping supports a mapped 0.5-dB step, not an acoustic measurement. No new mute test or validation of other selectable step sizes. This fixed-button test and the later display/fader tests are separate experiments.',sourceUrl:REPORTS.step},
    {id:'earlier-v06',revision:'Earlier v06',level:'Historical scoped iPad observation',title:'Earlier step and custom mute experiments.',result:'Relative 0.5 dB steps and custom mute/restore were reported tested. Headphones addressed left and right together; the XLR control addressed output 1 only.',boundary:'This does not verify stereo main-output control or native TotalMix mute synchronization, and does not validate the later receiver or v09 candidate.',sourceUrl:REPORTS.overview},
    {id:'earlier-v08',revision:'Earlier v08',level:'Historical offline tests only',title:'Earlier software checks, not device proof.',result:'Eleven offline test groups covering 34,304 fader cases were recorded in the earlier website evidence snapshot.',boundary:'Those counts alone did not establish native widget or hardware behavior. Later scoped device observations are listed separately; none is a released reusable profile.',sourceUrl:`${PUBLIC_REPOSITORY.url}/blob/dfd5dc10a32f4ba5dcb4e837b1c4a6cd024df9e9/website/src/lib/evidence.ts`},
  ],
  remaining:['Full-range native faders and pickup','Native selectable-step UI with a real sender and larger physical steps','New mute toggles and native TotalMix mute synchronization','Stereo Main writes','Freshness, query correlation and feedback separation','Suspend, reconnect and long-duration behavior','TotalMix-independent operation','Full iPhone workflow','Exact reproducible profile and installable release'],
} as const;
export const LATEST_MILESTONE = LAB_STATUS.entries[0];
