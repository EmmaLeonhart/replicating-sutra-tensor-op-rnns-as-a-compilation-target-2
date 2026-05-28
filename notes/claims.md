# Headline claims (scoped to what the shipped recipe needs the reader to verify)

The paper's headline is a single dual claim about Sutra:

> The same `.su` program is both a logic program (decodes bundles to
> 100% through k=8 across four frozen embedding substrates) **and** a
> trainable neural network (backprop through the *compiled* graph trains
> a fuzzy-rule classifier from chance to 100%; the trained scalar gain
> rewrites the source as a numeric literal and recompiles bit-for-bit).

## Headline numbers we are checking

| §        | Claim                                              | Paper value(s)                                                       |
|----------|----------------------------------------------------|----------------------------------------------------------------------|
| 3.1      | Rotation k=8 binding accuracy across substrates    | 100.0% on all four (nomic, all-minilm, mxbai, ESM-2)                 |
| 3.1      | Hadamard k=8 collapse                              | mxbai 2.5%, all-minilm 7.5%, ESM-2 28.7%, nomic 87.5%                |
| 3.1      | Rotation k=48                                      | nomic 93.3%, all-minilm 42.3%, mxbai 72.1%, ESM-2 44.2%              |
| 3.1.1    | Crosstalk chain length=1 accuracy                  | 100% on every substrate (single-cycle records)                       |
| 3.1.1    | Crosstalk chain length=8 accuracy                  | ≤5% (falls to chance)                                                |
| 3.6      | Compiled-graph differentiable training (K=5)       | 18.7 ± 9.5 % → 100.0 ± 0.0 %, 3 seeds, ~230 s                        |
| 3.7      | Weighted variant + recompile round-trip (K=3)      | 33.3 ± 5.9 % → 100.0 ± 0.0 %, w*=1.43±0.004, Δlogit ≈ 2×10⁻⁷         |
| 5/Smoke  | 10-program demonstration corpus                    | All 10 programs decode their expected output                         |
| §4 suite | Compiler unit tests                                | 237 passed, 7 skipped (per recipe; package now ships 402 / 8)        |

## Datasets / models / scripts

The recipe ships everything:

- 200-word semantic codebook hard-coded in `experiments/rotation_binding_capacity_llm.py`
- 84-protein sequence list hard-coded in `experiments/rotation_binding_capacity_bioinformatics.py`
- Embedding models pulled at setup time:
  - `nomic-embed-text` (768-d) via Ollama
  - `all-minilm` (384-d) via Ollama
  - `mxbai-embed-large` (1024-d) via Ollama
  - `facebook/esm2_t6_8M_UR50D` (320-d) via HuggingFace (auto-downloads, ~30 MB)
- Categorized 5-class / 20-class word lists in `experiments/differentiable_training.py`
  (reused by §3.6 / §3.7 compiled-graph scripts)

## Compute envelope

Paper reports CPU torch on a single laptop, ≈230 s for §3.6, ≈2.5 min for §3.7,
≈2 min/substrate for capacity, ≈5 min for crosstalk. Total ≤ 20 min, no GPU
required — comfortably CI-runnable.

## References — sanity check

The bibliography names well-known canonical work in each cited area:
Adam (Kingma & Ba 2015), ESM-2 (Lin et al. 2023 Science), HRR (Plate 1995),
tensor product binding (Smolensky 1990), hyperdimensional computing
(Kanerva 2009), Torchhd (Heddes et al. 2023, JMLR), Scallop (Li et al. 2023,
PLDI), DeepProbLog (Manhaeve et al. 2018, NeurIPS), embedding anisotropy
(Ethayarajh 2019, EMNLP), three-valued logic (Kleene 1952). No suspect or
fabricated references were spotted.
