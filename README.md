# Multi-Agent Debate System

Two AI agents debate technical problems — an Architect proposes solutions, a Critic challenges them — producing battle-tested recommendations through adversarial collaboration.

No single AI perspective. Two agents with opposing roles stress-test every decision.

## How it works
```
Round 1: Architect proposes solution → Critic finds weaknesses
Round 2: Architect responds to criticism → Critic pushes harder  
Round 3: Architect makes final case → Critic gives final verdict
Final:   Neutral synthesis distills key insights and recommendation
```

Each agent has a distinct system prompt, role, and objective. They run as independent Claude instances with no shared context — only the debate transcript connects them.

## Built-in scenarios

| # | Scenario |
|---|---|
| 1 | Microservices vs Monolith for a New Startup |
| 2 | AI Content Moderation System Design |
| 3 | Database Strategy for Rapid Scale |
| 4 | Deploying LLMs Safely in Production |
| 5 | Candidate evaluation for AI Engineer role |

## Setup
```bash
git clone https://github.com/kajolgulabani171995/multi-agent-system.git
cd multi-agent-system
python3 -m venv venv
source venv/bin/activate
pip install anthropic python-dotenv rich
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## Run
```bash
python3 run.py
```

Select a scenario from the menu, or run all:
```bash
python3 run.py all
```

## Add your own scenario

Add to `scenarios.py`:
```python
{
    "name": "your_scenario",
    "title": "Your Debate Title",
    "topic": "Describe the problem or decision to debate in detail."
}
```

Then run and select it from the menu.

## Sample output
```
──────────────────────── Round 1 ────────────────────────

╭─ 🏗  Architect ────────────────────────────────────────╮
│ I recommend starting with a well-structured monolith.  │
│ With 5 engineers, the overhead of microservices will   │
│ slow you down more than it helps...                    │
╰────────────────────────────────────────────────────────╯

╭─ 🔍  Critic ───────────────────────────────────────────╮
│ You're ignoring the 10x growth requirement. If you     │
│ build a monolith now, you're guaranteeing a painful    │
│ rewrite in 18 months. What's your migration plan?...  │
╰────────────────────────────────────────────────────────╯

──────────────────── Final Synthesis ────────────────────

╭─ ⚡ Recommendation ────────────────────────────────────╮
│ 1. Start modular monolith with clear service           │
│    boundaries — extract to microservices only when     │
│    scaling pain is real, not anticipated               │
│ 2. Watch out for: premature optimization, team         │
│    coordination overhead, deployment complexity        │
│ 3. Both agreed: team size is the most important factor │
╰────────────────────────────────────────────────────────╯
```

## Project structure
```
multi-agent-system/
├── agents.py      # Architect + Critic + Synthesis agent logic
├── scenarios.py   # 5 built-in debate scenarios
├── run.py         # CLI runner with rich terminal UI
└── .env           # API key (not committed)
```

## Tech stack

- Python 3.12
- Anthropic API (claude-haiku-4-5)
- Rich (terminal UI)
- python-dotenv