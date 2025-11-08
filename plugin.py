\
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    """
    AeroVolt HomeFlow - IFTTT-based Smart Home, EV and UAV Controller for NVIDIA Project G-Assist

    This plugin lets users control:
      - Smart home scenes (lights, AC, plugs, etc.)
      - EV (electric vehicle) home charging routines
      - UAV (drone) patrol & return actions

    All actions are mapped to IFTTT Webhooks events so they can interface with
    a wide range of devices and home automation platforms.

    Example commands:
      - "Hey homeflow, run the study scene."
      - "Hey homeflow, start my EV home charging."
      - "Hey homeflow, schedule off-peak EV charging."
      - "Hey homeflow, let the drone patrol the backyard."
      - "Hey homeflow, tell the UAV to return home."
      - "Hey homeflow, list my mobility actions."
      - "Hey homeflow, list my home scenes."

    The plugin communicates with G-Assist over Windows pipes using JSON messages
    terminated with the marker `<<END>>`, following the official example.
    """

    import json
    import logging
    import os
    import sys
    import time
    from typing import Any, Dict, Optional

    import requests

    # -------------------------
    # Configuration & Constants
    # -------------------------

    CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    LOG_FILE_PATH = os.path.join(os.path.expanduser("~"), "HomeFlow_plugin.log")
    IFTTT_BASE_URL = "https://maker.ifttt.com/trigger/{event_name}/with/key/{api_key}"


    # -------------------------
    # Logging Setup
    # -------------------------

    def setup_logging() -> None:
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        logging.basicConfig(
            filename=LOG_FILE_PATH,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        # Also log to stderr for easier debugging when run from console
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)


    # -------------------------
    # Config Handling
    # -------------------------

    def load_config() -> Dict[str, Any]:
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
                logging.info("Config loaded successfully from %s", CONFIG_PATH)
                return config
        except FileNotFoundError:
            logging.error("Config file not found at %s", CONFIG_PATH)
        except json.JSONDecodeError as e:
            logging.error("Failed to parse config.json: %s", e)

        # Fallback to safe defaults (no real key)
        return {
            "IFTTT_API_KEY": "",
            "DEFAULT_TIMEOUT_SECONDS": 10,
            "SCENES": {},
            "MOBILITY_ACTIONS": {}
        }


    CONFIG: Dict[str, Any] = {}


    def get_ifttt_api_key() -> str:
        api_key = CONFIG.get("IFTTT_API_KEY", "").strip()
        return api_key


    def get_timeout_seconds() -> int:
        try:
            return int(CONFIG.get("DEFAULT_TIMEOUT_SECONDS", 10))
        except Exception:
            return 10


    def get_scenes() -> Dict[str, str]:
        scenes = CONFIG.get("SCENES", {})
        if not isinstance(scenes, dict):
            return {}
        return scenes


    def get_mobility_actions() -> Dict[str, str]:
        """
        Mobility actions cover EV and UAV-related commands.
        Example keys:
          - "start_ev_charging_home"
          - "ev_off_peak_schedule"
          - "uav_patrol_yard"
          - "uav_return_home"
        """
        actions = CONFIG.get("MOBILITY_ACTIONS", {})
        if not isinstance(actions, dict):
            return {}
        return actions


    # -------------------------
    # G-Assist IPC Helpers
    # -------------------------

    def read_command() -> Optional[Dict[str, Any]]:
        """
        Read a JSON command from stdin until the terminator '<<END>>' is encountered.
        Returns the parsed dict, or None if parsing fails.
        """
        buffer = ""
        terminator = "<<END>>"

        while True:
            chunk = sys.stdin.read(1)
            if chunk == "":
                # EOF or no data
                time.sleep(0.01)
                if buffer.strip():
                    # Try to parse any remaining partial JSON (best-effort)
                    break
                return None

            buffer += chunk

            if buffer.endswith(terminator):
                buffer = buffer[: -len(terminator)]
                break

        buffer = buffer.strip()
        if not buffer:
            return None

        try:
            command = json.loads(buffer)
            logging.info("Received command: %s", command)
            return command
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON command: %s", e)
            return None


    def write_response(response: Dict[str, Any]) -> None:
        """
        Write a JSON response followed by '<<END>>' to stdout.
        """
        try:
            payload = json.dumps(response, ensure_ascii=False)
        except TypeError as e:
            logging.error("Failed to encode response to JSON: %s", e)
            payload = json.dumps(
                {"success": False, "message": "Internal JSON encoding error"},
                ensure_ascii=False,
            )

        logging.info("Sending response: %s", payload)
        sys.stdout.write(payload + "<<END>>")
        sys.stdout.flush()


    # -------------------------
    # IFTTT Helpers
    # -------------------------

    def build_ifttt_url(event_name: str, api_key: str) -> str:
        return IFTTT_BASE_URL.format(event_name=event_name, api_key=api_key)


    def call_ifttt_event(
        event_name: str,
        value1: Optional[str] = None,
        value2: Optional[str] = None,
        value3: Optional[str] = None,
    ) -> Dict[str, Any]:
        api_key = get_ifttt_api_key()
        if not api_key:
            logging.error("IFTTT_API_KEY is missing in config.json")
            return {
                "success": False,
                "message": (
                    "❌ IFTTT_API_KEY is not configured. "
                    "Please edit config.json and set your Webhooks key."
                ),
            }

        url = build_ifttt_url(event_name, api_key)
        timeout = get_timeout_seconds()

        payload: Dict[str, Optional[str]] = {}
        if value1 is not None:
            payload["value1"] = value1
        if value2 is not None:
            payload["value2"] = value2
        if value3 is not None:
            payload["value3"] = value3

        logging.info("Calling IFTTT event '%s' with payload=%s", event_name, payload)

        try:
            response = requests.post(url, json=payload or None, timeout=timeout)
            response.raise_for_status()
            return {
                "success": True,
                "message": (
                    f"✅ Triggered IFTTT event **{event_name}**.\n"
                    f"HTTP status: {response.status_code}"
                ),
            }
        except requests.exceptions.RequestException as e:
            logging.error("Error calling IFTTT event '%s': %s", event_name, e)
            return {
                "success": False,
                "message": (
                    f"❌ Failed to trigger IFTTT event **{event_name}**.\n"
                    f"Error: `{e}`"
                ),
            }


    # -------------------------
    # Command Implementations
    # -------------------------

    def initialize_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Optional initialize hook. Can be used by G-Assist to warm up the plugin.
        """
        scenes = get_scenes()
        mobility = get_mobility_actions()

        scene_list = ", ".join(sorted(scenes.keys())) if scenes else "no scenes configured"
        mobility_list = (
            ", ".join(sorted(mobility.keys())) if mobility else "no mobility actions configured"
        )

        return {
            "success": True,
            "message": (
                "AeroVolt HomeFlow initialized.\n"
                f"- Scenes: {len(scenes)} ({scene_list})\n"
                f"- Mobility actions (EV/UAV): {len(mobility)} ({mobility_list})"
            ),
        }


    def shutdown_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        logging.info("Shutdown requested by G-Assist")
        return {
            "success": True,
            "message": "AeroVolt HomeFlow shutting down.",
        }


    def run_scene_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if params is None:
            params = {}

        scene_raw = params.get("scene", "")
        if not isinstance(scene_raw, str) or not scene_raw.strip():
            return {
                "success": False,
                "message": "❌ Missing required parameter `scene`.",
            }

        scene_key = scene_raw.strip().lower()
        scenes = get_scenes()
        event_name = scenes.get(scene_key)

        if not event_name:
            # Try fuzzy match: simple substring search
            candidates = [
                name for name in scenes.keys()
                if scene_key in name.lower() or name.lower() in scene_key
            ]
            if candidates:
                event_name = scenes[candidates[0]]
                scene_key = candidates[0]
            else:
                if not scenes:
                    return {
                        "success": False,
                        "message": (
                            "❌ No scenes configured yet. "
                            "Please edit `config.json` and add entries under `SCENES`."
                        ),
                    }
                scene_list = ", ".join(sorted(scenes.keys()))
                return {
                    "success": False,
                    "message": (
                        f"❌ Scene **{scene_raw}** is not configured.\n"
                        f"Available scenes: {scene_list}."
                    ),
                }

        result = call_ifttt_event(event_name)
        if result.get("success"):
            result["message"] = (
                f"🏠 Scene **{scene_key}** triggered "
                f"(IFTTT event: `{event_name}`).\n" + result["message"]
            )
        return result


    def trigger_ifttt_event_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if params is None:
            params = {}

        event_name = params.get("event_name", "")
        if not isinstance(event_name, str) or not event_name.strip():
            return {
                "success": False,
                "message": "❌ Missing required parameter `event_name`.",
            }

        value1 = params.get("value1")
        value2 = params.get("value2")
        value3 = params.get("value3")

        return call_ifttt_event(
            event_name=event_name.strip(),
            value1=value1,
            value2=value2,
            value3=value3,
        )


    def list_scenes_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        scenes = get_scenes()
        if not scenes:
            return {
                "success": True,
                "message": (
                    "ℹ️ No scenes are configured yet. "
                    "Edit `config.json` and add entries under `SCENES` like:\n"
                    "```json\n"
                    "\"SCENES\": {\n"
                    "  \"study\": \"aerovolt_study\",\n"
                    "  \"sleep\": \"aerovolt_sleep\"\n"
                    "}\n"
                    "```"
                ),
            }

        lines = ["✅ AeroVolt HomeFlow scenes:"]
        for name, event in sorted(scenes.items()):
            lines.append(f"- **{name}** → IFTTT event `{event}`")

        return {
            "success": True,
            "message": "\n".join(lines),
        }


    def run_mobility_action_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Execute an EV/UAV mobility action mapped in MOBILITY_ACTIONS.

        Typical actions:
          - start_ev_charging_home
          - stop_ev_charging_home
          - ev_off_peak_schedule
          - uav_patrol_yard
          - uav_return_home
        """
        if params is None:
            params = {}

        action_raw = params.get("action", "")
        if not isinstance(action_raw, str) or not action_raw.strip():
            return {
                "success": False,
                "message": "❌ Missing required parameter `action`.",
            }

        action_key = action_raw.strip().lower()
        actions = get_mobility_actions()
        event_name = actions.get(action_key)

        if not event_name:
            # Simple fuzzy match
            candidates = [
                name for name in actions.keys()
                if action_key in name.lower() or name.lower() in action_key
            ]
            if candidates:
                event_name = actions[candidates[0]]
                action_key = candidates[0]
            else:
                if not actions:
                    return {
                        "success": False,
                        "message": (
                            "❌ No mobility actions configured yet. "
                            "Please edit `config.json` and add entries under `MOBILITY_ACTIONS`."
                        ),
                    }
                action_list = ", ".join(sorted(actions.keys()))
                return {
                    "success": False,
                    "message": (
                        f"❌ Mobility action **{action_raw}** is not configured.\n"
                        f"Available actions: {action_list}."
                    ),
                }

        result = call_ifttt_event(event_name)
        if result.get("success"):
            # 根据名字简单区分 EV / UAV 做一点文案润色
            if "uav" in action_key or "drone" in action_key:
                prefix = "🛸 UAV/Drone action"
            elif "ev" in action_key or "charging" in action_key or "vehicle" in action_key:
                prefix = "🚗 EV action"
            else:
                prefix = "🚀 Mobility action"

            result["message"] = (
                f"{prefix} **{action_key}** triggered "
                f"(IFTTT event: `{event_name}`).\n" + result["message"]
            )
        return result


    def list_mobility_actions_command(
        params: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system_info: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        actions = get_mobility_actions()
        if not actions:
            return {
                "success": True,
                "message": (
                    "ℹ️ No mobility actions are configured yet. "
                    "Edit `config.json` and add entries under `MOBILITY_ACTIONS` like:\n"
                    "```json\n"
                    "\"MOBILITY_ACTIONS\": {\n"
                    "  \"start_ev_charging_home\": \"aerovolt_start_ev_charging_home\",\n"
                    "  \"uav_patrol_yard\": \"aerovolt_uav_patrol_yard\"\n"
                    "}\n"
                    "```"
                ),
            }

        lines = ["✅ AeroVolt HomeFlow mobility actions (EV/UAV):"]
        for name, event in sorted(actions.items()):
            if "uav" in name or "drone" in name:
                icon = "🛸"
            elif "ev" in name or "charging" in name or "vehicle" in name:
                icon = "🚗"
            else:
                icon = "🚀"
            lines.append(f"- {icon} **{name}** → IFTTT event `{event}`")

        return {
            "success": True,
            "message": "\n".join(lines),
        }


    # -------------------------
    # Main Loop
    # -------------------------

    def main() -> None:
        global CONFIG

        setup_logging()
        logging.info("AeroVolt HomeFlow plugin starting up.")
        CONFIG = load_config()

        commands = {
            "initialize": initialize_command,
            "shutdown": shutdown_command,
            "run_scene": run_scene_command,
            "trigger_ifttt_event": trigger_ifttt_event_command,
            "list_scenes": list_scenes_command,
            "run_mobility_action": run_mobility_action_command,
            "list_mobility_actions": list_mobility_actions_command,
        }

        while True:
            command = read_command()
            if command is None:
                # No valid command received; continue waiting
                continue

            tool_calls = command.get("tool_calls", [])
            if not isinstance(tool_calls, list):
                logging.error("Invalid command: tool_calls is not a list")
                continue

            for tool_call in tool_calls:
                func_name = tool_call.get("func")
                params = tool_call.get("params", {})

                if func_name == "shutdown":
                    response = shutdown_command(params)
                    write_response(response)
                    logging.info("AeroVolt HomeFlow plugin exiting after shutdown.")
                    return

                func = commands.get(func_name)
                if not func:
                    logging.error("Unknown function requested: %s", func_name)
                    write_response(
                        {
                            "success": False,
                            "message": f"❌ Unknown function `{func_name}`.",
                        }
                    )
                    continue

                try:
                    response = func(
                        params=params,
                        context=command.get("context"),
                        system_info=command.get("system_info"),
                    )
                except Exception as e:
                    logging.exception("Error executing function %s: %s", func_name, e)
                    response = {
                        "success": False,
                        "message": (
                            f"❌ Internal error while executing `{func_name}`: `{e}`"
                        ),
                    }

                write_response(response)


    if __name__ == "__main__":
        main()
