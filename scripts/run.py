"""CI entry point: re-run the reproduction recipe end-to-end.

This is a thin Python driver around the authors' shipped
``replication/sutra-replication-package/SKILL.md`` recipe. Each step
shells out to one of the recipe's commands and captures its output to
``results/<step>.out``; the final results JSON files emitted by the
authors' experiment scripts are read back to extract the numbers that
``FINDINGS.md`` reports.

The runtime is dominated by ``differentiable_training_compiled.py``
(~230 s on CPU) — the whole sweep is laptop-CPU scale (well under one
GPU-hour), which is why ``paper.json`` marks this replication
CI-runnable.

Skipped here: the Docker-only ``scallop_compare`` block from the recipe
(needs a 10–15 min Rust-nightly + scallopy + DeepProbLog image build);
it is optional in the paper.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PKG = REPO / "replication" / "sutra-replication-package"
RESULTS = REPO / "results"
RESULTS.mkdir(exist_ok=True)


def run(label: str, cmd: list[str], *, env_extra: dict[str, str] | None = None) -> int:
    """Run a recipe step from inside the package directory, tee to results/."""
    print(f"\n=== {label} ===", flush=True)
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    out_path = RESULTS / f"{label}.out"
    t0 = time.time()
    with out_path.open("w", encoding="utf-8") as fh:
        proc = subprocess.run(
            cmd,
            cwd=PKG,
            env=env,
            stdout=fh,
            stderr=subprocess.STDOUT,
            text=True,
        )
    dt = time.time() - t0
    print(f"    rc={proc.returncode}  {dt:.1f}s  -> {out_path}", flush=True)
    return proc.returncode


def main() -> int:
    # Smoke test (10-program corpus).
    rc = run("smoke_test", [sys.executable, "examples/_smoke_test.py"])
    if rc != 0:
        return rc

    # Compiler unit suite (excluding optional egglog).
    rc = run(
        "pytest_compiler",
        [
            sys.executable, "-m", "pytest",
            "sdk/sutra-compiler/tests/", "-q",
            "--ignore=sdk/sutra-compiler/tests/test_simplify_egglog.py",
        ],
    )
    if rc != 0:
        return rc

    # §3.1 capacity sweep, three LLM substrates.
    rc = run(
        "capacity_llm",
        [sys.executable, "experiments/rotation_binding_capacity_llm.py"],
    )
    if rc != 0:
        return rc

    # §3.1 capacity sweep, ESM-2 protein LM.
    rc = run(
        "capacity_esm2",
        [sys.executable, "experiments/rotation_binding_capacity_bioinformatics.py"],
    )
    if rc != 0:
        return rc

    # §3.1.1 crosstalk chain.
    rc = run(
        "crosstalk_chain",
        [sys.executable, "experiments/crosstalk_chain.py"],
    )
    if rc != 0:
        return rc

    # §3.6 differentiable training (compiled, batched).
    rc = run(
        "diff36_compiled",
        [
            sys.executable, "experiments/differentiable_training_compiled.py",
            "--k", "5", "--per-class", "10",
            "--epochs", "30", "--seeds", "0,1,2",
            "--lr", "0.01", "--batched",
        ],
    )
    if rc != 0:
        return rc

    # §3.7 trained-weight round-trip.
    rc = run(
        "diff37_weighted",
        [
            sys.executable, "experiments/differentiable_training_weighted.py",
            "--k", "3", "--per-class", "8",
            "--epochs", "30", "--seeds", "0,1",
        ],
    )
    if rc != 0:
        return rc

    # Pull the JSON results the experiment scripts wrote, mirror them
    # under results/ so the deliverables jobs (Pages, package zip) can
    # find everything in one place.
    json_artifacts = [
        "experiments/rotation_binding_capacity_llm_results.json",
        "experiments/rotation_binding_capacity_bioinformatics_results.json",
        "experiments/crosstalk_chain_results.json",
        "experiments/differentiable_training_multiseed_results.json",
    ]
    summary: dict[str, object] = {}
    for rel in json_artifacts:
        src = PKG / rel
        if src.exists():
            data = json.loads(src.read_text(encoding="utf-8"))
            (RESULTS / Path(rel).name).write_text(
                json.dumps(data, indent=2), encoding="utf-8"
            )
            summary[Path(rel).stem] = "ok"
        else:
            summary[Path(rel).stem] = "missing"
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print("\nAll recipe steps passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
