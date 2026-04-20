# ASM-001 Aircraft Research Sensor Mount
### Operations Flight Test Portfolio Project
**Author:** Carlos Bueno | **Date:** April 2026

---

## Project Overview

This project demonstrates an end-to-end aerospace engineering workflow for the design, analysis, and integration of a research sensor mount for aircraft flight tests directly aligned with NASA operations engineering requirements.

The project covers three engineering disciplines in one project:
- **CAD Design** — 3D bracket model and engineering drawing in Onshape
- **Risk Assessment** — Design FMEA following aerospace standards
- **Flight Data Analysis** — Python anomaly detection dashboard using real mass properties from the CAD model

---

## Repository Structure

```
Operations-Project/
│
├── cad/
│   ├── ASM-001_sensor_mount_drawing.pdf    # Design drawing
│   └── sensor_mount_assembly_render.png    # Onshape assembly screenshot
│
├── fmea/
│   └── ASM-001_Design_FMEA.xlsx            # Design FMEA
│
├── python/
│   ├── flight_data.py                      # Flight data generation
│   ├── sensor_analysis.py                  # Anlysis and dashboard
│   ├── flight_test_data.csv                # Generated flight data
│   ├── sensor_dashboard.png                # Output dashboard
│   └── requirements.txt                    # Python dependencies
│
└── README.md
```

---

## CAD Model — Onshape (ASM-001)

**Part:** Aircraft Research Sensor Mount
**Material:** 6061-T6 Aluminum
**Drawing Number:** ASM-001 | Rev 1.0 | April 2026

### Bracket Specifications

| Parameter | Value |
|---|---|
| Overall Height | 4.000 in |
| Base Length | 4.000 in |
| Base Depth | 3.000 in |
| Wall Thickness | 0.500 in |
| Sensor Bore Diameter | Ø2.000 in |
| Mounting Holes | 4x Ø0.250 THRU |
| Fillet Radius (inner) | 0.250 in |
| Material | 6061-T6 Aluminum |

### Mass Properties (from Onshape export)

| Component | Mass | Volume |
|---|---|---|
| Bracket only | 0.930 lb | 9.467 in³ |
| Air Data Sensor Body | 1.373 lb | 13.974 in³ |
| **Assembly Total** | **2.303 lb** | **23.441 in³** |

**Assembly Center of Gravity:**
- X: -0.256 in | Y: ≈0.000 in | Z: -1.174 in

### Design Decisions

- **4-bolt pattern** chosen over 3-bolt for load path redundancy — if one fastener loosens under vibration, 3 remaining fasteners maintain structural integrity
- **0.250 in inner fillet** at wall-to-base junction addresses the highest stress concentration point identified in the FMEA
- **2.000 in sensor bore** sized for a research instrumentation pod consistent with NASA AFRC instrument packages flown on research aircraft
- **6061-T6 aluminum** selected for optimal strength-to-weight ratio in aerospace structural applications

---

## Design FMEA

**File:** `FMEA/ASM-001_Design_FMEA.xlsx`

### Severity Scale (MIL-STD-1629A aligned)
| Score | Category | Definition |
|---|---|---|
| 9–10 | Catastrophic | May cause death or loss of aircraft |
| 7–8 | Critical | Mission loss or major system damage |
| 4–6 | Marginal | Mission degradation or minor damage |
| 1–3 | Minor | Unscheduled maintenance only |

### Detection Scale
| Score | Meaning |
|---|---|
| 1–2 | Almost certain to detect |
| 3–4 | High likelihood of detection |
| 5–6 | Moderate detection capability |
| 7–8 | Low detection capability |
| 9–10 | Cannot detect |

### Action Threshold
- **RPN ≥ 100** → Corrective action required
- **Severity ≥ 9** → Corrective action required regardless of RPN

### Top Risk Items

| Failure Mode | S | O | D | RPN | Action |
|---|---|---|---|---|---|
| Fatigue crack at inner fillet | 9 | 3 | 4 | **108** | YES |
| Fastener loosening under vibration | 7 | 4 | 3 | 84 | MONITOR |
| Galvanic corrosion at interface | 6 | 4 | 4 | 96 | MONITOR |
| Sensor ejection / FOD risk | 10 | 2 | 2 | 40 | YES (S=10) |

---

## Python Analysis — Flight Test Dashboard

**Files:** `python/generate_flight_data.py` + `python/sensor_mount_analysis.py`

### What the scripts do

**`generate_flight_data.py`**
Generates a 500-second synthetic flight test dataset modeling a research aircraft flight profile with:
- Physics-based altitude profile (climb at 3 ft/s → 300 ft cruise → descent at 2 ft/s)
- Airspeed ramp to 120 kts cruise with gaussian sensor noise (σ=1.5 kts)
- Three injected anomalies at known timestamps for detector validation:
  - Vibration spike at t=150s (turbulence simulation, peak 9.1 in/s²)
  - Airspeed dropout at t=280s (pitot sensor glitch, -40 kts)
  - Gz spike at t=420s (abrupt maneuver, peak ~4.8G)

**`sensor_mount_analysis.py`**
Loads real mass properties exported from the Onshape CAD model (ASM-001) and performs:

1. **Weight budget check** — verifies assembly mass against 5.0 lb instrument bay limit
2. **CG shift analysis** — calculates payload effect on aircraft center of gravity using the composite CG formula
3. **Structural margin check** — computes max load at 9G and compares against 4x 1/4-20 bolt shear capacity
4. **Anomaly detection** — flags vibration events, high-G maneuvers, and airspeed dropouts using threshold and rolling mean methods
5. **Dashboard generation** — outputs a 4-panel matplotlib engineering dashboard

### Dashboard Output

![Dashboard](Python/sensor_dashboard.png)

---

## Technologies Used

- **Onshape** — CAD modeling, assembly, engineering drawing
- **Python 3** — pandas, numpy, matplotlib
- **MIL-STD-1629A** — FMEA methodology
- **GitHub** — version control and portfolio hosting

---

## References

- MIL-STD-1629A — Procedures for Performing a Failure Mode, Effects, and Criticality Analysis (1980)
- NASA SP-2016-6119 — NASA Systems Engineering Handbook
- 6061-T6 Aluminum — ASM Aerospace Specification Metals
