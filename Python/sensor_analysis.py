import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
import warnings
warnings.filterwarnings("ignore")


#################### MASS PROPERTIES FROM ONSHAPE
bracket = {
    "name":         "Sensor Mounting Bracket",
    "mass_lb":      0.93,
    "volume_in3":   9.467,
    "cg_x_in":      1.010,
    "cg_y_in":      0.000,
    "cg_z_in":      1.321,
    "Lxx": 2.194, "Lxy": 0.000,  "Lxz": 0.757,
    "Lyx": 0.000, "Lyy": 2.788,  "Lyz": -5.465e-12,
    "Lzx": 0.757, "Lzy": -5.465e-12, "Lzz": 2.118,
}

assembly = {
    "name":         "Sensor Mount Assembly (Bracket + Sensor Body)",
    "mass_lb":      2.303,
    "volume_in3":   23.441,
    "surface_area_in2": 84.05,
    "cg_x_in":      -0.256,
    "cg_y_in":      -8.496e-5,   
    "cg_z_in":      -1.174,
    "Lxx": 5.235,  "Lxy": 2.610e-6,  "Lxz": 1.334,
    "Lyx": 2.610e-6, "Lyy": 6.680,   "Lyz": -1.250e-7,
    "Lzx": 1.334,  "Lzy": -1.250e-7, "Lzz": 3.631,
}

sensor = {
    "name":    "Air Data Sensor Body",
    "mass_lb": round(assembly["mass_lb"] - bracket["mass_lb"], 4),
}


#################### WEIGHT AND BUDGET CHECK
WEIGHT_LIMIT_LB = 5.0   
total_mass = assembly["mass_lb"]
weight_margin = WEIGHT_LIMIT_LB - total_mass
weight_ok = total_mass <= WEIGHT_LIMIT_LB


#################### MAX LOAD FOR 9 GS
max_load_lb = assembly["mass_lb"] * 9.0

#################### Flight test data anamonly config 
df = pd.read_csv("flight_data.csv")

#################### ANOMALY THRESHOLDS
VIB_THRESHOLD  = 3.0    
GZ_THRESHOLD   = 2.5    
SPEED_DROP     = 20.0

# ROLLING MEAN FOR SPEED DROPOUT
df["airspeed_mean"] = df["airspeed_kts"].rolling(10, center=True).mean()
df["airspeed_drop"] = df["airspeed_kts"] < (df["airspeed_mean"] - SPEED_DROP)

# ANOMALIES
df["vib_anomaly"]   = df["vibration_in_s2"].abs() > VIB_THRESHOLD
df["gz_anomaly"]    = df["gz_g"] > GZ_THRESHOLD
df["any_anomaly"]   = df["vib_anomaly"] | df["gz_anomaly"] | df["airspeed_drop"]

# SUMMARY OF ANOMALIES
n_vib   = df["vib_anomaly"].sum()
n_gz    = df["gz_anomaly"].sum()
n_speed = df["airspeed_drop"].sum()
n_total = df["any_anomaly"].sum()


#################### DASHBOARD 4 TABLES

fig = plt.figure(figsize=(16, 10), facecolor="#0d1117")
fig.suptitle(
    "ASM-001 Aircraft Mount — Flight Test Analysis\n"
    "Carlos Bueno | April 2026",
    fontsize=14, fontweight="bold", color="white", y=0.98
)

gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.32,
                       left=0.07, right=0.97, top=0.91, bottom=0.07)

PANEL_BG   = "#161b22"
GRID_COLOR = "#30363d"
TEXT_COLOR = "#e6edf3"

def style_ax(ax, title):
    ax.set_facecolor(PANEL_BG)
    ax.tick_params(colors=TEXT_COLOR, labelsize=8)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5, linestyle="--")
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)

#################### PLOT 1 AIRSPEED, ALTITUDE
ax1 = fig.add_subplot(gs[0, 0])
style_ax(ax1, "Flight Profile — Altitude & Airspeed")
ax1.plot(df["time_s"], df["altitude_ft"], color="#58a6ff", lw=1.2, label="Altitude (ft)")
ax1b = ax1.twinx()
ax1b.plot(df["time_s"], df["airspeed_kts"], color="#3fb950", lw=1.2, label="Airspeed (kts)", alpha=0.85)
ax1b.tick_params(colors=TEXT_COLOR, labelsize=8)
ax1b.yaxis.label.set_color(TEXT_COLOR)
########MARKING SPEED DROPS
dropout_times = df[df["airspeed_drop"]]["time_s"]
ax1b.scatter(dropout_times, df[df["airspeed_drop"]]["airspeed_kts"],
             color="#f85149", s=18, zorder=5, label="Dropout")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Altitude (ft)", color="#58a6ff")
ax1b.set_ylabel("Airspeed (kts)", color="#3fb950")
########THIS IS FOR COMBINEING BOTH LEGENDS
lines1 = [plt.Line2D([0],[0], color="#58a6ff", lw=1.5),
          plt.Line2D([0],[0], color="#3fb950", lw=1.5),
          plt.Line2D([0],[0], marker='o', color="#f85149", ls='none', ms=5)]
ax1.legend(lines1, ["Altitude", "Airspeed", "Dropout"],
           facecolor=PANEL_BG, labelcolor=TEXT_COLOR, fontsize=7, loc="lower left")

#################### PLOT 2 MOUNT VIBRATION 
ax2 = fig.add_subplot(gs[0, 1])
style_ax(ax2, "Sensor Mount Vibration — Anomaly Detection")
ax2.plot(df["time_s"], df["vibration_in_s2"], color="#58a6ff", lw=0.8, alpha=0.7)
ax2.axhline(VIB_THRESHOLD,  color="#f85149", lw=1, ls="--", label=f"+{VIB_THRESHOLD} in/s² threshold")
ax2.axhline(-VIB_THRESHOLD, color="#f85149", lw=1, ls="--")
vib_events = df[df["vib_anomaly"]]
ax2.scatter(vib_events["time_s"], vib_events["vibration_in_s2"],
            color="#ff7b72", s=22, zorder=5, label=f"{n_vib} anomaly pts")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Vibration (in/s²)")
ax2.legend(facecolor=PANEL_BG, labelcolor=TEXT_COLOR, fontsize=7)

#################### PLOT 3 G'S PULLED
ax3 = fig.add_subplot(gs[1, 0])
style_ax(ax3, "Vertical Load Factor (Gz) — Structural Margin Check")
ax3.fill_between(df["time_s"], df["gz_g"], 1.0,
                 where=df["gz_g"] >= 1, color="#58a6ff", alpha=0.25)
ax3.plot(df["time_s"], df["gz_g"], color="#58a6ff", lw=0.9)
ax3.axhline(GZ_THRESHOLD, color="#f85149", lw=1.2, ls="--",
            label=f"Alert threshold ({GZ_THRESHOLD}g)")
ax3.axhline(9.0, color="#ff7b72", lw=1, ls=":",
            label="Limit (9G)")
gz_events = df[df["gz_anomaly"]]
ax3.scatter(gz_events["time_s"], gz_events["gz_g"],
            color="#ff7b72", s=25, zorder=5)
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Gs Pulled (G)")
ax3.legend(facecolor=PANEL_BG, labelcolor=TEXT_COLOR, fontsize=7)

#################### MASS PROPERTIES & CHECKS
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(PANEL_BG)
ax4.axis("off")
ax4.set_title("ASM-001 Mass Properties & Weight Budget", fontsize=10,
              fontweight="bold", color=TEXT_COLOR, pad=8)

def pass_fail_color(ok): return "#3fb950" if ok else "#f85149"

lines = [
    ("COMPONENT MASSES", "", "#8b949e"),
    (f"  Bracket",          f"{bracket['mass_lb']:.3f} lb",  TEXT_COLOR),
    (f"  Sensor Body",      f"{sensor['mass_lb']:.3f} lb",   TEXT_COLOR),
    (f"  Assembly Total",   f"{assembly['mass_lb']:.3f} lb", "#e3b341"),
    ("", "", TEXT_COLOR),
    ("WEIGHT BUDGET", "", "#8b949e"),
    (f"  Limit",            f"{WEIGHT_LIMIT_LB:.2f} lb",     TEXT_COLOR),
    (f"  Margin",           f"{weight_margin:.3f} lb",        pass_fail_color(weight_ok)),
    (f"  Status",           "PASS" if weight_ok else "FAIL",  pass_fail_color(weight_ok)),
    ("", "", TEXT_COLOR),
    ("ANOMALY SUMMARY", "", "#8b949e"),
    (f"  Vibration events", f"{n_vib}",   "#f85149" if n_vib  > 0 else "#3fb950"),
    (f"  High-G events",    f"{n_gz}",    "#f85149" if n_gz   > 0 else "#3fb950"),
    (f"  Airspeed dropouts",f"{n_speed}", "#f85149" if n_speed> 0 else "#3fb950"),
    (f"  Total Events",f"{n_total}", "#f85149" if n_total> 0 else "#3fb950"),

]

y = 0.97
for label, value, color in lines:
    if label == "" :
        y -= 0.025
        continue
    weight = "bold" if not label.startswith(" ") else "normal"
    ax4.text(0.02, y, label, transform=ax4.transAxes,
             fontsize=8, color=color, fontweight=weight, va="top", fontfamily="monospace")
    ax4.text(0.72, y, value, transform=ax4.transAxes,
             fontsize=8, color=color, fontweight=weight, va="top", fontfamily="monospace")
    y -= 0.04

plt.savefig("sensor_dashboard.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Dashboard saved at sensor_dashboard.png")
plt.close()
