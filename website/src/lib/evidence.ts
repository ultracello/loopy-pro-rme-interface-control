export const PUBLIC_REPOSITORY = {
  url: 'https://github.com/ultracello/loopy-pro-rme-interface-control',
  branch: 'main',
  reviewedCommit: '7b722b4dd50cc20b9a68aa1ed7bfd21c7d8fa37a',
  reviewedDate: '2026-11-08',
  reviewedFile: 'README.md and docs/MODULE_STATUS.md',
  visibility: 'public',
  status: 'Documentation and contribution templates are published. No released installable control module or reproducible hardware-validation package was present in the reviewed revision.',
} as const;
export const EVIDENCE = [
  {id:'rme-ipad-app', title:'RME TotalMix FX for iPad', type:'Official product description', url:'https://apps.apple.com/us/app/totalmix-fx-for-ipad/id739965887', finding:'The app excludes MIDI/OSC and TCP/IP remote control. This does not establish whether a separate direct hardware-control path exists.'},
  {id:'rme-midi', title:'RME MIDI remote reference', type:'Official protocol documentation', url:'https://docs.rme-audio.com/aoxm/850-1c_midi_remote_tmfx/', finding:'Desktop TotalMix MIDI remote mappings are documented. Device, operating mode, destination and feedback still need validation.'},
  {id:'loopy-manual', title:'Loopy Pro manual', type:'Official application documentation', url:'https://loopypro.com/manual/', finding:'Loopy provides MIDI actions and custom controls. The receiving hardware path must be established separately.'},
  {id:'project-status', title:'Reviewed project README', type:'Public project status, pinned revision', url:`${PUBLIC_REPOSITORY.url}/blob/${PUBLIC_REPOSITORY.reviewedCommit}/README.md`, finding:PUBLIC_REPOSITORY.status},
] as const;
export const CONTROL_BOUNDARIES = [
  {name:'Interface control', detail:'Loopy control → verified MIDI/control transport → exact RME model and operating mode. A direct path must be demonstrated independently of the TotalMix app.'},
  {name:'Audio', detail:'The audio connection and existing mix routing are separate from the control messages. This planner does not alter either.'},
  {name:'Developer testing', detail:'Mac-based UI automation can support development, but it is not an established requirement for musicians using a future released profile.'},
] as const;
export const RELEASE_GATES = [
  'Record the exact model, firmware, host, app versions and operating mode.',
  'Read the current hardware state before any control can apply a saved value.',
  'Verify headphones and main output independently, including mute semantics and feedback.',
  'Measure the requested dB steps; do not equate a MIDI increment with a dB increment.',
  'Test restart, reconnect and safe recovery, then publish a reproducible profile and simple installation guide.',
] as const;
export const LAB_STATUS = {
  reviewedDate: '2026-11-08',
  evidenceType: 'Project-reported experimental results; raw test artifacts are not bundled with this planner.',
  releaseReady: false,
  entries: [
    {revision:'v06', level:'Scoped iPad device check', result:'Relative 0.5 dB steps and a custom mute/restore behavior were reported tested. Headphones addressed left and right together; the XLR control addressed output 1 only.', boundary:'This does not verify stereo main-output control or native TotalMix mute-state synchronization. It is not a released, reusable device profile.'},
    {revision:'v08', level:'Offline tests only', result:'Eleven offline test groups passed, covering 34,304 fader cases.', boundary:'Native device and Loopy widget behavior remain unverified. Offline test counts do not demonstrate working hardware faders.'},
  ],
  remaining:['Stereo main-output control','Hardware fader feedback','Native TotalMix mute synchronization','Full iPhone compatibility','Exact reproducible profile and installable release'],
} as const;
