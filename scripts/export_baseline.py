
from pathlib import Path
import traceback

from ansys.turbogrid.core.launcher.launcher import launch_turbogrid
from ansys.turbogrid.core.mesh_statistics import mesh_statistics

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "states" / "Baseline.tst"
OUTPUT = ROOT / "results" / "Baseline_stats.csv"

tg = None

try:
    if not STATE.is_file():
        raise FileNotFoundError(STATE)

    print("STEP 1: Launching TurboGrid...", flush=True)
    tg = launch_turbogrid(product_version="26.1.0")

    print("STEP 2: Reading state...", flush=True)
    tg.read_state(str(STATE))

    print("STEP 3: Generating mesh...", flush=True)
    tg.unsuspend(object="/TOPOLOGY SET")

    print("STEP 4: Reading mesh statistics...", flush=True)
    ms = mesh_statistics.MeshStatistics(tg)
    ms.update_mesh_statistics("ALL")

    stats = ms.get_mesh_statistics()

    if not stats:
        raise RuntimeError(
            "No mesh statistics available. "
            "Check mesh generation and geometry paths."
        )

    print(ms.get_table_as_text(), flush=True)

    print("STEP 5: Exporting CSV...", flush=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    ms.write_table_to_csv(str(OUTPUT))

    print(f"SUCCESS: {OUTPUT}", flush=True)

except Exception:
    print("ERROR OCCURRED:", flush=True)
    traceback.print_exc()

finally:
    if tg is not None:
        try:
            tg.quit()
        except Exception:
            pass
