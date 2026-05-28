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
