# AI Newsletter — Week of 2026-09-06

The week's dominant theme was frontier model competition heating up again: OpenAI shipped GPT-6 Astra and Anthropic released Fable 5.1 within days of each other, each priced at identical $10/$50 input/output rates. For developers the practical question shifts from "which is smarter" to "whose cached-prompt economics fit my workload."

## Top Stories

**GPT-6 Astra launches in limited preview (OpenAI, Sept 3)**
OpenAI released GPT-6 Astra to ChatGPT Plus/Pro/Business/Enterprise and via API on September 3. The model targets complex end-to-end work — coding, computer use, multi-step research, document creation — with a 1,050,000-token context window (128K max output) and an April 2026 knowledge cutoff. API identifier: `gpt-6-astra`. Pricing: $10/$50 per million tokens, 2.5× GPT-5.6 Sol. Availability also via AWS.

**Claude Fable 5.1 and Mythos 5.1 go GA (Anthropic, Sept 1)**
Anthropic released two models simultaneously: Fable 5.1 (frontier) and Mythos 5.1 (reasoning-class). Fable 5.1 holds the same $10/$50 pricing as Fable 5 but cuts prompt-cache reads 75% to $0.25/M tokens — Anthropic estimates ~25% average savings and up to 45% for agentic/coding workloads where cache hits dominate. Fable 5.1 scores 52.6% on Terminal-Bench-Science. Call as `claude-fable-5-1` on Anthropic API, AWS, GCP, and Azure.

**Amazon Nova 2 Sonic: native speech-to-speech**
Amazon introduced the Nova 2 series this week, with Nova 2 Sonic as the standout — a model designed from the ground up for speech-to-speech rather than text-as-intermediate, optimized for low latency and natural turn-taking. Details on API access and pricing via Bedrock are still rolling out.

**AutoSearch: adaptive agentic RAG via reinforcement learning**
A new arXiv paper (2604.17337) proposes AutoSearch, which trains an agent to decide dynamically how many search iterations to spend per query rather than using a fixed retrieval depth. On multi-hop QA benchmarks, the RL-tuned agent matches deeper fixed-depth pipelines at roughly half the retrieval cost — a direct lever for production RAG cost/accuracy tradeoffs.

## Model & API Updates

- **Claude Fable 5.1**: `claude-fable-5-1`, $10/$50, cache reads $0.25/M (down 75%). GA on Anthropic, AWS, GCP, Azure.
- **Claude Mythos 5.1**: Released alongside Fable 5.1; targets long-horizon reasoning tasks.
- **GPT-6 Astra**: `gpt-6-astra`, $10/$50, 1M context, 128K max output. Limited preview via OpenAI API and AWS.
- **Google Gemini 3.6 Flash**: Google pushed additional Gemini 3.x Flash variants this week, including audio and image sub-models; pricing and context details TBA on the Google AI Studio changelog.

## Research Worth Reading

**Fine-Tuning with RAG (ICLR 2026)** — arxiv.org/abs/2510.01375  
Formal analysis of when fine-tuning improves RAG versus when it doesn't. Key finding: a thin LoRA/QLoRA adapter on top of a strong base paired with retrieval beats either approach alone, and distillation clusters at the lowest cost with highest performance on several benchmarks. Recommended pipeline: Prompt → RAG → Fine-tune → Distill.

**Graph-based Agent Memory: Taxonomy, Techniques, and Applications**  
Comprehensive survey covering graph extraction, storage, retrieval, and memory evolution for long-running agents. Useful reference for anyone designing persistent agent state, especially in multi-session or multi-agent architectures.

**SOPRAG: Graph Experts Retrieval for Industrial SOPs**  
Proposes replacing flat chunk-based RAG with graph experts that model entity relationships, causality, and process flows — particularly useful for structured documents like standard operating procedures where step ordering matters.

## Tools & Libraries

**DeepSeek Harness ("Everything is a Plugin")** — ~207k GitHub stars, +12k in the past week  
A plugin-centric inference and tooling harness built around DeepSeek models that has been gaining rapid adoption. The plugin architecture lets teams compose retrieval, tool-calling, and memory layers without forking the core.

**OpenMontage** — open-source agentic video production  
Described as the first open-source agentic video production system, OpenMontage chains script generation, asset sourcing, and editing steps into an agent-driven pipeline. Early-stage but notable as the pattern extends AI coding agents into media production.

**GLM-5.2 (MIT License)** — Z.ai  
The 744B MoE checkpoint (40B active per token) released earlier under MIT is seeing increased downstream adoption now that GLM-5.3-Flash is confirmed in production. GLM-5.2 is tuned for long-horizon coding and agentic workflows and remains one of the largest permissively licensed models available.

## Quick Links

- [GPT-6 Astra API docs](https://developers.openai.com/api/docs/models/gpt-6-astra) — model card, context limits, and pricing breakdown
- [Fable 5.1 benchmark summary](https://llm-stats.com/models/claude-fable-5-1) — Terminal-Bench-Science, cache-read savings estimates
- [AutoSearch paper](https://arxiv.org/abs/2604.17337) — RL-based adaptive search depth for agentic RAG
- [Awesome AI Agent Papers 2026](https://github.com/VoltAgent/awesome-ai-agent-papers) — curated arXiv list covering memory, evaluation, multi-agent coordination, and security
- [Fine-Tuning LLMs in 2026: When RAG Isn't Enough](https://bigdataboutique.com/blog/fine-tuning-llms-when-rag-isnt-enough) — practitioner-oriented breakdown of the Prompt→RAG→Fine-tune→Distill pipeline

---
*Generated by Claude Code on 2026-09-06. Sources: OpenAI, Anthropic, Amazon, arXiv, llm-stats.com, VentureBeat, MarkTechPost, GitHub*
