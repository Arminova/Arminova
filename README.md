# Hi, I'm Armin

I build and tune local AI: inference engines, model recipes and dev tools, so large models run fast on hardware you
own. Current focus: NVIDIA DGX Spark (GB10).

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-armin1-FFD21E?logo=huggingface&logoColor=000)](https://huggingface.co/armin1)
[![X](https://img.shields.io/badge/X-@arminxnova-000000?logo=x&logoColor=fff)](https://x.com/arminxnova)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-arminh-FF5E5B?logo=kofi&logoColor=fff)](https://ko-fi.com/arminh)

<!-- impact:start -->
<picture>
  <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/impact-mobile-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/impact-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">
  <img alt="What my TensorFold pull requests changed. Qwen3.8-Flash-Next: #1368 2.4× faster server start; #1763 +2 % one-stream decode; #1764 +4–5 % faster cold prompts; #1786 +11.5 % one-stream decode, up to; #2160 +5–6 % 8-stream decode, MLX 4-bit; #1942 +3–6 % 8-stream decode. LFM2.5-24B-A2B: #1590 A 2,048-row prompt chunk 243 s to 3.9 s; #1590 First token of a cold 930-token prompt 212 s to 2.0 s" src="assets/impact-light.svg">
</picture>
<!-- impact:end -->

<!-- stats:start -->
**TensorFold** (upstream: [ashhart/TensorFold](https://github.com/ashhart/TensorFold)): **6** [pull requests merged](https://github.com/ashhart/TensorFold/pulls?q=is%3Apr+is%3Amerged+author%3AArminova) · **4,155** lines added · **9** [commits on main](https://github.com/ashhart/TensorFold/commits/main/?author=Arminova)

<sub>Counted from GitHub by [tools/refresh.py](tools/refresh.py). Pull requests: those GitHub shows as merged. Lines added: the sum of those pull requests' additions. Commits: authored by me on TensorFold's main branch; that includes #1368 and #268, which landed as my commits while GitHub shows their pull requests closed.</sub>
<!-- stats:end -->

<!-- gains:start -->
## What my pull requests changed, model by model

For each model, the best figure the maintainer or I measured in each category, from a single pull request. Every figure says who measured it and links its source. Different pull requests are separate before/after runs and do not add up to one total. Every pull request's own numbers are in the [details](TENSORFOLD.md).

| Model | Server start | One-stream decode | Many-stream decode | Prompt speed |
|---|---|---|---|---|
| **Qwen3.8-Flash-Next**<br><sub>CUDA engine, one GB10 (the chip in the NVIDIA DGX Spark)</sub> | **2.4× faster†**<br><sub>about 200 s → about 83 s · [#1368, maintainer's A/B](https://github.com/ashhart/TensorFold/pull/1368#issuecomment-6450647092)</sub> | **up to +11.5 %**<br><sub>the maintainer's best case · [#1786, maintainer's A/B](https://github.com/ashhart/TensorFold/pull/1786#issuecomment-6622991893)</sub> | **+6.4 %**<br><sub>code, 8 greedy streams, MLX 4-bit · [#2160, maintainer's A/B](https://github.com/ashhart/TensorFold/pull/2160#issuecomment-6646355107)</sub> | **+5.2 %**<br><sub>cold 16,384-token prompt · [#1764, maintainer's A/B](https://github.com/ashhart/TensorFold/pull/1764#issuecomment-6581126349)</sub> |
| **LFM2.5-24B-A2B**<br><sub>Metal engine, Apple M1 and M2 Macs (measured on an M1 Pro)</sub> | — | — | **11–17 tok/s → 116–123 tok/s**<br><sub>16 greedy streams together · [#1590, own receipt](https://github.com/ashhart/TensorFold/pull/1590)</sub> | **106× faster†**<br><sub>first token of a cold 930-token prompt, 212 → 2.0 s · [#1590, own receipt](https://github.com/ashhart/TensorFold/pull/1590)</sub> |

† computed from the two stated figures; every other percentage is as the source states it.
<!-- gains:end -->

## Recipes for one DGX Spark

| Recipe | What it is |
|---|---|
| [Nemotron-3.5-Super-VL abliterated](https://github.com/Arminova/Nemotron-3.5-Super-VL-Abliterated-Single-DGX-Spark) | NVIDIA's 120B vision-language model, uncensored, on TensorFold or vLLM; refusals from 98 % to 2 %, tasks and speed unchanged |
| [Qwen3.8-Flash-Next](https://github.com/Arminova/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold) | 262,144-token windows, three streams, NVIDIA's public FP4-Local checkpoint |
| [DeepSeek-V4-Flash](https://github.com/Arminova/DeepSeek-V4-Flash-Single-DGX-Spark-TensorFold) | Engine patches and a Docker image for the 0731 model on a single Spark |

## Models on Hugging Face

| Model | What it is |
|---|---|
| [Nemotron-3.5-Super-VL-120B-A12B-NVFP4-abliterated](https://huggingface.co/armin1/Nemotron-3.5-Super-VL-120B-A12B-NVFP4-abliterated) | The uncensored build behind the recipe above, in NVIDIA's own tensor formats |
| [Qwen3.8-27B-NVFP4-FP8-Mixed-LH](https://huggingface.co/armin1/Qwen3.8-27B-NVFP4-FP8-Mixed-LH) | A mixed NVFP4 / FP8 quantization for single-GPU Blackwell machines, SGLang and DFlash ready ([uncensored variant](https://huggingface.co/armin1/Qwen3.8-27B-NVFP4-FP8-Mixed-LH-Heretic)) |

## Contributions to [TensorFold](https://github.com/ashhart/TensorFold)

<!-- prs:start -->
All of them, open ones included: [my TensorFold pull requests](https://github.com/ashhart/TensorFold/pulls?q=author%3AArminova).
<!-- prs:end -->

More projects and tools will appear here as I open-source them.

🤗 [Hugging Face](https://huggingface.co/armin1) · [X](https://x.com/arminxnova) · [Ko-fi](https://ko-fi.com/arminh)
