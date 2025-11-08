# 🚀 AeroVolt HomeFlow
**Unified Smart Home, EV & UAV Controller for NVIDIA Project G-Assist**

---

## 🧠 Overview / 项目简介

**AeroVolt HomeFlow** 是一个为 **NVIDIA Project G-Assist** 设计的 Python 插件，
通过语音或文本指令实现对 **智能家居 (Smart Home)**、**电动车充电 (EV Charging)** 与 **无人机巡逻 (UAV Patrol)** 的统一控制。

该插件基于 **IFTTT Webhooks** 实现设备联动，可运行在 RTX™ AI PC 上的本地 G-Assist 环境中，实现真正的 **边缘端 AI 智能家居控制**。

---

## ⚙️ Features / 功能特性
- 🎙️ **语音/文本控制智能家居**（如灯光、空调、学习模式）
- ⚡ **电动车充电控制 (EV)**：支持启动、停止与离峰时段调度
- 🛸 **无人机控制 (UAV)**：支持后院自动巡逻与返航命令
- 🔗 **IFTTT / Google Home / Home Assistant 集成**
- 💻 **完全本地执行**，隐私安全，响应迅速
- 🧩 **开放结构**，可扩展更多自定义命令与设备

---

## 🧰 Installation / 安装与配置

1. 克隆或下载仓库：
   ```bash
   git clone https://github.com/YuanzheChen/aerovolt-homeflow.git
   cd aerovolt-homeflow
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 编辑配置文件 `config.json`：
   - 在 `"IFTTT_API_KEY"` 处填入你自己的 IFTTT Webhooks Key
   - 根据你的 IFTTT Applet 修改事件名（例如 `aerovolt_start_ev_charging_home`）

4. 可选：编译为 G-Assist 插件可执行文件
   ```bash
   build.bat
   ```

---

## 🧪 Usage / 使用方法

运行插件测试：
```bash
python plugin.py
```

示例命令：
```bash
Hey HomeFlow, start EV charging at home
Hey HomeFlow, let the drone patrol the backyard
Hey HomeFlow, stop EV charging
Hey HomeFlow, return the drone home
```

日志中会输出：
```
🚗 EV action start_ev_charging_home triggered (IFTTT event: aerovolt_start_ev_charging_home)
✅ Triggered IFTTT event successfully.
```

---

## 🎬 Demo 演示说明 / Demo Showcase

### 🇨🇳 中文说明  

本项目包含一个独立的可视化演示程序 `demo.py`，用于展示 **AeroVolt HomeFlow 插件** 的核心功能与逻辑。  

- **功能说明：**  
  `demo.py` 模拟了智能家居场景中 **电动车（EV）充电控制** 与 **无人机（UAV）后院巡逻** 的过程。  
  用户可以通过界面按钮触发“开始充电”、“停止充电”、“开始巡逻”、“返回基站”等操作。  
  对应的动画展示了电池电量变化和无人机路径移动，形象地呈现了插件在真实环境中的控制效果。  

- **技术原理：**  
  该演示程序与实际插件共用相同的命令逻辑与事件名称（如 `start_ev_charging_home`、`uav_patrol_yard`）。  
  在真实环境中，这些命令通过 G-Assist 插件触发 **IFTTT Webhooks**，可控制智能插座、充电桩、  
  或无人机控制节点；而在 Demo 中，这些操作通过动画可视化展示，便于离线演示与评审观看。  

- **演示方式：**  
  运行命令：  
  ```bash
  python demo.py
  ```  
  即可打开图形化界面，无需额外硬件设备。  
  Demo 用于 Hackathon 视频录制，帮助评审快速理解 HomeFlow 的工作机制。  

---

### 🇬🇧 English Description  

This project includes a standalone visualization program `demo.py` that demonstrates the core functionality of the **AeroVolt HomeFlow plug-in**.  

- **Overview:**  
  `demo.py` simulates smart-home control of an **electric vehicle (EV)** and an **unmanned aerial vehicle (UAV)**.  
  Users can trigger actions such as *Start Charging*, *Stop Charging*, *Start Patrol*, and *Return Home*.  
  The animation shows EV battery charging progress and UAV patrol motion in a backyard scene.  

- **Technical Background:**  
  The demo uses the same action logic and event names as the real plug-in  
  (e.g., `start_ev_charging_home`, `uav_patrol_yard`).  
  In the actual implementation, these commands are executed through G-Assist using **IFTTT Webhooks**  
  to control physical devices such as smart plugs, chargers, or drones.  
  In the demo, these actions are visualized through animation, enabling full demonstration without hardware.  

- **How to Run:**  
  ```bash
  python demo.py
  ```  
  The demo is self-contained and runs locally.  
  It was created specifically for the NVIDIA Project G-Assist Hackathon to help judges visualize  
  the integrated control logic of home, vehicle, and UAV systems.  

---

## 📜 License  
This project is released under the MIT License.  
Copyright © 2025 Yuanzhe (Anthony) Chen.  

---

## 🧩 Acknowledgments  
Developed by **Yuanzhe (Anthony) Chen** @ UNSW Sydney  
as part of the **NVIDIA Project G-Assist Plug-in Hackathon 2025**.
