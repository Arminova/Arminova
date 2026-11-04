# Armin

I make large language models run fast on one NVIDIA DGX Spark (GB10), mostly in
[TensorFold](https://github.com/ashhart/TensorFold)'s native engine. Every change keeps replies token-equal to the
engine before it.

## Merged into TensorFold

Results as TensorFold's changelog states them:

| Pull request | What | Result |
|---|---|---|
| [#1786](https://github.com/ashhart/TensorFold/pull/1786) | Flash Next on CUDA: drafted rounds | one-stream decode on a GB10 up to 11.5 % faster (chat +8.7 %, code +6.3 %) |
| [#1764](https://github.com/ashhart/TensorFold/pull/1764) | Flash Next on CUDA: prompt passes with the same bits and less work | cold prompts about 4 to 5 % faster on a GB10 |
| [#1763](https://github.com/ashhart/TensorFold/pull/1763) | Flash Next on CUDA: decode with several streams | pending DeltaNet rows, reused lane buffers, the shared expert on a side stream |
| [#1368](https://github.com/ashhart/TensorFold/pull/1368) | Flash Next on CUDA: NVFP4 experts loaded on several threads | a server starts in about 83 s instead of about 200 s |
| [#1590](https://github.com/ashhart/TensorFold/pull/1590) | Prompt tiles on M1 and M2 Macs | a 2,048-row prompt chunk in 3.9 s instead of 243 s on an M1 Pro |

Open and in review: [my TensorFold pull requests](https://github.com/ashhart/TensorFold/pulls?q=author%3AArminova).

## Recipes for one DGX Spark

- [Qwen3.8-Flash-Next](https://github.com/Arminova/Qwen3.8-Flash-Next-Single-DGX-Spark-TensorFold): 262,144-token
  windows, three streams, on NVIDIA's public FP4-Local checkpoint.
- [DeepSeek-V4-Flash](https://github.com/Arminova/DeepSeek-V4-Flash-Single-DGX-Spark-TensorFold): the 0731 model on
  one Spark with TensorFold.
