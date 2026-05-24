# AI Newsletter — Week of 2026-05-24

Google I/O 2026 dominated the week, shipping Gemini 3.5 Flash to GA and previewing an agentic platform that signals a hard shift toward agent-first development. Anthropic countered with a developer-focused London event that introduced sandboxed multi-agent infrastructure and a public-beta security toolchain.

## Top Stories

**Google I/O 2026: Gemini Goes Agentic**
Google released Gemini 3.5 Flash at GA via the Gemini API and AI Studio, outperforming Gemini 3.1 Pro on Terminal-Bench 2.1 (76.2%), GDPval-AA (1656 Elo), and multimodal benchmarks (CharXiv: 84.2%) at Flash-tier speed and cost. The bigger story is Antigravity 2.0: developers can now spin up specialized subagents with built-in sandboxing, credential masking, and hardened Git policies. Managed Agents in the Gemini API provisions a full agent with a remote sandbox from a single API call — no infra setup required.

**Anthropic Code with Claude London**
Anthropic rolled out Claude Agent sandboxes that let companies run agents on their own infrastructure, plus "MCP tunnels" for agents to reach internal systems without touching the public internet. A new "dreaming" feature lets agents write notes to themselves that other agents can consume, enabling faster context handoff in multi-agent workflows. Claude Security entered public beta, adding code scanning, vulnerability triage, and fix generation for eligible security teams.

**OpenAI Codex Extends to Mobile and On-Prem**
OpenAI partnered with Dell to bring Codex to hybrid and on-premises enterprise environments (May 19). The Codex mobile extension for ChatGPT lets developers monitor workflows, approve commands, and supervise coding agents from a smartphone. OpenAI also strengthened AI content provenance: images generated with OpenAI tools now carry C2PA conformance and SynthID watermarks, with a public verification tool in preview.

**KPMG and SAP Embed Claude at Scale**
KPMG signed a global alliance with Anthropic, giving all 276,000+ employees access to Claude through its Digital Gateway platform. SAP announced plans to embed Claude as the primary reasoning and agentic capability across SAP Business AI Platform, announced at SAP Sapphire. Both deals reflect enterprises moving from pilot to firm-wide AI deployment.

## Model & API Updates

- **Gemini 3.5 Flash** — GA as of Google I/O (May 19). Surpasses 3.1 Pro on coding, agentic, and multimodal benchmarks; 4× faster output tokens/sec than competing frontier models. Gemini 3.5 Pro in testing, expected next month.
- **Gemini Omni** — New multimodal model that accepts text, audio, image, and video inputs to produce dynamic video output. Rolling out to Gemini API and Agent Platform API in coming weeks.
- **Qwen3 Coder Next** — Code-specialist variant with long-context support for multi-file and large-repo tasks; released May 18 on LLM Gateway.
- **ZAYA1-8B** — Open-source MoE reasoning model from Zyphra: 8B total params, ~760M active per token, trained end-to-end on AMD Instinct hardware. Useful for cost-sensitive inference.
- **Gemini API: Built-in Tools + Function Calling** — Google shipped the ability to combine Gemini built-in tools (Search, Code Execution) with custom function calling in a single API call.

## Research Worth Reading

**"Thinking with Visual Primitives" (DeepSeek-AI)** — Addresses the "Reference Gap" in multimodal models, where systems struggle to link textual concepts to specific visual coordinates. The paper proposes a new reasoning paradigm that improves complex visual grounding accuracy. Practical for developers building visual agents or document-understanding pipelines. [ArXiv / Hugging Face Papers]

**WebMCP Proposal (Google)** — An open web standard that exposes structured JavaScript functions and HTML forms as tools for browser-based AI agents, enabling faster and more reliable task execution without screen-scraping. An origin trial starts in Chrome 149. Worth watching as a potential replacement for fragile DOM-traversal automation.

**Elicit Accuracy Report (May 2026)** — Elicit hit 95% search recall, 97% abstract screening, 99% full-text screening across 994 Cochrane reviews, narrowing the gap with human systematic-review workflows. Relevant for research-augmented RAG pipelines.

## Tools & Libraries

- **Antigravity CLI (Google)** — New open CLI for Antigravity agent platform: spawn subagents, manage workflows, built-in sandbox and credential masking. Available now with Gemini API.
- **NVIDIA Nemotron 3 (open models)** — New family of open models covering speech, multimodal RAG, and safety. NVIDIA also released dataset and training code for Llama Embed Nemotron 8B plus an updated LLM Router for automatic model selection.
- **Claude Agent Sandboxes (Anthropic)** — Self-hostable sandboxes for Claude Code agents, with MCP tunnels for secure internal-network access. Aimed at teams that can't route agent traffic through the public internet.
- **AlpaSim** — Open-source simulation framework for closed-loop training and evaluation of reasoning-based autonomous vehicle models. Practical for ML teams needing diverse edge-case environments.

## Quick Links

- [100 things announced at Google I/O 2026](https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/) — Full list including Android XR, SynthID, Gemini for Science.
- [OpenAI Deployment Company launch](https://openai.com/index/openai-launches-the-deployment-company/) — $4B-backed venture to help businesses operationalize AI workflows.
- [Anthropic Claude Security public beta](https://red.anthropic.com/2026/mythos-preview/) — New cyber-verification tools for security teams using Claude.
- [Gemini API changelog](https://ai.google.dev/gemini-api/docs/changelog) — Built-in tools + function calling combination now live.
- [MIT Tech Review: Code with Claude London](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/) — Critical look at what Anthropic's agentic coding demo means for software engineers.

---
*Generated by Claude Code on 2026-05-24. Sources: Google Developers Blog, 9to5Google, Anthropic News, MIT Technology Review, TechCrunch, llm-stats.com, buildfastwithai.com, Medium (David Akpovi), NVIDIA Blog, releasebot.io*
