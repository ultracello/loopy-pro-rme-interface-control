# Babyface Pro controller page for Loopy Pro: set-up and use

This folder holds the controller page this project uses: a Loopy Pro project with three pages of buttons, a MidiFire scene that brings the status of the controller back to the displays, and the two StreamByter rule texts behind it. With it, an RME Babyface Pro FS is controlled from inside Loopy Pro on an iPad, without TotalMix FX.

It was built for one player and one unit and has been used on exactly that set-up. Treat it as a working example, not as a product. If you want this done properly, ask for native support in your host; the [protocol reference](../docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md) is written for that.

## What you need

- An iPad with **Loopy Pro**, and the apps **StreamByter** and **MidiFire** by Audeonic (both are paid apps).
- An RME **Babyface Pro FS** in class-compliant mode, connected to the iPad. A Babyface Pro without FS should behave the same, but nobody has tried it with this page.
- TotalMix FX for iPad must not run at the same time.

## What is in the folder

| File | What it is |
|---|---|
| `Babyface Pro Controller for Loopy Pro 1.1.lpproj` | the Loopy Pro project: pages "Interface", "Inputs" and "Monitoring" |
| `Scene-Babyface Pro Controller display feedback 1.1.mfr` | the MidiFire scene for the displays |
| `StreamByter rules - controller (instance A in Loopy Pro).txt` | the rules of the controller, as text. They are already inside the project; the file is for reading. Its first lines are notes from the days each part was added; the text as a whole is what runs. |
| `StreamByter rules - filter in front of the Babyface (instance B in Loopy Pro).txt` | the rules of the filter that lets only known messages reach the unit. Also already inside the project. |

## Before you start

- Turn your monitors and headphones down. The page changes real levels on your interface.
- The page never switches phantom power. Its filter would not let such a message through.
- Your own Loopy Pro projects and MidiFire scenes are not touched; you load a separate project and a separate scene.

## Set-up, once

### 1. Put the files on the iPad

1. Install StreamByter and MidiFire first. The project holds two instances of StreamByter with their rules.
2. Download this repository (on its GitHub page: Code, then Download ZIP) and unpack it. The files are in the folder `controller`.
3. In the Files app, move the folder `Babyface Pro Controller for Loopy Pro 1.1.lpproj` to **On My iPad › Loopy Pro › Projects**.
4. Move the file `Scene-Babyface Pro Controller display feedback 1.1.mfr` to **On My iPad › MidiFire**.

### 2. MidiFire

1. Open MidiFire. If you have a set-up of your own in it, save it first: **Scenes**, then **Save**.
2. Tap **Scenes** and load "Babyface Pro Controller display feedback 1.1". Three modules appear: "Loopy Out", "UI feedback only" and "Status to Loopy". There is nothing to connect.
3. Under **Setup**, set "background idle timeout (when on battery)" to "never", so that MidiFire keeps running behind Loopy Pro.

The scene uses the ports "MidiFire 2" and "MidiFire 3" that MidiFire offers to other apps. On our iPad they were there without any setting.

### 3. Loopy Pro: connect your own Babyface

Loopy Pro ties a MIDI connection to the one unit it was made with, so the project comes with a placeholder where your unit belongs. Four taps put yours in:

1. Open the project "Babyface Pro Controller for Loopy Pro 1.1" and tap **Mixer** (bottom left).
2. In the strip "StreamByter B", under "Destinations", tap **+** ("Add Destination") and choose "Babyface Pro (…) Port 2" from the list "MIDI Destinations".
3. In the strip "StreamByter A", under "Sources", tap **+** ("Add Source") and choose "Babyface Pro (…) Port 2" from the list "MIDI Source".
4. Tap **Mixer** again to close it.

It has to be Port 2: that is the port on which the unit answers. The entries "Babyface Pro (your unit) Port 2" are the placeholders; they can stay. Save the project.

This is how far it was tested: on the iPad and the unit it was made on, with the placeholders in place and the two connections made by hand as above. There the page read and armed, stepped the headphone level and a line gain, refused a step it has to refuse, switched a pad and a reference level, and switched monitoring, pan and phase. Nobody has set it up on a second iPad yet. If the displays stay dark on yours while the levels do change, the binding of the displays to the port "MidiFire 3" did not carry over; please [tell us](https://github.com/ultracello/loopy-pro-rme-interface-control/issues/new).

## Every time you start

1. Connect everything first: hub, power, Babyface.
2. Open MidiFire and load the scene.
3. Open Loopy Pro, load the project, go to the page "Interface" and start the transport. The controller only works while the transport runs.
4. Press **READ**. The status row shows READ OK. If it does not, press READ again.
5. Press **ARM**. The status row shows ARMED; buttons, faders and switches now work. The page locks itself a minute after the last press, and **LOCK** locks it at once.

## The page "Interface"

- **Main and headphone level**: a fader and a dB display for each, and buttons for −0.5, −1, −2, −3, −6 dB and the same upwards.
- **Any step**: the slider "Step width" sets a step from 0.5 to 30 dB; "MAIN − STEP", "MAIN + STEP", "PHONES − STEP" and "PHONES + STEP" apply it. A step that would go above 0 dB or below −63.5 dB is refused. Large steps upwards are loud: look at the display first.
- **Mute**: "MAIN OUT · MUTE ↔ BACK" and "PHONES · MUTE ↔ BACK" mute an output and bring back exactly the level from before. If an output is found muted and the page does not know the level from before (lamp "59 NO REF"), the switch sets a fixed, quiet −30 dB.
- **HEADPHONE ROUTE · RESTORE** sends the playback of the iPad to the headphones at 0 dB. The unit forgets its mixer whenever it loses power, and then the headphones are silent until this is sent.

## The page "Inputs"

- **Gain** of the four inputs: microphone inputs 1 and 2 from 0 to 65 dB in whole dB, line inputs 3 and 4 from 0 to 9 dB in half dB. Take care with large steps up on a microphone input.
- **IN1 PAD, IN2 PAD** switch the pad of a microphone input. Lamps below show pad and 48 V as the unit reports them. 48 V cannot be switched from this page; while the unit reports 48 V as on, the page refuses to switch the pad, because both sit in one message.
- **IN3 +4 ↔ −10, IN4 +4 ↔ −10** switch the reference level of a line input. In the "−10" position the input is 8.7 dB more sensitive.

## The page "Monitoring"

What you hear on the headphones, without TotalMix FX. Five columns: MON1 to MON4 are the four inputs, PB is the playback of the iPad. Each has:

- **ON/OFF**, a level from −60 to 0 dB, and a state display: "?", OFF or ON.
- **Pan** with ◀, MID and ▶.
- **Ø**, which inverts the phase of that way to the headphones. Useful when you hear your instrument both directly and through Loopy Pro.

The unit does not report its mixer. The page remembers what it has sent, so after loading the project every column shows "?" until you press its ON/OFF once. Monitoring goes to the headphones only, never to the main output.

## The row "Reason"

It says why the page did not do what you wanted.

| Lamp | Meaning |
|---|---|
| OK | all is well |
| TIMED OUT | the minute after the last press is over: READ, ARM |
| READ FIRST | you pressed before the page had read and was armed |
| NO REPLY | the unit did not answer: check the connection |
| LEVEL DIFFERS | the level was changed elsewhere, or came back different: READ and try again |
| REFUSED | nothing was written: end of the range, the output is muted, or the page was still busy |
| FAULT | the transport is stopped, or something went wrong on the way: check the transport, READ |

## After the interface was unplugged

Levels, gains and input settings survive. The mixer is gone, so the headphones are silent.

1. READ, then ARM. ARM sends again every way to the headphones you have switched since you loaded the project.
2. If the displays do not move, tap MidiFire once and come back to Loopy Pro, then READ and ARM again. iPadOS pauses MidiFire when the interface disappears; the control itself does not need MidiFire, only the displays do.
3. If the column PB still shows "?", press "HEADPHONE ROUTE · RESTORE".

## If a switch answers FAULT

The page writes a setting (pad, reference level) only when it knows every bit of the settings the unit reports; otherwise it answers FAULT and writes nothing. One such bit is known and allowed: the one the unit sets while its own OUT key stands on "Opt". With version 1.0 of this page that bit locked the pad switches; since 1.1 they work with OUT on "Opt" as well, and the selection on the unit stays as it is.

If a switch still answers FAULT, the unit reports something this page has not seen. Press READ and try again, and if it stays, please [tell us](https://github.com/ultracello/loopy-pro-rme-interface-control/issues/new) what you had set on the unit.

## What it does not do

Equaliser and low cut, loopback, the levels of the AS and ADAT outputs, playback or inputs on the main output, phantom power. The [coverage table](../docs/protocol/BABYFACE-PRO-FS-CC-REFERENCE.md#5-coverage-against-what-totalmix-fx-offers) of the reference says what the unit can do beyond this page.

## How it is wired

StreamByter instance A inside Loopy Pro is the controller: the buttons of the pages send it MIDI, it builds the messages for the unit, receives the answers of the unit and checks every one. Instance B sits between A and the Babyface and lets only known messages pass. What the displays of the page show, A sends out as MIDI on the port "MidiFire 2"; MidiFire lets only those status messages pass and hands them back to Loopy Pro on "MidiFire 3", where a control profile of the project turns them into lamps and numbers.

## Licence

Public domain under the Unlicense, like the rest of this repository. No warranty. Not affiliated with RME, Audeonic or A Tasty Pixel.
