import tkinter as tk
from tkinter import ttk

class AeroVoltDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AeroVolt HomeFlow – EV & UAV Demo")
        self.geometry("900x500")
        self.resizable(False, False)

        self.configure(bg="#1e1e1e")

        self._create_styles()
        self._create_layout()

        # EV state
        self.ev_soc = 20  # %
        self.ev_charging = False

        # UAV state
        self.uav_x = 80
        self.uav_y = 80
        self.uav_radius = 10
        self.uav_patrolling = False
        self.uav_returning = False
        self.uav_path_index = 0
        self.uav_path_points = [
            (80, 80),
            (320, 80),
            (320, 260),
            (80, 260),
            (80, 80),
        ]

        self._draw_ev_battery()
        self._draw_uav_scene()

        # start animation loops
        self.after(200, self._ev_loop)
        self.after(80, self._uav_loop)

    def _create_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#1e1e1e")
        style.configure("Title.TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 16, "bold"))
        style.configure("Body.TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
        style.configure("Small.TLabel", background="#1e1e1e", foreground="#cccccc", font=("Segoe UI", 9))
        style.configure("Aero.TButton", font=("Segoe UI", 10, "bold"))

    def _create_layout(self):
        root_frame = ttk.Frame(self)
        root_frame.pack(fill="both", expand=True, padx=16, pady=16)

        # EV frame
        ev_frame = ttk.Frame(root_frame)
        ev_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        ev_title = ttk.Label(ev_frame, text="EV Home Charging", style="Title.TLabel")
        ev_title.pack(anchor="w")

        ev_sub = ttk.Label(
            ev_frame,
            text="Simulated battery state for AeroVolt HomeFlow EV actions.",
            style="Small.TLabel",
        )
        ev_sub.pack(anchor="w", pady=(0, 8))

        self.ev_canvas = tk.Canvas(
            ev_frame, width=360, height=260, bg="#252526", highlightthickness=0
        )
        self.ev_canvas.pack(pady=(0, 8))

        btn_row = ttk.Frame(ev_frame)
        btn_row.pack(anchor="w", pady=(4, 0))

        self.ev_start_btn = ttk.Button(
            btn_row,
            text="Start EV Charging",
            style="Aero.TButton",
            command=self._start_ev_charging,
        )
        self.ev_start_btn.grid(row=0, column=0, padx=(0, 4))

        self.ev_stop_btn = ttk.Button(
            btn_row,
            text="Stop EV Charging",
            style="Aero.TButton",
            command=self._stop_ev_charging,
        )
        self.ev_stop_btn.grid(row=0, column=1, padx=(0, 4))

        self.ev_label = ttk.Label(
            ev_frame, text="Status: Idle · SOC: 20%", style="Body.TLabel"
        )
        self.ev_label.pack(anchor="w", pady=(4, 0))

        # UAV frame
        uav_frame = ttk.Frame(root_frame)
        uav_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        uav_title = ttk.Label(uav_frame, text="UAV Backyard Patrol", style="Title.TLabel")
        uav_title.pack(anchor="w")

        uav_sub = ttk.Label(
            uav_frame,
            text="Simulated drone patrol path for AeroVolt HomeFlow UAV actions.",
            style="Small.TLabel",
        )
        uav_sub.pack(anchor="w", pady=(0, 8))

        self.uav_canvas = tk.Canvas(
            uav_frame, width=360, height=260, bg="#252526", highlightthickness=0
        )
        self.uav_canvas.pack(pady=(0, 8))

        uav_btn_row = ttk.Frame(uav_frame)
        uav_btn_row.pack(anchor="w", pady=(4, 0))

        self.uav_patrol_btn = ttk.Button(
            uav_btn_row,
            text="Start Patrol",
            style="Aero.TButton",
            command=self._start_uav_patrol,
        )
        self.uav_patrol_btn.grid(row=0, column=0, padx=(0, 4))

        self.uav_return_btn = ttk.Button(
            uav_btn_row,
            text="Return Home",
            style="Aero.TButton",
            command=self._return_uav_home,
        )
        self.uav_return_btn.grid(row=0, column=1, padx=(0, 4))

        self.uav_label = ttk.Label(
            uav_frame, text="Status: On standby at home", style="Body.TLabel"
        )
        self.uav_label.pack(anchor="w", pady=(4, 0))

        # Make columns expand equally
        root_frame.columnconfigure(0, weight=1)
        root_frame.columnconfigure(1, weight=1)

    # -------- EV drawing & loop --------
    def _draw_ev_battery(self):
        self.ev_canvas.delete("all")

        # Battery body
        x0, y0, x1, y1 = 60, 60, 300, 200
        self.ev_canvas.create_rectangle(
            x0, y0, x1, y1, outline="#cccccc", width=3
        )
        # Battery tip
        self.ev_canvas.create_rectangle(
            x1, 100, x1 + 12, 160, outline="#cccccc", width=3, fill="#1e1e1e"
        )

        # Fill level
        fill_margin = 6
        inner_x0 = x0 + fill_margin
        inner_y0 = y0 + fill_margin
        inner_x1 = x1 - fill_margin
        inner_y1 = y1 - fill_margin

        soc_frac = max(0.0, min(1.0, self.ev_soc / 100.0))
        w = inner_x1 - inner_x0
        fill_x1 = inner_x0 + w * soc_frac

        # Color changes with SOC
        if soc_frac < 0.3:
            fill_color = "#d16969"  # red
        elif soc_frac < 0.7:
            fill_color = "#dcdcaa"  # yellow
        else:
            fill_color = "#6a9955"  # green

        self.ev_canvas.create_rectangle(
            inner_x0, inner_y0, fill_x1, inner_y1, fill=fill_color, width=0
        )

        # Text
        self.ev_canvas.create_text(
            (x0 + x1) / 2,
            y1 + 30,
            text=f"State of Charge: {self.ev_soc:.0f}%",
            fill="white",
            font=("Segoe UI", 12, "bold"),
        )

        # Label for integration hint
        self.ev_canvas.create_text(
            (x0 + x1) / 2,
            y0 - 25,
            text="EV action example: start_ev_charging_home",
            fill="#bbbbbb",
            font=("Segoe UI", 9),
        )

    def _ev_loop(self):
        if self.ev_charging:
            # slow charge
            self.ev_soc += 0.6
            if self.ev_soc >= 100:
                self.ev_soc = 100
                self.ev_charging = False
            self._draw_ev_battery()

        status = "Charging" if self.ev_charging else "Idle"
        self.ev_label.config(
            text=f"Status: {status} · SOC: {self.ev_soc:.0f}%"
        )
        self.after(300, self._ev_loop)

    def _start_ev_charging(self):
        self.ev_charging = True

    def _stop_ev_charging(self):
        self.ev_charging = False

    # -------- UAV drawing & loop --------
    def _draw_uav_scene(self):
        self.uav_canvas.delete("all")

        # Yard rectangle
        yard_x0, yard_y0, yard_x1, yard_y1 = 40, 40, 340, 240
        self.uav_canvas.create_rectangle(
            yard_x0, yard_y0, yard_x1, yard_y1, outline="#cccccc", width=2
        )
        self.uav_canvas.create_text(
            70,
            30,
            text="Backyard",
            fill="#bbbbbb",
            anchor="w",
            font=("Segoe UI", 9),
        )

        # Patrol path (simple rectangle)
        self.uav_canvas.create_line(
            80,
            80,
            320,
            80,
            320,
            260,
            80,
            260,
            80,
            80,
            fill="#3fc6ff",
            dash=(4, 2),
        )

        # Home position
        self.uav_canvas.create_oval(72, 72, 88, 88, outline="#6a9955", width=2)
        self.uav_canvas.create_text(
            95,
            78,
            text="Home",
            fill="#6a9955",
            anchor="w",
            font=("Segoe UI", 9),
        )

        # UAV (drone)
        r = self.uav_radius
        self.uav_canvas.create_oval(
            self.uav_x - r,
            self.uav_y - r,
            self.uav_x + r,
            self.uav_y + r,
            fill="#3fc6ff",
            outline="white",
        )
        # heading indicator
        self.uav_canvas.create_line(
            self.uav_x,
            self.uav_y,
            self.uav_x,
            self.uav_y - r * 1.8,
            fill="white",
            width=2,
        )

        self.uav_canvas.create_text(
            200,
            260 + 25,
            text="UAV actions: uav_patrol_yard · uav_return_home",
            fill="#bbbbbb",
            font=("Segoe UI", 9),
        )

    def _uav_loop(self):
        if self.uav_patrolling:
            self._step_along_path()
            self.uav_label.config(text="Status: Patrolling backyard perimeter")
        elif self.uav_returning:
            self._step_towards_home()
            self.uav_label.config(text="Status: Returning to home")
        else:
            self.uav_label.config(text="Status: On standby at home")

        self._draw_uav_scene()
        self.after(80, self._uav_loop)

    def _start_uav_patrol(self):
        self.uav_patrolling = True
        self.uav_returning = False
        self.uav_path_index = 0

    def _return_uav_home(self):
        self.uav_patrolling = False
        self.uav_returning = True

    def _step_along_path(self):
        if not self.uav_path_points:
            return

        target_x, target_y = self.uav_path_points[self.uav_path_index]
        dx = target_x - self.uav_x
        dy = target_y - self.uav_y
        dist = max((dx ** 2 + dy ** 2) ** 0.5, 1e-6)
        step = 4.0

        if dist < step:
            # reached this waypoint
            self.uav_x, self.uav_y = target_x, target_y
            self.uav_path_index = (self.uav_path_index + 1) % len(self.uav_path_points)
        else:
            self.uav_x += step * dx / dist
            self.uav_y += step * dy / dist

    def _step_towards_home(self):
        home_x, home_y = self.uav_path_points[0]
        dx = home_x - self.uav_x
        dy = home_y - self.uav_y
        dist = max((dx ** 2 + dy ** 2) ** 0.5, 1e-6)
        step = 5.0

        if dist < step:
            self.uav_x, self.uav_y = home_x, home_y
            self.uav_returning = False
        else:
            self.uav_x += step * dx / dist
            self.uav_y += step * dy / dist


if __name__ == "__main__":
    app = AeroVoltDemo()
    app.mainloop()