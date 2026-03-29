import sys
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich import box
from agents import run_debate
from scenarios import SCENARIOS

console = Console()


def display_round(round_data: dict):
    """Display a single debate round."""
    round_num = round_data["round"]

    console.print(Rule(f"[bold]Round {round_num}[/bold]", style="dim"))
    console.print()

    console.print(Panel(
        round_data["architect"],
        title="[bold blue]🏗  Architect[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))
    console.print()

    console.print(Panel(
        round_data["critic"],
        title="[bold red]🔍  Critic[/bold red]",
        border_style="red",
        padding=(1, 2)
    ))
    console.print()


def display_synthesis(synthesis: str):
    """Display the final synthesis."""
    console.print(Rule("[bold green]Final Synthesis[/bold green]", style="green"))
    console.print()
    console.print(Panel(
        synthesis,
        title="[bold green]⚡ Recommendation[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    console.print()


def run_scenario(scenario: dict):
    """Run and display a single debate scenario."""
    console.print()
    console.print(Panel.fit(
        f"[bold]{scenario['title']}[/bold]",
        border_style="yellow"
    ))
    console.print()
    console.print(f"[dim]Topic: {scenario['topic'][:200]}...[/dim]" if len(scenario['topic']) > 200 else f"[dim]Topic: {scenario['topic']}[/dim]")
    console.print()

    with console.status("[bold yellow]Running multi-agent debate...[/bold yellow]"):
        result = run_debate(scenario["topic"], rounds=3)

    for round_data in result["rounds"]:
        display_round(round_data)

    display_synthesis(result["synthesis"])
    console.rule(style="dim")


def show_menu():
    """Show scenario selection menu."""
    console.print(Panel.fit(
        "[bold magenta]Multi-Agent Debate System[/bold magenta]\n"
        "[dim]Two AI agents debate technical problems — Architect proposes, Critic challenges[/dim]",
        border_style="magenta"
    ))
    console.print()
    console.print("[bold]Available scenarios:[/bold]")
    console.print()

    for i, scenario in enumerate(SCENARIOS):
        console.print(f"  [bold cyan]{i+1}.[/bold cyan] {scenario['title']}")

    console.print()
    console.print("  [bold cyan]all[/bold cyan] — Run all scenarios")
    console.print()


def main():
    show_menu()

    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = console.input("[bold yellow]Choose a scenario (1-5 or 'all'): [/bold yellow]")

    if arg == "all":
        for scenario in SCENARIOS:
            run_scenario(scenario)
    elif arg.isdigit() and 1 <= int(arg) <= len(SCENARIOS):
        run_scenario(SCENARIOS[int(arg) - 1])
    else:
        console.print("[red]Invalid choice. Run with a number 1-5 or 'all'[/red]")


if __name__ == "__main__":
    main()