# replicating-sutra-tensor-op-rnns-as-a-compilation-target - Work Queue

**This file is a queue of concrete, executable steps, not a state snapshot.**
Finished work lives in `devlog.md` (dated entries) and `git log`;
longer-horizon items live in `todo.md`. **When an item is done, delete it
from this file AND append a dated entry to `devlog.md` in the same commit,
then push.** No checkmarks, no status indicators in place.

**Why this file exists:** the replication plan is written here BEFORE
execution so an interrupted session resumes from the queue, not from chat.
The canonical methodology is `SKILL.md`; this queue is its executable form.

---

## Active — Replicate "Sutra: Tensor-Op RNNs as a Compilation Target for VSAs" (arXiv:2605.20919)

The headline empirical claims are all reproduced. Remaining tail:

1. **Confirm the GitHub Pages site is live.** The repo is public and pushed,
   `pages.yml` is wired up. The one-time manual step is **Settings → Pages →
   Source: GitHub Actions** — confirm that's set and the deploy job goes
   green. If the FINDINGS page renders, this step is done.

2. **Confirm the `package.yml` ZIP build is green.** Workflow dispatch (or a
   release) builds the downloadable replication package. Trigger once and
   verify the artifact downloads.

3. **(Optional) Retry §3.6 K=5 compiled training on a faster machine.**
   The codegen `translate_module` is super-polynomial in `!similarity` chain
   depth; on this machine k=4 codegen took 206 s and k=5 didn't complete in
   600 s. The substantive claim is replicated by §3.7 (same codegen path,
   K=3), so this is a nice-to-have, not a blocker for the headline.

---

## Pointers

- Methodology / definition of done: `SKILL.md`.
- Long-horizon items: `todo.md`.
- Completed work + replication milestones (chronological): `devlog.md`.
- Narrative history: `git log`.
