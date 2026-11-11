
from pathlib import Path
import traceback

from ansys.turbogrid.core.launcher.launcher import launch_turbogrid
from ansys.turbogrid.core.mesh_statistics import mesh_statistics

ROOT = Path(__file__).resolve().parent
STATES = ROOT / "states"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

state_files = sorted(STATES.glob("*.tst"))

print(f"Found {len(state_files)} state files", flush=True)

for state_file in state_files:
    tg = None

    try:
        print(f"\nProcessing: {state_file.name}", flush=True)

        tg = launch_turbogrid(product_version="26.1.0")
        tg.read_state(str(state_file))

        # Generate the mesh
        tg.unsuspend(object="/TOPOLOGY SET")

        # Read mesh statistics
        ms = mesh_statistics.MeshStatistics(tg)
        ms.update_mesh_statistics("ALL")

        stats = ms.get_mesh_statistics()

        if not stats or "Orthogonality Angle" not in stats:
            raise RuntimeError("Mesh statistics are unavailable")

        # Export CSV
        output = RESULTS / f"{state_file.stem}_stats.csv"
        ms.write_table_to_csv(str(output))

        print(f"SUCCESS: {output}", flush=True)

    except Exception:
        print(f"FAILED: {state_file.name}", flush=True)
        traceback.print_exc()

    finally:
        if tg is not None:
            try:
                tg.quit()
            except Exception:
                pass

print("\nAll available states processed.")
