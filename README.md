# Axial Compressor Rotor Modeling & Meshing

**Structured blade-passage meshing and geometric mesh-quality assessment using ANSYS BladeGen, TurboGrid, and Python.**

This educational project develops an axial compressor rotor blade geometry, generates a structured hexahedral mesh for one periodic blade passage, and compares five meshing configurations. The study focuses on mesh geometry and quality metrics; **no CFD flow solution or mesh-independence study is claimed**.

## 1. Project Overview

The workflow consists of four stages:

1. **Geometry modeling:** Define the meridional flow path, blade-angle distribution, and thickness distribution in ANSYS BladeGen.
2. **Mesh generation:** Transfer the blade geometry to ANSYS TurboGrid and generate a structured mesh for one blade passage using automatic topology and meshing (ATM).
3. **Quality assessment:** Evaluate the generated mesh using TurboGrid's mesh-quality statistics and configured limits.
4. **Parameter study and automation:** Change one meshing parameter at a time, regenerate the mesh, and export comparative statistics using PyTurboGrid.

### Software environment

| Software / tool | Version or role |
|---|---|
| ANSYS Workbench, BladeGen, TurboGrid | 2026 R1 Student |
| Python | 3.11 |
| PyTurboGrid (`ansys-turbogrid-core`) | 0.9.4 |
| Microsoft Excel | Comparison workbook |

## 2. Rotor Geometry

The initial BladeGen model uses the following **illustrative design parameters**:

| Parameter | Value |
|---|---:|
| Machine type | Axial compressor rotor |
| Number of rotor blades | 24 |
| Hub radius | 100 mm |
| Shroud radius | 150 mm |
| Blade span | 50 mm |
| Blade axial extent | 45 mm |
| Angular pitch | 15° |

The geometric model is intended for learning and mesh-generation assessment; its aerodynamic performance has not been validated.

![BladeGen rotor geometry](figures/rotor_3d.png)

*Figure 1. Rotor blade geometry created in ANSYS BladeGen.*

## 3. Structured Mesh Generation

TurboGrid was used to generate a structured hexahedral mesh for **one blade-to-blade flow passage**, including inlet, outlet, and blade-passage regions. The baseline mesh contains:

| Baseline mesh quantity | Count |
|---|---:|
| Nodes | 223,857 |
| Elements | 205,244 |

![Three-dimensional blade-passage mesh](figures/mesh_3d.png)

*Figure 2. Three-dimensional blade-passage mesh generated in TurboGrid.*

### Mesh sections

| Hub | Midspan | Tip |
|---|---|---|
| ![Hub mesh](figures/mesh_hub.png) | ![Midspan mesh](figures/mesh_midspan.png) | ![Tip mesh](figures/mesh_tip.png) |

*Figure 3. Blade-to-blade mesh sections near the hub, midspan, and tip.*

### Local mesh details

| Leading edge | Trailing edge |
|---|---|
| ![Leading-edge mesh](figures/mesh_le.png) | ![Trailing-edge mesh](figures/mesh_te.png) |

*Figure 4. Local mesh structures around the leading and trailing edges.*

## 4. Mesh Quality Assessment

Mesh quality was assessed for all domains using the following metrics: Orthogonality Angle, Minimum Face Angle, Maximum Face Angle, Edge Length Ratio, Element Volume Ratio, Minimum Volume, Connectivity Number, and Skewness.

Selected **baseline** values are listed below. Angles and volume are expressed in the units used for reporting here; the exported PyTurboGrid CSV files may display angles in radians and volume in cm³.

| Metric | Baseline value |
|---|---:|
| Orthogonality Angle | 37.9389° |
| Minimum Face Angle | 35.1806° |
| Maximum Face Angle | 144.737° |
| Maximum Edge Length Ratio | 200.302 |
| Maximum Element Volume Ratio | 4.50705 |
| Minimum Element Volume | 2.89777 × 10⁻¹³ m³ |
| Maximum Connectivity Number | 10 |
| Maximum Skewness | 0.609138 |

For the configured TurboGrid mesh-quality limits, all five configurations reported **0% Bad** in the exported statistics. The `% ok` category is an intermediate quality classification, distinct from `% Bad` and `% OK`. These classifications do not by themselves establish the accuracy of a CFD solution.

## 5. Meshing Parameter Study

Four configurations were compared with the baseline. **Each run changes one setting relative to the baseline**.

| Configuration | Spanwise-to-B2B count factor | Boundary-layer factor base | Target maximum expansion rate |
|---|---:|---:|---:|
| Baseline | 1.00 | 3.0 | 1.30 |
| Run 1 | 1.15 | 3.0 | 1.30 |
| Run 2 | 1.30 | 3.0 | 1.30 |
| Run 3 | 1.00 | 3.3 | 1.30 |
| Run 4 | 1.00 | 3.0 | 1.25 |

The first parameter corresponds to the ATM spanwise-to-blade-to-blade count factor in the saved TurboGrid states; it influences the spanwise mesh resolution. The other two parameters control boundary-layer refinement and the target rate of cell-size growth.

### Comparative results

The following data were exported from the five TurboGrid states:

| Configuration | Orthogonality `% ok` | Connectivity `% ok` | Max. Edge Length Ratio |
|---|---:|---:|---:|
| Baseline | 0.327441% | 0.044671% | 200.302 |
| Run 1 | 0.309938% | 0.045321% | 171.599 |
| Run 2 | **0.297913%** | 0.045833% | **137.487** |
| Run 3 | 0.305818% | **0.043440%** | 232.031 |
| Run 4 | 0.335912% | 0.045640% | 201.512 |

**Observations**

- **Run 2** produced the lowest proportion of elements in the intermediate orthogonality category and the lowest maximum Edge Length Ratio of the five cases. Relative to the baseline, these values decreased by approximately **9.0%** and **31.4%**, respectively.
- **Run 3** produced the lowest intermediate-category proportion for Connectivity Number, although its maximum Edge Length Ratio increased.
- **Run 4** did not improve the reported orthogonality or connectivity percentages relative to the baseline.

The comparison shows sensitivity to selected mesh-generation parameters, **not a universally optimal mesh**. Element counts and CFD-solution convergence would be needed to assess computational cost and numerical independence.

The complete exported data and comparison workbook are available in [`results/`](results/):

[Download mesh-quality comparison workbook](results/Axial_Compressor_Rotor_mesh_quality_comparison.xlsx)

## 6. Python Automation

PyTurboGrid automates loading the saved `.tst` configurations, triggering mesh generation, collecting mesh statistics, and exporting individual CSV files.

### Requirements

- ANSYS TurboGrid 2026 R1 installed locally, with a compatible license
- Python 3.11
- The Python dependency listed in [`requirements.txt`](requirements.txt)
- Access to the referenced blade geometry files

### Run the analysis

Clone or download this repository, then open a terminal **in the repository root**, where `requirements.txt` is located.

```powershell
python -m pip install -r requirements.txt
python scripts/export_stats.py
```

The script processes each `.tst` file in `states/` and writes a corresponding statistics CSV into `results/`.

**Reproducibility note:** Some TurboGrid state files retain absolute geometry paths from the original Windows workstation. On another machine or after moving the repository, the referenced `.curve` and `.inf` files may need to be relinked in TurboGrid before regenerating the meshes. These geometry-support files are included in [`states/`](states/). Successful execution on a different workstation has not yet been independently verified.

## 7. Repository Structure

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── Axial_Compressor_Rotor_technical_report.pdf
├── geometry/
│   └── BG.bgd
├── states/
│   ├── BG.inf
│   ├── BG_hub.curve
│   ├── BG_profile.curve
│   ├── BG_shroud.curve
│   ├── Baseline.tst
│   └── Run1–Run4 state files
├── scripts/
│   ├── export_baseline.py
│   └── export_stats.py
├── results/
│   ├── Baseline and Run1–Run4 statistics CSV files
│   └── Axial_Compressor_Rotor_mesh_quality_comparison.xlsx
└── figures/
    ├── rotor_3d.png
    ├── mesh_3d.png
    ├── mesh_hub.png
    ├── mesh_midspan.png
    ├── mesh_tip.png
    ├── mesh_le.png
    └── mesh_te.png
```

## 8. Limitations and Future Work

This project covers **geometry modeling, structured mesh generation, and geometric mesh-quality assessment only**. No CFX/Fluent simulation, compressor pressure-ratio calculation, efficiency prediction, or CFD mesh-independence verification has been performed.

Potential extensions include reporting element counts for every configuration, assessing near-wall resolution for a defined CFD operating condition, and performing a CFD-based grid-convergence study.

## 9. Technical Report

For a fuller description of the methods, mesh-quality statistics, comparative results, and limitations, see the accompanying technical report:

**[Download Technical Report (PDF)](Axial_Compressor_Rotor_technical_report.pdf)**
