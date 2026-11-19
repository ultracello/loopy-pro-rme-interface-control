# Prompt for your AI assistant

Copy everything in the box into ChatGPT, Claude or another assistant, and add one line about your computer (for example "I use Windows 11"). The assistant then guides you through one task.

```
I want to help an open hardware project by running a short test with my RME Babyface Pro / Babyface Pro FS.
Please guide me through it step by step, one step at a time, and wait for my answer after each step.

Project: https://github.com/ultracello/loopy-pro-rme-interface-control
Instructions for helpers: https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/docs/help-wanted/README.md
The tool I will run: https://github.com/ultracello/loopy-pro-rme-interface-control/blob/main/tools/babyface_helper.py

If you can open these pages, read the instructions first and follow them exactly. If you cannot, use this summary:

1. I need Python 3.9 to 3.13 and the package python-rtmidi (python3 -m pip install python-rtmidi; on Windows "py" instead of "python3").
2. I download the repository as a ZIP from its GitHub page (Code, Download ZIP), unpack it and open a terminal in that folder.
3. Dry run without hardware: python3 tools/babyface_helper.py check --simulate
4. The unit must be in class-compliant mode: hold SELECT and DIM while plugging in the USB cable; the meters show CC.
   The same procedure switches back to normal mode later (the meters then show PC).
5. Real run: python3 tools/babyface_helper.py check
   Other tasks: dim-key, clock-optical, replug. If no unit is found: python3 tools/babyface_helper.py ports
6. The tool writes a file babyface-report-<task>-<date>.json. I attach it to a new GitHub issue in the project
   (template "Hardware result"), or send it to the person who asked for help.

Rules for you:
- Help me install and run this tool and understand what it prints. Do not write other programs that send MIDI or SysEx
  to my unit, and do not suggest sending any message the tool does not send itself.
- Never suggest switching phantom power (48 V) or raising any level.
- Remind me to turn my monitors and headphones down before a task starts.
- If something fails, help me find the cause (wrong mode, missing package, wrong folder). If it cannot be solved,
  help me write down what happened so I can report it. A failed attempt is a useful result.
- When I am done, remind me to switch the unit back to normal mode if I use it with TotalMix FX.

Start by asking which operating system I use and which task I want to do. If I do not know, suggest "check".
```
