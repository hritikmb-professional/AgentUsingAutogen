# AutoGen Multi-Model Agent System

Marketing campaign brainstorming system using AutoGen framework with multi-model LLM collaboration and human-in-the-loop interaction.

## Features

**Dual-Agent Marketing Team**
- **CMO Agent:** Strategic planning and audience targeting
- **Brand Marketer Agent:** Tactical campaign ideas and KPIs
- Automated collaborative conversations

**Multi-Model Support**
- OpenAI GPT-4o-mini
- Google Gemini 2.0 Flash
- Cross-provider agent collaboration

**Three Interaction Modes**
1. **Single-model:** Both agents using OpenAI
2. **Multi-model:** CMO (Gemini) + Marketer (OpenAI)
3. **Human-in-the-Loop:** Group chat with user participation

## Tech Stack

- **Framework:** AutoGen (Microsoft)
- **Models:** GPT-4o-mini, Gemini 2.0 Flash
- **Interface:** Gradio (ready for UI)
- **Libraries:** google-generativeai, openai

## Use Case

Sustainable shoe brand marketing campaign development with:
- Target audience definition
- Channel strategy
- KPI recommendations
- Creative concept brainstorming

## Setup

```bash
pip install pyautogen openai google-generativeai gradio python-dotenv
```

Create `.env`:
```
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

Run:
```bash
python autog.py
```

## Conversation Flow

Agents automatically collaborate for 4 turns, then switch to group chat mode where users can guide the brainstorming process. Type `exit` to terminate.

Perfect for testing multi-agent LLM orchestration and comparing different model behaviors in collaborative tasks.
