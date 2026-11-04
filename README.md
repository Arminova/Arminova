# Hi, I'm Armin

I build and tune local AI: inference engines, model recipes and dev tools, so large models run fast on hardware you
own. Current focus: NVIDIA DGX Spark (GB10).

[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-armin1-FFD21E?logo=huggingface&logoColor=000)](https://huggingface.co/armin1)
[![X](https://img.shields.io/badge/X-@arminxnova-000000?logo=x&logoColor=fff)](https://x.com/arminxnova)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-arminh-FF5E5B?logo=kofi&logoColor=fff)](https://ko-fi.com/arminh)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/impact-dark.svg">
  <img alt="What my TensorFold pull requests changed: Flash Next server start 200 s to 83 s, one-stream decode up to 11.5 % faster, cold prompts 4 to 5 % faster; M1 prompt tiles 62 times faster" src="assets/impact-light.svg">
</picture>

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

| Pull request | What it does |
|---|---|
| [#1786](https://github.com/ashhart/TensorFold/pull/1786) | Flash Next on CUDA: drafted rounds send the first token earlier and draft deeper |
| [#1764](https://github.com/ashhart/TensorFold/pull/1764) | Flash Next on CUDA: prompt passes do less work |
| [#1763](https://github.com/ashhart/TensorFold/pull/1763) | Flash Next on CUDA: less repeated work when several streams decode |
| [#1368](https://github.com/ashhart/TensorFold/pull/1368) | Flash Next on CUDA: experts load on several threads |
| [#1590](https://github.com/ashhart/TensorFold/pull/1590) | Prompt tiles on M1 and M2 Macs |

All of them, open ones included: [my TensorFold pull requests](https://github.com/ashhart/TensorFold/pulls?q=author%3AArminova).

More projects and tools will appear here as I open-source them.

🤗 [Hugging Face](https://huggingface.co/armin1) · [X](https://x.com/arminxnova) · [Ko-fi](https://ko-fi.com/arminh)
