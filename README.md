# AeroVolt HomeFlow – Unified Smart Home, EV & UAV Controller for NVIDIA Project G-Assist

AeroVolt HomeFlow is a Project G-Assist plug-in that lets you control:

- 🏠 Smart-home scenes (lights, AC, plugs)
- 🚗 Electric-vehicle charging routines
- 🛸 UAV / drone patrol & return actions

…all with simple voice or text commands through G-Assist.

Example:

> “Hey homeflow, start EV charging and launch the drone patrol.”

Built with Python and IFTTT Webhooks, AeroVolt HomeFlow bridges home automation,
mobility, and AI computing on RTX™ PCs.

## Repository Structure

```text
aerovolt-homeflow/
  ├─ LICENSE 
  ├─ README.md
  ├─ manifest.json
  ├─ config.json
  ├─ plugin.py
  ├─ requirements.txt
  └─ build.bat
```

## Quick Start

1. Edit `homeflow/config.json` → paste your IFTTT key and configure scenes
   and mobility actions.
2. In `homeflow/`, run:

   ```bash
   build.bat
   ```

   This will create `dist\\g-assist-plugin-homeflow.exe`.

3. Copy the `homeflow` folder to:

   ```text
   %PROGRAMDATA%\NVIDIA Corporation\nvtopps\rise\plugins\homeflow
   ```

4. Restart G-Assist and try commands such as:

   - “run study scene”
   - “start EV home charging”
   - “let the drone patrol the backyard”

## License

MIT License — Free to use, modify, and distribute.

See LICENSE for details.
