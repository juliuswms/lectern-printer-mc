# Lectern Printer MC

Generate instructions for a Lectern‑based printer / block placer used with [Eugene’s Carpet Extension](https://github.com/juliuswms/eugene-carpet-extension).

> **Note**
> This tool is developed on **Linux** and tested mainly on Fedora (KDE Plasma & Hyprland).
> Windows support is planed and comming soon.

---

## Prerequisites

- **Python 3.8+** and `pip`
- **Git**
- **Linux only:** [`ydotool`](https://github.com/ReimuNotMoe/ydotool) and its daemon running
  (see [Linux – ydotool setup](#linux--ydotool-setup) below)

---

## Linux – ydotool setup

1. **Install ydotool**

   ```bash
   # Fedora
   sudo dnf install ydotool
   # Ubuntu/Debian (from source or PPA)
   sudo apt install ydotool
   ```

2. **Start the daemon**
   The daemon must be running in the background whenever you use this script.

   ```bash
   sudo ydotoold &
   ```

   Or enable the systemd service (if provided by your package):

   ```bash
   sudo systemctl enable --now ydotool
   ```

3. Verify it works:
   ```bash
   ydotool type "test"
   ```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/juliuswms/lectern-printer-mc.git
   cd lectern-printer-mc
   ```

2. (Optional) Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Prepare a schematic of what you want to print.
   - The schematic must be **square** and **exactly one block high** (e.g., a floor pattern or map art).

2. In Minecraft, open an **empty book**.

3. Make sure the **ydotool daemon is running** (Linux only, see above).

4. Run the instruction generator:

   ```bash
   python ./src/paste_instructions.py -p /path/to/your/schematic
   ```

   (Use `-h` to see all available arguments.)

5. Wait for the generation to finish.
   During the process, magazine load schematics are created under `./schematics/output_mag[Mag number].litematic`

6. When prompted, press **any key** and **immediately focus** your Minecraft window.
   You have **3 seconds** before automatic pasting begins.

7. Wait for the pasting to complete.
   ⚠️ Check for skipped or empty pages. If any occur, you may re‑run the script.

8. The printer and carpet bot are controlled via [Eugene’s Carpet Extension](https://github.com/juliuswms/eugene-carpet-extension).

Tip: Use the minimum amount of mags needed for the print to reduce needed mag changes. Adjust the mag count with `-m`.

---

## TODO

- [x] Multi‑book support: handle prints requiring more than 101,277 instructions (span multiple books).
- [ ] Windows support: enable the tool to run on Windows (alternative input method).
- [ ] Script‑based printing: bring back scriped based lectern inputs for users who do not want to use the carpet bot.
- [ ] Video tutorial: create a video explaining how the printer works and how to use it.

---

## Contributing

Any help or improvement is welcome! Feel free to fork the repository and submit a pull request.

---

## License

MIT
