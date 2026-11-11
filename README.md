
# Axial Compressor Rotor Modeling & Meshing

## 1. Overview

This project focuses on the geometric modeling and structured mesh generation of an axial compressor rotor using ANSYS BladeGen and TurboGrid.

A single blade passage is modeled and meshed. Five mesh configurations are evaluated to investigate the effects of meshing parameters on geometric mesh-quality metrics.

## 2. Software and Tools

- ANSYS Workbench 2026 R1 Student
- ANSYS BladeGen
- ANSYS TurboGrid
- Python and PyTurboGrid
- Microsoft Excel

## 3. Rotor Geometry

The initial rotor model was created in BladeGen using the following parameters:

| Parameter | Value |
|---|---:|
| Rotor blades | 24 |
| Hub radius | 100 mm |
| Shroud radius | 150 mm |
| Blade span | 50 mm |
| Blade axial extent | 45 mm |

![Rotor Geometry](figures/rotor_3d.png)

## 4. Structured Mesh Generation

A structured hexahedral mesh was generated for a single blade passage using TurboGrid.

The baseline mesh contains:

- 223,857 nodes
- 205,244 elements

![3D Blade Passage Mesh](figures/mesh_3d.png)

### Hub

![Hub Mesh](figures/mesh_hub.png)

### Midspan

![Midspan Mesh](figures/mesh_midspan.png)

### Tip

![Tip Mesh](figures/mesh_tip.png)

### Leading Edge

![Leading Edge Mesh](figures/mesh_le.png)

### Trailing Edge

![Trailing Edge Mesh](figures/mesh_te.png)

## 5. Mesh Quality Assessment

The mesh was evaluated using the following geometric quality metrics:

- Orthogonality Angle
- Minimum and Maximum Face Angle
- Edge Length Ratio
- Element Volume Ratio
- Minimum Volume
- Connectivity Number
- Skewness

All five configurations reported 0% Bad elements according to the configured TurboGrid mesh-quality limits.

## 6. Mesh Quality Comparison

Five mesh configurations were analyzed.

| Configuration | Orthogonality (% ok) | Connectivity (% ok) | Max. Edge Length Ratio |
|---|---:|---:|---:|
| Baseline | 0.327441 | 0.044671 | 200.302 |
| Run 1 | 0.309938 | 0.045321 | 171.599 |
| Run 2 | 0.297913 | 0.045833 | 137.487 |
| Run 3 | 0.305818 | 0.043440 | 232.031 |
| Run 4 | 0.335912 | 0.045640 | 201.512 |

Run 2 produced the lowest proportion of elements in the intermediate orthogonality category and the lowest maximum Edge Length Ratio.

Run 3 produced the lowest intermediate-category proportion for Connectivity Number, but increased the maximum Edge Length Ratio.

These results represent geometric mesh-quality comparisons, not a CFD mesh-independence study.

## 7. Python Automation

PyTurboGrid was used to automate mesh generation and statistical data extraction.

Workflow:

1. Load a TurboGrid state file.
2. Generate the mesh.
3. Extract mesh statistics.
4. Export the results to CSV.
5. Compare the results across mesh configurations.

The scripts are located in `scripts/`, and the exported CSV files are stored in `results/`.

### Reproducing the Mesh Statistics

#### Requirements

- ANSYS TurboGrid 2026 R1
- Python 3.11
- PyTurboGrid
- A compatible ANSYS license

#### Installation

Clone or download this repository and open a terminal in the project root directory.

Install the required Python package:

```powershell
python -m pip install -r requirements.txt
```

#### Running the Analysis

Run the mesh statistics extraction script:

```powershell
python scripts/export_stats.py
```

The script automatically:

1. Loads all TurboGrid `.tst` state files from `states/`.
2. Generates the mesh for each configuration.
3. Extracts mesh quality statistics.
4. Exports the results as CSV files to `results/`.

#### Notes

- ANSYS TurboGrid must be installed locally.
- Geometry references may need to be relinked when running on another computer.
- The exported data can be compared using the Excel workbook in `results/`.
```

## 8. Repository Structure

- `geometry/`: BladeGen geometry
- `states/`: TurboGrid state files
- `scripts/`: Python automation scripts
- `results/`: Mesh statistics and comparison workbook
- `figures/`: Geometry and mesh visualization

## 9. Limitations

The study focuses on geometric mesh quality and meshing parameter sensitivity.

No CFD flow solution, aerodynamic performance evaluation, or mesh-independence verification has been performed.
