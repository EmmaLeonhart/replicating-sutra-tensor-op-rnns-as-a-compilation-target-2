# Reproduction sources

The paper's §"Reproducibility" links two ready-to-run artifacts:

- Authors' code repo: <https://github.com/EmmaLeonhart/Sutra>
- Self-contained replication zip: <https://sutra.emmaleonhart.com/sutra-replication-package.zip>
  (ships `SKILL.md`, an agent-runnable recipe)

## What we used

We downloaded the **replication zip** (the self-contained artifact the
paper points to). It is now at `data_lake/sutra-replication-package.zip`
(gitignored) and extracted to `replication/sutra-replication-package/`
(committed). We copied its `SKILL.md` to repo root as `replication_skill.md`.

Package contents (top level):
- `SKILL.md` — agent-runnable recipe (the reproduction entry point)
- `REPRODUCE.md` — paper-section → command map
- `SYNTAX.md` — Sutra language reference
- `sdk/sutra-compiler/` — the compiler (pure Python, numpy-only build dep)
- `examples/` — 26 `.su` programs + 10-program smoke test
- `experiments/` — §3 reproduction scripts (and pre-shipped `*_results.json`)
- `sutraDB/` — Rust FFI sources for the embedded codebook (optional)

We did NOT separately clone `EmmaLeonhart/Sutra` as a submodule: the
zip is the self-contained artifact the paper says to use, and per its
README the GitHub repo is a fallback only. If we hit a bug that the
upstream has since fixed, we will revisit.

## Recipe coverage of headline claims

The bundled `SKILL.md` covers every empirical headline claim in the
paper end-to-end:

| Paper section | Recipe block | Reproduces |
|---|---|---|
| §3.1 capacity (3 LLM substrates) | `rotation_binding_capacity_llm.py` | rotation k=8 ≥95%, Hadamard collapse |
| §3.1 capacity (ESM-2 protein LM) | `rotation_binding_capacity_bioinformatics.py` | rotation k=8 ≥95%, Hadamard k=48 ≤10% |
| §3.1.1 crosstalk chain | `crosstalk_chain.py` | chain=1 → 100%, chain=8 → ≤5% |
| §3.6 differentiable training | `differentiable_training_compiled.py` | 18.7 ± 9.5 % → 100.0 ± 0.0 % |
| §3.7 trained-weight round-trip | `differentiable_training_weighted.py` | 33.3 ± 5.9 % → 100.0 ± 0.0 %, recompile ≈ 2e-7 / logit |
| §5 smoke test | `_smoke_test.py` + per-program checks | 10 programs decode their expected outputs |
| Compiler suite | `pytest sdk/sutra-compiler/tests/` | 237 passed / 7 skipped |

Optional (Docker-only): cross-paradigm `scallop_compare` — we will skip
this if the bare-metal sweep is sufficient for FINDINGS.

## Environment we have

- Python 3.13.3
- torch 2.10.0+cu128, transformers 5.4.0, torchhd 5.8.4, pytest 9.0.2
- ollama 0.17.1, with `nomic-embed-text`, `all-minilm`, `mxbai-embed-large`
  already pulled
- No CUDA usage required (the paper reports CPU torch on a laptop)
