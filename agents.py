import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def run_architect(topic: str, conversation_history: list, round_num: int) -> str:
    """Agent 1 — The Architect. Proposes and defends solutions."""

    system = (
        "You are a senior software architect with 15 years of experience. "
        "Your role is to propose technical solutions and defend them under scrutiny. "
        "Be specific, use concrete examples, and back your proposals with reasoning. "
        "When responding to criticism, acknowledge valid points but defend what you believe is right. "
        "Keep responses focused and under 200 words."
    )

    if round_num == 1:
        prompt = f"Propose a technical solution for the following problem:\n\n{topic}\n\nBe specific about architecture, technology choices, and key design decisions."
    else:
        last_critic = next((m["content"] for m in reversed(conversation_history) if m["content"].startswith("CRITIC:")), "")
        prompt = f"The critic has raised these concerns:\n\n{last_critic}\n\nRespond to the criticism. Acknowledge valid points, defend your position where appropriate, and refine your proposal."

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def run_critic(topic: str, proposal: str, conversation_history: list, round_num: int) -> str:
    """Agent 2 — The Critic. Finds weaknesses and asks hard questions."""

    system = (
        "You are a skeptical senior engineer and technical lead. "
        "Your role is to critically evaluate technical proposals and find weaknesses. "
        "Ask hard questions about scalability, security, maintainability, and cost. "
        "Don't accept vague answers — push for specifics. "
        "Be direct but constructive. Acknowledge improvements when made. "
        "Keep responses focused and under 200 words."
    )

    if round_num == 1:
        prompt = f"The architect has proposed the following solution:\n\n{proposal}\n\nCritically evaluate this proposal. What are the weaknesses? What important considerations are missing? Ask 2-3 specific hard questions."
    else:
        prompt = f"The architect responded:\n\n{proposal}\n\nEvaluate their response. Have they addressed your concerns adequately? Push harder on unresolved issues or acknowledge improvements and raise new concerns."

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def run_final_synthesis(topic: str, conversation_history: list) -> str:
    """Synthesize the debate into a final recommendation."""

    debate_text = "\n\n".join([m["content"] for m in conversation_history])

    prompt = (
        f"You observed a debate about:\n{topic}\n\n"
        f"Here is the full debate:\n{debate_text}\n\n"
        f"Synthesize the key insights into:\n"
        f"1. Final recommended approach (2-3 sentences)\n"
        f"2. Top 3 things to watch out for\n"
        f"3. One thing both sides agreed on\n"
        f"Be concise and actionable."
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system="You are a neutral technical advisor synthesizing a debate into clear recommendations.",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()


def run_debate(topic: str, rounds: int = 3) -> dict:
    """Run a full multi-agent debate on a topic."""

    conversation_history = []
    rounds_data = []

    for round_num in range(1, rounds + 1):
        architect_response = run_architect(topic, conversation_history, round_num)
        conversation_history.append({
            "role": "user",
            "content": f"ARCHITECT: {architect_response}"
        })

        critic_response = run_critic(topic, architect_response, conversation_history, round_num)
        conversation_history.append({
            "role": "assistant",
            "content": f"CRITIC: {critic_response}"
        })

        rounds_data.append({
            "round": round_num,
            "architect": architect_response,
            "critic": critic_response
        })

    synthesis = run_final_synthesis(topic, conversation_history)

    return {
        "topic": topic,
        "rounds": rounds_data,
        "synthesis": synthesis
    }