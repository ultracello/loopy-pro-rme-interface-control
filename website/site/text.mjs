// The text the page does not take from the documents. Keep it short; anything that changes with the work belongs in ../docs.
export const TEXT = {
  title: 'RME Babyface Pro FS, controlled from Loopy Pro',
  description: 'Controlling an RME Babyface Pro FS from Loopy Pro on the iPad without TotalMix FX: what works, what is measured, and a protocol reference for native support.',
  // The picture a social network shows next to a link to the page. It carries the title above: draw it again with tools/share-image.swift when the title or the screenshot changes.
  share: { file: 'share-preview-babyface-pro-fs-loopy-pro.png', width: 1200, height: 630, alt: 'The title of the page next to the controller page in Loopy Pro: faders for main and headphone level and rows of buttons for steps in dB.' },
  project: 'Babyface Pro FS · Loopy Pro',
  heading: 'Control an RME Babyface Pro FS from Loopy Pro',
  lead: 'Main and headphone level, input gains and monitoring next to your loops, on the iPad, without TotalMix FX.',
  state: 'A controller page for Loopy Pro is ready to use, and the protocol is written down for anyone who wants to build this into an app.',
  // The three ways into the page. Keep each text to one or two short sentences.
  ways: [
    { who: 'I play with Loopy Pro', title: 'Get the controller page', text: 'A Loopy Pro project with three pages of buttons. You also need StreamByter and MidiFire.', href: '#use' },
    { who: 'I own a Babyface', title: 'Check yours in ten minutes', text: 'Everything here was measured on one unit. A small tool guides you; no programming.', href: '#help' },
    { who: 'I build apps', title: 'Read the protocol reference', text: 'Every message byte for byte, measured on the unit, with a codec and test vectors.', href: '#developers' },
  ],
  nativePercent: 'Not started:',
  native: 'native support in Loopy Pro. That is the aim. It is in the hands of the developer of Loopy Pro; what he needs is in the protocol reference.',
  progressAfter: [
    'Both figures are counted from the table below whenever the page is built. A function counts as measured when its effect was read at the unit. The controller page covers what its maker needs on stage; equaliser and low cut cannot be done from it at all.',
  ],
  status: [
    'The table follows the functions TotalMix FX offers. Each entry says how far it is established on the one unit all of this was done with.',
  ],
  marks: [
    ['measured', 'The effect was measured at the unit\'s own meters, with a cable from an output to an input where needed.'],
    ['reported', 'The message was sent and the unit reported the new value back. The effect on audio was not measured.'],
    ['notes', 'Taken from other people\'s notes and not tried, or tried without a visible effect.'],
    ['unknown', 'No source and no way to observe it so far.'],
  ],
  pageHeading: 'The controller page for Loopy Pro',
  page: [
    'A Loopy Pro project you load next to your own. It talks to the Babyface directly; TotalMix FX is not running. It does this:',
  ],
  guide: 'https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/controller/README.md',
  guideLabel: 'Download and set-up guide',
  morePictures: 'Show the other two pages: inputs and monitoring',
  pageList: [
    'Main and headphone level in dB, in steps of any width from 0.5 to 30 dB, with mute and return to the level before.',
    'Gain of all four inputs, pad of the two microphone inputs, reference level of the two line inputs.',
    'Monitoring on the headphones: each input and the playback with its own level, pan and phase.',
    'After the interface was unplugged it sends the mixer again, because the unit forgets it.',
  ],
  figures: [
    { file: 'controller-interface-page.png', width: 1600, height: 1050,
      alt: 'The controller page in Loopy Pro: a row of status lamps, faders and dB displays for the main and the headphone output, step buttons from 0.5 to 6 dB for each, and a mute switch for each.',
      caption: 'The first of the three pages on 18 November 2026, armed. READ reads the unit, ARM arms the page, LOCK locks it. Under the faders, one row names the reason when a press is refused; the round lamps show the state of each output.' },
    { file: 'controller-inputs-page.png', width: 1600, height: 1050,
      alt: 'The inputs page: a gain display and six step buttons for each of the four inputs, a pad switch with lamps for the two microphone inputs, and a switch between +4 dBu and −10 dBV for the two line inputs.',
      caption: 'The second page: gain of the four inputs, pad of inputs 1 and 2, reference level of inputs 3 and 4. The lamps for 48 V only show what the unit reports; the page has no button for it.' },
    { file: 'controller-monitoring-page.png', width: 1600, height: 1050,
      alt: 'The monitoring page: five columns, one for each input and one for the playback, each with a level display, an on/off switch, step buttons, a pan display with left, mid and right, and a phase button.',
      caption: 'The third page: what is heard on the headphones. MON1 to MON4 are the four inputs, PB is the playback from the iPad. Each has level, on/off, pan and phase.' },
  ],
  pageAfter: [
    'Equaliser and low cut are not on the page: the scripting plug-in it is built with cannot send a message of that length in one piece. Phantom power is left out on purpose.',
    'How it is wired: a StreamByter plug-in inside Loopy Pro builds the messages and checks every answer of the unit. A second one in front of the unit lets only known messages pass. The answers reach the displays on the page through the app MidiFire.',
    'It is a working example, used on one iPad with one unit, and no substitute for native support: it has to keep its own picture of the mixer, and setting it up takes several steps.',
  ],
  questions: [
    ['Is there an app I can use?', 'A first one exists, made by someone else from this reference: [OliSimpleRME](https://github.com/OlivierPersoGit/OliSimpleRME), a small iPad mixer for the Babyface Pro FS, to sit next to Loopy Pro. It has to be built with Xcode. We have not built or tested it.'],
    ['What do I need for the controller page?', 'An iPad with Loopy Pro, the apps StreamByter and MidiFire, and a Babyface Pro FS in class-compliant mode. You connect your own Babyface in four taps; the guide shows them. It was tested on the iPad it was made on; nobody has set it up on a second one yet.'],
    ['Does it work on the iPhone?', 'Not tested. There is no TotalMix FX for the iPhone, which is one reason to want this. Hub and power supply on the iPhone are open questions.'],
    ['Does it work with other RME interfaces?', 'Unknown. Everything here was measured on a Babyface Pro FS in class-compliant mode. The notes this work started from describe the Babyface Pro. No other model was tried.'],
    ['Can it run next to TotalMix FX for iPad?', 'Not tested. Both would ask the unit for its meters, and each would take the peak values away from the other.'],
    ['What happens when the interface is unplugged?', 'Levels, gains and input settings survive. The unit forgets its mixer, so the headphones are silent until the mixer is sent again. The page does that when it is armed.'],
  ],
  helpHeading: 'Own a Babyface? Check yours',
  help: [
    'Everything here was measured on one unit. If you own a Babyface Pro or a Babyface Pro FS and a computer, a small tool guides you through a few checks with yours. It takes about ten minutes and needs no programming; ChatGPT or Claude can walk you through it with the prompt that comes with it.',
  ],
  helpLink: 'https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/docs/help-wanted/README.md',
  helpLabel: 'How to help',
  storyHeading: 'Where this comes from',
  story: [
    'A cellist plays with live looping in Loopy Pro on an iPad, through an RME Babyface Pro FS. The levels of that interface are normally set in TotalMix FX, a second app on the iPad that does not exist for the iPhone. The wish was simple: main and headphone level next to the loops.',
    'So the interface is controlled from inside Loopy Pro, over the MIDI port the unit offers in class-compliant mode. Two things came out of it: the controller page, and a protocol reference with measured values, written so that Loopy Pro or any other host could support the interface natively.',
  ],
  developers: [
    'If you want to build support for this interface into a host, the reference has what you need. Every statement in it says how it was established: measured, reported by the unit, taken from notes, or unknown.',
  ],
  open: [
    'These are the points that can still be settled on that unit. They are taken from the reference and disappear from this list when they are done.',
  ],
  reports: [
    'Every step of the work has a dated report with what was done, what was measured and what went wrong.',
  ],
  footer: [
    'Public domain under the [Unlicense](https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/LICENSE). Do whatever you want with it.',
    'Independent work. Not affiliated with RME or with A Tasty Pixel, the maker of Loopy Pro. Questions and corrections: [open an issue](https://github.com/ultracello/loopy-pro-rme-interface-control/issues).',
  ],
};
