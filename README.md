# 🚀 AeroVolt HomeFlow
**Unified Smart Home, EV & UAV Controller for NVIDIA Project G-Assist**

---

## 🧠 Overview

**AeroVolt HomeFlow** is a Python-based plug-in designed for **NVIDIA Project G-Assist**.  
It enables unified control of **Smart Home**, **Electric Vehicle (EV) charging**, and **Unmanned Aerial Vehicle (UAV) patrol** through text or voice commands.  

Built upon **IFTTT Webhooks**, the plug-in links local AI commands with physical devices, running fully on RTX™ AI PCs to demonstrate real-time **on-device intelligence for smart living**.

---

## ⚙️ Features
- 🎙️ Voice or text control for smart home scenes  
- ⚡ EV charging management — start, stop, or schedule off-peak charging  
- 🛸 UAV patrol and return-to-home actions  
- 🔗 Integration with IFTTT, Google Home, or Home Assistant  
- 💻 Fully local execution on RTX AI PCs — fast, private, and reliable  
- 🧩 Open and modular architecture for easy customization  

---

## 🧰 Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/YuanzheChen/aerovolt-homeflow.git
   cd aerovolt-homeflow
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Edit `config.json`:  
   - Insert your own IFTTT Webhooks Key in `"IFTTT_API_KEY"`.  
   - Modify event names (e.g., `aerovolt_start_ev_charging_home`) based on your IFTTT applets.

4. (Optional) Build as a G-Assist plug-in executable:
   ```bash
   build.bat
   ```

---

## 🧪 Usage

Run the plug-in directly:
```bash
python plugin.py
```

Example commands:
```bash
Hey HomeFlow, start EV charging at home
Hey HomeFlow, let the drone patrol the backyard
Hey HomeFlow, stop EV charging
Hey HomeFlow, return the drone home
```

Expected console output:
```
🚗 EV action start_ev_charging_home triggered (IFTTT event: aerovolt_start_ev_charging_home)
✅ Triggered IFTTT event successfully.
```

---

## 🎬 Demo Showcase

### Demo Overview  

This project includes a standalone visualization program `demo.py` that demonstrates the core functionality of the **AeroVolt HomeFlow plug-in**.

- **Functionality:**  
  `demo.py` simulates the smart-home control process for **EV charging** and **UAV backyard patrol**.  
  Users can trigger actions such as *Start Charging*, *Stop Charging*, *Start Patrol*, and *Return Home*.  
  The animated interface visualizes battery charge level and UAV motion, representing real-world behavior of the actual plug-in.

- **Technical Background:**  
  The demo uses the same command logic and event names as the real plug-in  
  (e.g., `start_ev_charging_home`, `uav_patrol_yard`).  
  In the real environment, these commands would be executed via **G-Assist** and **IFTTT Webhooks**  
  to control smart plugs, EV chargers, or UAV APIs.  
  In this demo, they are visualized locally through animation, allowing easy offline presentation and recording.

- **How to Run:**  
  ```bash
  python demo.py
  ```
  The demo opens a graphical interface — no hardware required.  
  It was created specifically for the NVIDIA Project G-Assist Hackathon to help judges visualize  
  the integration of smart home, EV, and UAV control through a unified AI assistant.

---

## 📜 License  
This project is released under the MIT License.  
Copyright © 2025 Yuanzhe (Anthony) Chen.  

---

## 🧩 Acknowledgments  
Developed by **Yuanzhe (Anthony) Chen** @ UNSW Sydney  
as part of the **NVIDIA Project G-Assist Plug-in Hackathon 2025**.
