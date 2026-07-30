<h1 align="center">João Felipe de Souza</h1>

<p align="center">
  <b>ML Systems Engineer focused on LLM inference runtime, GPU kernels, and serving infrastructure.</b>
</p>

<p align="center">
  <a href="https://github.com/JohnScheuer">
    <img src="https://img.shields.io/badge/GitHub-JohnScheuer-181717?style=for-the-badge&logo=github" />
  </a>
  <a href="https://linkedin.com/in/joaofelipescheuer">
    <img src="https://img.shields.io/badge/LinkedIn-João%20Felipe%20de%20Souza-0A66C2?style=for-the-badge&logo=linkedin" />
  </a>
  <a href="mailto:johnfelipe13@gmail.com">
    <img src="https://img.shields.io/badge/Email-johnfelipe13%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/WeChat-JohnScheuer7-07C160?style=for-the-badge&logo=wechat&logoColor=white" />
  <img src="https://img.shields.io/badge/Phone-%2B55%2041%2099705--4864-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/CUDA-GPU%20Kernel%20Engineering-76B900?style=flat-square&logo=nvidia&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-Inference%20Runtime-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Serving-Continuous%20Batching-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/Distributed-TP%20%7C%20PP%20%7C%20KV%20Sharding-purple?style=flat-square" />
  <img src="https://img.shields.io/badge/Open%20to-Relocation%20Worldwide-success?style=flat-square" />
</p>

---

## About

I build systems around **large language model inference**:

- custom **CUDA kernels** and **PTX intrinsics**
- **C++/CUDA inference runtimes**
- **serving stacks** and scheduling systems
- **compiler/codegen** experiments for Transformer workloads
- **distributed inference** (TP / PP / KV sharding)
- **quantization** and compression analysis
- **retrieval-augmented** inference pipelines
- **LLM-as-a-Service** backends with billing and rate limiting

My work sits at the boundary between **ML systems**, **GPU performance engineering**, and **runtime infrastructure**.

Currently based in Brazil. Open to relocation worldwide.

---

## Start Here

If you are visiting for the first time, these are the best entry points:

| Project | Area | Key Result |
|---|---|---|
| [mini-llm-inference-engine](https://github.com/JohnScheuer/mini-llm-inference-engine) | C++/CUDA Runtime | 32.4k tok/s, 87% INT8 Tensor Core ceiling |
| [sm75-tensorcore-microkernel](https://github.com/JohnScheuer/sm75-tensorcore-microkernel) | PTX / GEMM | Instruction-level Tensor Core micro-kernel engineering |
| [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75) | INT4 Kernel + E2E LLM | PTX MMA + Qwen2 integration, 14.7% VRAM reduction |
| [llm-fusion-compiler](https://github.com/JohnScheuer/llm-fusion-compiler) | Compiler / Codegen | 10.5 TFLOPS peak on RTX 2070 |
| [custom-llm-serving-engine](https://github.com/JohnScheuer/custom-llm-serving-engine) | Serving Runtime | OpenAI-compatible API, batching, KV cache, metrics |
| [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine) | Distributed Inference | Megatron-style TP, GPipe PP, KV sharding |
| [llm-gateway-saas](https://github.com/JohnScheuer/llm-gateway-saas) | Production Backend | LLM-as-a-Service with billing, tool calling, rate limiting |

---

## Featured Metrics

<p>
  <img src="https://img.shields.io/badge/Custom%20LLM%20Engine-32.4k%20tok%2Fs-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/INT8%20Tensor%20Core-87%25%20of%20ceiling-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/Compiler%20Codegen-10.5%20TFLOPS-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/Comm%20Cost%20Model-R%C2%B2%20%3D%200.9996-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/Speculative%20Decoding-1.41x%20speedup-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/AWQ%204--bit-26.05%20PPL-1f6feb?style=flat-square" />
  <img src="https://img.shields.io/badge/INT4%20E2E%20Qwen2-14.7%25%20VRAM%20cut-1f6feb?style=flat-square" />
</p>

---

## Flagship Implementations

### GPU Kernels and Low-Level Performance
- [mini-llm-inference-engine](https://github.com/JohnScheuer/mini-llm-inference-engine)  
  Transformer inference engine in **C++/CUDA**, without a PyTorch execution path.

- [sm75-tensorcore-microkernel](https://github.com/JohnScheuer/sm75-tensorcore-microkernel)  
  **PTX-level** Tensor Core GEMM programming for NVIDIA Turing (SM75).

- [flash-attention-sm75](https://github.com/JohnScheuer/flash-attention-sm75)  
  FlashAttention v1 forward pass for SM75.

- [flash-attention-sm75-register-fused](https://github.com/JohnScheuer/flash-attention-sm75-register-fused)  
  Register-fused FlashAttention study with persistent accumulators.

- [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75)  
  PTX INT4 GEMM kernel with end-to-end Qwen2 integration and 14.7% VRAM reduction.

- [fused-backward-kernels-sm75](https://github.com/JohnScheuer/fused-backward-kernels-sm75)  
  Fused GEMM + Bias + GeLU backward CUDA kernels.

### Compiler / Codegen
- [llm-fusion-compiler](https://github.com/JohnScheuer/llm-fusion-compiler)  
  Compiler MVP: **IR → CUDA codegen → nvcc → GPU execution**.

### Serving and Runtime Systems
- [custom-llm-serving-engine](https://github.com/JohnScheuer/custom-llm-serving-engine)  
  Production-oriented inference server with batching, SSE streaming, KV cache management, and Prometheus metrics.

- [llm-gateway-saas](https://github.com/JohnScheuer/llm-gateway-saas)  
  Complete LLM-as-a-Service backend with billing, tool calling, distributed rate limiting, and financial audit trail.

- [speculative-decoding-runtime](https://github.com/JohnScheuer/speculative-decoding-runtime)  
  Speculative decoding with rejection sampling and adaptive gamma.

- [lora-inference-runtime](https://github.com/JohnScheuer/lora-inference-runtime)  
  Multi-LoRA serving runtime with low-latency adapter hot-swapping.

- [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine)  
  Simulated multi-GPU runtime implementing **Tensor Parallelism**, **Pipeline Parallelism**, and **KV cache sharding**.

### Quantization and Compression
- [quantization-runtime](https://github.com/JohnScheuer/quantization-runtime)  
  From-scratch **AWQ** and **GPTQ** implementation and stability analysis.

### Retrieval and Multimodal
- [rag-inference-stack](https://github.com/JohnScheuer/rag-inference-stack)  
  Local-first RAG pipeline with ingestion, embeddings, vector retrieval, and answer generation.

- [vlm-inference-runtime](https://github.com/JohnScheuer/vlm-inference-runtime)  
  Deployment-oriented VLM serving wrapper for Qwen2-VL.

---

## By Project Type

### From-Scratch Implementations
Core logic implemented directly rather than wrapped around an existing system:

- `mini-llm-inference-engine`
- `sm75-tensorcore-microkernel`
- `flash-attention-sm75`
- `flash-attention-sm75-register-fused`
- `fused-int4-gemm-sm75`
- `fused-backward-kernels-sm75`
- `llm-fusion-compiler`
- `custom-llm-serving-engine`
- `distributed-inference-engine`
- `quantization-runtime`
- `speculative-decoding-runtime`
- `llm-gateway-saas`

### Analytical / Simulation Studies
Systems tradeoff analysis, modeling, and operational benchmarking:

- [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim)
- [comm-cost-modeling](https://github.com/JohnScheuer/comm-cost-modeling)
- [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator)
- [hardware-aware-llm-runtime](https://github.com/JohnScheuer/hardware-aware-llm-runtime)
- [capacity-planning-sim](https://github.com/JohnScheuer/capacity-planning-sim)
- [continuous-batching-fragmentation-sim](https://github.com/JohnScheuer/continuous-batching-fragmentation-sim)
- [paged-attention-sim](https://github.com/JohnScheuer/paged-attention-sim)

### Integration / Deployment Wrappers
These are intentionally framed as integration/deployment systems, not custom low-level runtimes:

- `rag-inference-stack`
- `vlm-inference-runtime`

---

## Recent Inference Systems Series

A recent 6-project series covering major components of the inference stack:

| Project | Focus |
|---|---|
| [distributed-inference-engine](https://github.com/JohnScheuer/distributed-inference-engine) | Parallelism and scaling |
| [quantization-runtime](https://github.com/JohnScheuer/quantization-runtime) | 4-bit AWQ/GPTQ analysis |
| [fused-int4-gemm-sm75](https://github.com/JohnScheuer/fused-int4-gemm-sm75) | INT4 kernel + Qwen2 E2E integration |
| [rag-inference-stack](https://github.com/JohnScheuer/rag-inference-stack) | Retrieval-augmented serving |
| [lora-inference-runtime](https://github.com/JohnScheuer/lora-inference-runtime) | Multi-adapter serving |
| [speculative-decoding-runtime](https://github.com/JohnScheuer/speculative-decoding-runtime) | Latency acceleration |
| [llm-gateway-saas](https://github.com/JohnScheuer/llm-gateway-saas) | Production LLM SaaS backend |

---

## Selected Systems / Research Repos

- [comm-cost-modeling](https://github.com/JohnScheuer/comm-cost-modeling) — communication modeling across PCIe / NVLink / InfiniBand  
- [llm-serving-sim](https://github.com/JohnScheuer/llm-serving-sim) — end-to-end serving simulation  
- [tensor-memory-allocator](https://github.com/JohnScheuer/tensor-memory-allocator) — allocator policy tradeoffs  
- [continuous-batching-scheduler](https://github.com/JohnScheuer/continuous-batching-scheduler) — scheduling policy comparisons  
- [kv-cache-compaction-lab](https://github.com/JohnScheuer/kv-cache-compaction-lab) — compaction policy analysis  
- [cuda-graph-decode-profiler](https://github.com/JohnScheuer/cuda-graph-decode-profiler) — graph vs eager decode profiling  

---

## Open Source

- Contributed to [LLM Inference Handbook / llm-inference-at-scale](https://github.com/harshuljain13/llm-inference-at-scale)

---

## Experience

Worked on AI infrastructure for a **confidential leading Chinese LLM company** under NDA, with focus on backend/runtime-adjacent systems.

---

## Contact

<p>
  <a href="mailto:johnfelipe13@gmail.com">
    <img src="https://img.shields.io/badge/Email-johnfelipe13%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" />
  </a>
  <a href="https://linkedin.com/in/joaofelipescheuer">
    <img src="https://img.shields.io/badge/LinkedIn-joaofelipescheuer-0A66C2?style=for-the-badge&logo=linkedin" />
  </a>
  <img src="https://img.shields.io/badge/WeChat-JohnScheuer7-07C160?style=for-the-badge&logo=wechat&logoColor=white" />
  <img src="https://img.shields.io/badge/Phone-%2B55%2041%2099705--4864-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />
</p>

- **Email:** johnfelipe13@gmail.com
- **LinkedIn:** [linkedin.com/in/joaofelipescheuer](https://linkedin.com/in/joaofelipescheuer)
- **WeChat:** JohnScheuer7
- **Phone / WhatsApp:** +55 41 99705-4864
- **GitHub:** [github.com/JohnScheuer](https://github.com/JohnScheuer)
