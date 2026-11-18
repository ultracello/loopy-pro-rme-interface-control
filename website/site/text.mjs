// The text the page does not take from the documents. Keep it short; anything that changes with the work belongs in ../docs.
export const TEXT = {
  title: 'RME Babyface Pro FS, controlled from Loopy Pro',
  description: 'Controlling an RME Babyface Pro FS from Loopy Pro on the iPad without TotalMix FX: what works, what is measured, and a protocol reference for native support.',
  project: 'Babyface Pro FS · Loopy Pro',
  heading: 'Controlling an RME Babyface Pro FS from Loopy Pro',
  intro: [
    'This project comes from a cellist who plays with live looping in Loopy Pro on an iPad, through an RME Babyface Pro FS. The levels of that interface are normally set in TotalMix FX, which is a second app on the iPad and does not exist for the iPhone. The wish was simple: main and headphone level next to the loops.',
    'So the interface is controlled from inside Loopy Pro, over the MIDI port the unit offers in class-compliant mode. Two things have come out of it: a controller page that is in use, and a protocol reference with measured values, written so that Loopy Pro or any other host could support the interface natively.',
    'There is nothing to download and install yet. The controller is a private working copy.',
  ],
  progress: [
    'Three figures say how far the work is. The first two are counted from the table below every time the page is built; nobody types them.',
  ],
  nativePercent: 'Not started:',
  native: 'native support in Loopy Pro. That is the aim. It is in the hands of the developer of Loopy Pro; what he needs is in the protocol reference.',
  progressAfter: [
    'A function counts as measured when its effect was read at the unit. Functions the unit only reported back, or that are known from other people\'s notes alone, do not count yet. Two entries of the table are left out because they are not functions of the unit.',
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
  pageHeading: 'The controller page in Loopy Pro',
  page: [
    'The page lives in a Loopy Pro project on one iPad and talks to one Babyface Pro FS. TotalMix FX is not running. It does this:',
  ],
  pageList: [
    'Main and headphone level in dB, in steps of any width from 0.5 to 30 dB, with mute and return to the level before.',
    'Gain of all four inputs, pad of the two microphone inputs, reference level of the two line inputs.',
    'Monitoring on the headphones: each input and the playback with its own level, pan and phase.',
    'After the interface was unplugged it sends the mixer again, because the unit forgets it.',
  ],
  figure: {
    file: 'controller-interface-page.png', width: 1600, height: 1050,
    alt: 'The controller page in Loopy Pro: a row of status lamps, faders and dB displays for the main and the headphone output, step buttons from 0.5 to 6 dB for each, and a mute switch for each.',
    caption: 'The first of the three pages on 18 November 2026, armed. READ reads the unit, ARM arms the page, LOCK locks it. Under the faders, one row names the reason when a press is refused; the round lamps show the state of each output. The other two pages hold the input gains and the monitoring.',
  },
  pageAfter: [
    'Equaliser and low cut are not on the page: the scripting plug-in it is built with cannot send a message of that length in one piece. Phantom power is left out on purpose.',
    'How it is wired: a StreamByter plug-in inside Loopy Pro builds the messages and checks every answer of the unit. A second one in front of the unit lets only known messages pass. The answers reach the displays on the page through the app MidiFire.',
    'The page is not published, and it is no substitute for native support: it has to keep its own picture of the mixer, and setting it up takes many steps.',
  ],
  questions: [
    ['Can I get the controller?', 'Not yet. It is one person\'s working copy, tied to one project and one iPad. What is published is everything needed to build the same thing properly: the protocol reference.'],
    ['Does it work on the iPhone?', 'Not tested. There is no TotalMix FX for the iPhone, which is one reason to want this. Hub and power supply on the iPhone are open questions.'],
    ['Does it work with other RME interfaces?', 'Unknown. Everything here was measured on a Babyface Pro FS in class-compliant mode. The notes this work started from describe the Babyface Pro. No other model was tried.'],
    ['Can it run next to TotalMix FX for iPad?', 'Not tested. Both would ask the unit for its meters, and each would take the peak values away from the other.'],
    ['What happens when the interface is unplugged?', 'Levels, gains and input settings survive. The unit forgets its mixer, so the headphones are silent until the mixer is sent again. The page does that when it is armed.'],
  ],
  developers: [
    'If you want to build support for this interface into a host, the reference has what you need. Every statement in it carries one of the four marks above, so nothing has to be taken on trust.',
  ],
  open: [
    'These are the points that can still be settled on that unit. They are taken from the reference and disappear from this list when they are done.',
  ],
  reports: [
    'Every step of the work has a dated report with what was done, what was measured and what went wrong. Newest first.',
  ],
  footer: [
    'Public domain under the [Unlicense](https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/LICENSE). Do whatever you want with it.',
    'Independent work. Not affiliated with RME or with A Tasty Pixel, the maker of Loopy Pro. Questions and corrections: [open an issue](https://github.com/ultracello/loopy-pro-rme-interface-control/issues).',
  ],
};
