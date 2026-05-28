# replicating-sutra-tensor-op-rnns-as-a-compilation-target — Devlog

**This file is where "done" lives.** `queue.md` is delete-only: when a queue
item is finished, the item is **deleted from `queue.md`** and a dated entry
is **appended here**, in the same commit as the work, then pushed. Never
tick a box in place — a checked box left in `queue.md` is the failure mode
this file exists to prevent.

Also record releases (tag + a one-line note), notable milestones, and
anything else worth a chronological trail. Newest entries at the bottom.

This is the **same convention as the cleanvibe repo's own `devlog.md`** —
every cleanvibe-scaffolded project gets one for the same reason.

See `CLAUDE.md` § "Workflow Rules" and `queue.md`'s preamble.

---

## 2026-05-28 — Project scaffolded

Scaffolded with `cleanvibe new` (cleanvibe v1.11.1). Future entries
land here as queue items get deleted.

## 2026-05-28 — Reproduction recipe acquired

Pulled the self-contained replication zip from
<https://sutra.emmaleonhart.com/sutra-replication-package.zip>
(715 KB) into `data_lake/` (gitignored), extracted to
`replication/sutra-replication-package/` (committed), and copied its
`SKILL.md` to repo root as `replication_skill.md`.

The recipe covers every headline empirical claim in the paper
(§3.1 LLM + ESM-2 capacity, §3.1.1 crosstalk, §3.6 differentiable
training, §3.7 weighted round-trip, §5 smoke test, compiler suite).
Coverage map and environment notes in `notes/sources.md`.

Environment check: Python 3.13.3, torch 2.10.0+cu128, transformers
5.4.0, torchhd 5.8.4, pytest 9.0.2, ollama 0.17.1 with all three
embedding models (`nomic-embed-text`, `all-minilm`, `mxbai-embed-large`)
already pulled. The compiler itself is pure-Python with only numpy as a
build dep. User has consented to running the third-party recipe.

## 2026-05-28 — Live on GitHub

Public repo created and pushed:
<https://github.com/EmmaLeonhart/replicating-sutra-tensor-op-rnns-as-a-compilation-target-2>.
From here every commit pushes and Actions runs as work happens.

## 2026-05-28 — All headline numbers reproduced

Ran the bundled `replication_skill.md` recipe end-to-end. Captured stdout
to `results/*.out`; updated `replication/sutra-replication-package/experiments/*_results.json`.

- **§3.1 capacity, four substrates.** All 16 paper-table numbers
  (rotation k=8 / k=48, Hadamard k=8 / k=48 across nomic-embed-text,
  all-minilm, mxbai-embed-large, ESM-2) reproduce to the displayed
  decimal place. The shipped LLM-capacity JSON had a mxbai OOM error;
  the regenerated JSON fills that gap.
- **§3.1.1 crosstalk chain.** All three substrates: chain=1 → 100% raw
  acc, chain=8 → 0% raw acc — matches the paper's "single-cycle records,
  chance by L=8" claim.
- **§3.7 weighted training + recompile round-trip.** before=33.33±5.89%
  → after=100.00±0.00%, w*=1.4339±0.0035, recompile Δlogit ≤ 2.1×10⁻⁷,
  `round_trip_ok=True` on every seed. Wall time 114.8 s. Matches the
  paper exactly.
- **§5 / Appendix I.** 10-program smoke test: all programs decode their
  hardcoded expected output. Final line: `PASS`.
- **§4 compiler suite.** 402 passed, 8 skipped (recipe text said 237/7;
  the package has grown).

**Divergence (documented in `FINDINGS.md`):** §3.6 compiled training at
K=5 did not complete. The compiler's `translate_module` pass is
super-polynomial in `!similarity` chain depth (k=3 codegen 22 s,
k=4 codegen 206 s, k=5 ≥ 600 s on this CPU). The substantive headline
("training reaches 100% by backprop through the emitted graph") is
verified by §3.7, which uses the *same* PyTorch codegen path at K=3 and
also adds the stronger recompile round-trip claim.

`FINDINGS.md` written. Repo pushed.
