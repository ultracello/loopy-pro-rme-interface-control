# Help wanted: test with your own unit

This project works out how an RME Babyface Pro FS is controlled without TotalMix FX, so that apps like Loopy Pro can support it natively. Everything so far was measured on one unit. If you own a **Babyface Pro** or **Babyface Pro FS** and a computer, you can check in a few minutes whether yours behaves the same, and close the points we cannot close alone.

You do not need to program. A small tool talks you through each task, and you can let ChatGPT or Claude guide you: [copy this prompt](PROMPT.md).

## What is open

| Task | You need | Time | What it answers |
|---|---|---|---|
| `check` | the unit and a computer | 5 min | Does another unit answer like ours? Most wanted from a Babyface Pro **without** FS. |
| `dim-key` | the same | 5 min | What the DIM key does in this mode, and whether its lamp follows a message. |
| `clock-optical` | the same; much better with a device at the optical **output** that shows what it receives (ADAT or S/PDIF) | 10 min | Clock source and optical format: the one function of the unit that is not measured yet. |
| `replug` | the power supply of the unit, and headphones | 10 min | Does the unit keep its mixer when USB is pulled while it stays powered? |

Start with `check`. Each task is separate; do as many as you like.

## What the tool does, and what it never does

Each task sends a small, fixed set of messages, which the tool lists before it starts, and asks you what you see or hear. It **never switches phantom power, never raises a level**, and it puts back what it changed or tells you how to. You confirm each task with `yes` before anything is sent. The source is one readable file: [`tools/babyface_helper.py`](../../tools/babyface_helper.py).

It is still your unit and your ears: turn monitors and headphones down before you start, and stop if anything looks wrong.

## Step by step

1. **Install Python** 3.9 or later, if you do not have it: [python.org/downloads](https://www.python.org/downloads/).
2. **Get this repository.** On its [GitHub page](https://github.com/ultracello/loopy-pro-rme-interface-control) choose Code, then Download ZIP, and unpack it. Open a terminal (Windows: PowerShell) in the unpacked folder.
3. **Install the one package the tool needs:**
   ```
   python3 -m pip install python-rtmidi
   ```
   On Windows write `py` instead of `python3`, here and below.
4. **Try the tool without a unit.** Nothing is sent anywhere:
   ```
   python3 tools/babyface_helper.py check --simulate
   ```
5. **Put the unit into class-compliant mode** (see below) and connect it to the computer by USB.
6. **Run a task:**
   ```
   python3 tools/babyface_helper.py check
   ```
   The other tasks: `dim-key`, `clock-optical`, `replug`. If the tool finds no unit, `python3 tools/babyface_helper.py ports` shows what the computer offers.
7. **Send the report** (next section), and put the unit back into its normal mode if you use it with TotalMix FX.

## Class-compliant mode

The tool talks to the unit in class-compliant mode ("CC"), the mode it uses with an iPad. With the normal RME driver the unit speaks another protocol.

- **Into CC mode:** hold SELECT and DIM while you plug in the USB cable. The level meters show **CC** for about two seconds.
- **Back to normal mode:** do the same again. The meters show **PC**.

While the unit is in CC mode, TotalMix FX on the computer does not see it. That is expected.

## Sending your result

Every task writes a file `babyface-report-<task>-<date>.json` into the folder you ran it from.

- **With a GitHub account:** [open an issue](https://github.com/ultracello/loopy-pro-rme-interface-control/issues/new?template=hardware-result.yml) and attach the file. If GitHub refuses the file type, zip it or paste its text.
- **Without one:** send the file to Matthias where you read about this project.

The file holds: the task, date, your operating system and Python version, what the unit reported, the messages that were sent, and what you typed. The serial number in the name of the MIDI port is masked. Read the file before you send it; issues are public.

A result that says "mine behaves differently" is as welcome as one that agrees.

## If something does not work

- **"No port answered like a Babyface":** the unit is probably in normal mode. Check that it shows CC when it starts.
- **`pip` fails on `python-rtmidi`:** use a Python version from python.org between 3.9 and 3.13; very new versions may have no ready-made package yet.
- **Anything else:** stop, and write what you saw into an issue. A failed attempt is a result too.

## Fireface UCX II and other RME units

Not started. The Fireface UCX II speaks a different protocol in class-compliant mode; the project [oscmix](https://github.com/michaelforney/oscmix) by Michael Forney already implements it. The tool here is for the Babyface Pro and Pro FS only and must not be used with another unit. If you own a UCX II and would test once there is something to test, [say so in an issue](https://github.com/ultracello/loopy-pro-rme-interface-control/issues/new).
