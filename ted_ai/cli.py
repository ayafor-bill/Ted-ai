"""
Ted-AI Enhanced CLI Interface

Sophisticated command-line interface with rich formatting,
interactive features, and comprehensive command set.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from enum import Enum

# Rich for beautiful terminal output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.prompt import Prompt, Confirm
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Warning: Rich library not installed. Using basic output.")

from database import DatabaseManager, DatabaseConfig
from models import (
    EngagementStatus, SeverityLevel, EvidenceType
)
from core.reasoning_engine import ReasoningEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CLIState:
    """Manages current CLI session state"""
    def __init__(self):
        self.current_engagement_id: Optional[int] = None
        self.current_engagement_name: Optional[str] = None
        self.command_history: List[str] = []
        self.last_recommendations: List[Dict[str, Any]] = []


class TEDCLIInterface:
    """
    Enhanced CLI interface for Ted-AI with rich formatting,
    interactive features, and comprehensive commands.
    """

    def __init__(self, db_path: str = "ted_ai.db"):
        self.db = DatabaseManager(DatabaseConfig(db_path=db_path))
        self.reasoning_engine = ReasoningEngine()
        self.state = CLIState()
        
        if HAS_RICH:
            self.console = Console()
        else:
            self.console = None

    def print(self, message: str, style: Optional[str] = None):
        """Print message with optional styling"""
        if self.console:
            self.console.print(message, style=style)
        else:
            print(message)

    def print_table(self, data: List[Dict[str, Any]], title: str = ""):
        """Print formatted table"""
        if not data:
            self.print("[yellow]No data to display[/yellow]")
            return

        if HAS_RICH:
            table = Table(title=title)
            
            # Add columns
            for key in data[0].keys():
                table.add_column(str(key), style="cyan")
            
            # Add rows
            for row in data:
                table.add_row(*[str(v) for v in row.values()])
            
            self.console.print(table)
        else:
            # Fallback to simple text output
            headers = " | ".join(data[0].keys())
            self.print(headers)
            self.print("-" * len(headers))
            for row in data:
                self.print(" | ".join(str(v) for v in row.values()))

    def print_panel(self, content: str, title: str = "Info"):
        """Print content in a panel"""
        if HAS_RICH:
            self.console.print(Panel(content, title=title))
        else:
            self.print(f"\n=== {title} ===")
            self.print(content)
            self.print("=" * (len(title) + 8))

    # ==================== Engagement Commands ====================

    def cmd_new_engagement(self):
        """Create a new engagement"""
        self.print_panel(
            "Create a new penetration testing engagement",
            "New Engagement"
        )

        target_name = Prompt.ask("[cyan]Target Name[/cyan]") if HAS_RICH else input("Target Name: ")
        target_type = Prompt.ask(
            "[cyan]Target Type[/cyan]",
            choices=["web_app", "api", "mobile", "network", "cloud"]
        ) if HAS_RICH else input("Target Type (web_app/api/mobile/network/cloud): ")
        
        target_url = Prompt.ask(
            "[cyan]Target URL[/cyan]",
            default=""
        ) if HAS_RICH else input("Target URL (optional): ")
        
        client_name = Prompt.ask(
            "[cyan]Client Name[/cyan]",
            default=""
        ) if HAS_RICH else input("Client Name (optional): ")
        
        scope = Prompt.ask(
            "[cyan]Scope[/cyan]",
            default=""
        ) if HAS_RICH else input("Scope (optional): ")

        try:
            engagement = self.db.create_engagement(
                target_name=target_name,
                target_type=target_type,
                target_url=target_url or None,
                client_name=client_name or None,
                scope=scope or None
            )
            
            self.state.current_engagement_id = engagement.id
            self.state.current_engagement_name = engagement.target_name
            
            self.print(
                f"[green]✓ Engagement created: {target_name} (ID: {engagement.id})[/green]"
            )
            self.print_engagement_summary(engagement)
            
        except Exception as e:
            self.print(f"[red]✗ Error creating engagement: {str(e)}[/red]")
            logger.error(f"Error creating engagement: {str(e)}")

    def cmd_list_engagements(self):
        """List all engagements"""
        try:
            engagements = self.db.get_all_engagements()
            
            if not engagements:
                self.print("[yellow]No engagements found[/yellow]")
                return

            data = [
                {
                    "ID": eng.id,
                    "Target": eng.target_name,
                    "Type": eng.target_type,
                    "Status": eng.status.value,
                    "Client": eng.client_name or "-",
                    "Created": eng.created_at.strftime("%Y-%m-%d"),
                }
                for eng in engagements
            ]
            
            self.print_table(data, "Engagements")
            
        except Exception as e:
            self.print(f"[red]✗ Error listing engagements: {str(e)}[/red]")

    def cmd_select_engagement(self):
        """Select current engagement"""
        engagement_id = Prompt.ask("[cyan]Engagement ID[/cyan]") if HAS_RICH else input("Engagement ID: ")
        
        try:
            engagement = self.db.get_engagement(int(engagement_id))
            if engagement:
                self.state.current_engagement_id = engagement.id
                self.state.current_engagement_name = engagement.target_name
                self.print(
                    f"[green]✓ Switched to engagement: {engagement.target_name}[/green]"
                )
                self.print_engagement_summary(engagement)
            else:
                self.print("[red]✗ Engagement not found[/red]")
        except ValueError:
            self.print("[red]✗ Invalid engagement ID[/red]")

    def print_engagement_summary(self, engagement):
        """Print engagement summary"""
        summary = self.db.get_engagement_summary(engagement.id)
        if not summary:
            return

        summary_text = f"""
[bold]Target:[/bold] {engagement.target_name}
[bold]Type:[/bold] {engagement.target_type}
[bold]Status:[/bold] {engagement.status.value}
[bold]Client:[/bold] {engagement.client_name or 'N/A'}
[bold]Progress:[/bold] {summary.progress_percentage():.1f}% ({summary.completed_objectives}/{summary.total_objectives} objectives)
[bold]Evidence:[/bold] {summary.total_evidence} items
[bold]Findings:[/bold] {summary.total_findings} ({summary.critical_findings} critical, {summary.high_findings} high)
"""
        self.print_panel(summary_text.strip(), "Engagement Summary")

    # ==================== Objective Commands ====================

    def cmd_add_objective(self):
        """Add testing objective"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        self.print_panel("Add Testing Objective", "New Objective")

        title = Prompt.ask("[cyan]Objective Title[/cyan]") if HAS_RICH else input("Title: ")
        description = Prompt.ask(
            "[cyan]Description[/cyan]"
        ) if HAS_RICH else input("Description: ")
        
        objective_type = Prompt.ask(
            "[cyan]Type[/cyan]",
            choices=["reconnaissance", "authentication", "authorization", "injection",
                    "api_testing", "business_logic", "other"]
        ) if HAS_RICH else input("Type: ")
        
        priority = Prompt.ask(
            "[cyan]Priority (1-10)[/cyan]",
            default="1"
        ) if HAS_RICH else input("Priority (1-10, default 1): ")

        try:
            obj = self.db.create_objective(
                engagement_id=self.state.current_engagement_id,
                title=title,
                description=description,
                objective_type=objective_type,
                priority=int(priority)
            )
            self.print(f"[green]✓ Objective created: {title} (ID: {obj.id})[/green]")
        except Exception as e:
            self.print(f"[red]✗ Error creating objective: {str(e)}[/red]")

    def cmd_list_objectives(self):
        """List engagement objectives"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        try:
            objectives = self.db.get_engagement_objectives(
                self.state.current_engagement_id
            )
            
            if not objectives:
                self.print("[yellow]No objectives found[/yellow]")
                return

            data = [
                {
                    "ID": obj.id,
                    "Title": obj.title,
                    "Type": obj.objective_type,
                    "Priority": obj.priority,
                    "Status": obj.status,
                    "Progress": f"{obj.progress_percentage}%",
                }
                for obj in objectives
            ]
            
            self.print_table(data, "Objectives")
            
        except Exception as e:
            self.print(f"[red]✗ Error listing objectives: {str(e)}[/red]")

    # ==================== Evidence Commands ====================

    def cmd_add_evidence(self):
        """Add evidence to engagement"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        self.print_panel("Add Evidence", "New Evidence")

        title = Prompt.ask("[cyan]Evidence Title[/cyan]") if HAS_RICH else input("Title: ")
        description = Prompt.ask(
            "[cyan]Description[/cyan]"
        ) if HAS_RICH else input("Description: ")
        
        evidence_type = Prompt.ask(
            "[cyan]Evidence Type[/cyan]",
            choices=[et.value for et in EvidenceType]
        ) if HAS_RICH else input("Evidence Type: ")
        
        confidence = Prompt.ask(
            "[cyan]Confidence Level (0.0-1.0)[/cyan]",
            default="0.5"
        ) if HAS_RICH else input("Confidence Level (0.0-1.0, default 0.5): ")
        
        endpoint = Prompt.ask(
            "[cyan]Affected Endpoint[/cyan]",
            default=""
        ) if HAS_RICH else input("Affected Endpoint (optional): ")

        try:
            evidence = self.db.add_evidence(
                engagement_id=self.state.current_engagement_id,
                evidence_type=EvidenceType(evidence_type),
                title=title,
                description=description,
                affected_endpoint=endpoint or None,
                confidence_level=float(confidence)
            )
            self.print(
                f"[green]✓ Evidence added: {title} (ID: {evidence.id})[/green]"
            )
        except Exception as e:
            self.print(f"[red]✗ Error adding evidence: {str(e)}[/red]")

    def cmd_list_evidence(self):
        """List engagement evidence"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        try:
            evidence = self.db.get_engagement_evidence(
                self.state.current_engagement_id
            )
            
            if not evidence:
                self.print("[yellow]No evidence found[/yellow]")
                return

            data = [
                {
                    "ID": ev.id,
                    "Title": ev.title,
                    "Type": ev.evidence_type.value,
                    "Confidence": f"{ev.confidence_level:.2f}",
                    "Endpoint": ev.affected_endpoint or "-",
                    "Collected": ev.collected_at.strftime("%Y-%m-%d %H:%M"),
                }
                for ev in evidence
            ]
            
            self.print_table(data, "Evidence")
            
        except Exception as e:
            self.print(f"[red]✗ Error listing evidence: {str(e)}[/red]")

    # ==================== Finding Commands ====================

    def cmd_list_findings(self):
        """List engagement findings"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        try:
            findings = self.db.get_engagement_findings(
                self.state.current_engagement_id
            )
            
            if not findings:
                self.print("[yellow]No findings found[/yellow]")
                return

            data = [
                {
                    "ID": f.id,
                    "Title": f.title,
                    "Severity": f.severity.value,
                    "Type": f.finding_type,
                    "Status": f.status,
                    "CVSS": f.cvss_score or "-",
                }
                for f in findings
            ]
            
            self.print_table(data, "Findings")
            
        except Exception as e:
            self.print(f"[red]✗ Error listing findings: {str(e)}[/red]")

    # ==================== Analysis Commands ====================

    def cmd_analyze(self):
        """Perform engagement analysis"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        try:
            engagement = self.db.get_engagement(self.state.current_engagement_id)
            
            # Build context for analysis
            context = {
                "engagement": engagement.to_dict() if hasattr(engagement, 'to_dict') else {},
                "objectives": [obj.to_dict() for obj in engagement.objectives],
                "evidence": [ev.to_dict() for ev in engagement.evidence],
                "findings": [f.to_dict() for f in engagement.findings],
                "hypotheses": [h.to_dict() for h in engagement.hypotheses],
            }
            
            self.print("[cyan]Analyzing engagement...[/cyan]")
            
            # Run analysis
            analysis = self.reasoning_engine.analyze_engagement(context)
            
            # Generate recommendations
            recommendations = self.reasoning_engine.generate_recommendations(
                context, analysis
            )
            
            self.state.last_recommendations = [asdict(r) for r in recommendations]
            
            # Display results
            self._display_analysis_results(analysis, recommendations)
            
        except Exception as e:
            self.print(f"[red]✗ Analysis error: {str(e)}[/red]")
            logger.error(f"Analysis error: {str(e)}")

    def _display_analysis_results(self, analysis: Dict[str, Any], recommendations: List):
        """Display analysis results"""
        self.print_panel(
            f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Analysis Results"
        )
        
        if recommendations:
            self.print("\n[bold green]Recommended Actions:[/bold green]")
            for i, rec in enumerate(recommendations[:5], 1):
                priority_emoji = "🔴" if rec.priority <= 1 else "🟡" if rec.priority <= 3 else "🟢"
                self.print(
                    f"{priority_emoji} [{i}] {rec.title}\n"
                    f"    {rec.description}\n"
                    f"    Effort: {rec.effort_estimate} | "
                    f"Success: {rec.success_probability:.1%}\n"
                )

    # ==================== Statistics Commands ====================

    def cmd_statistics(self):
        """Display engagement statistics"""
        if not self.state.current_engagement_id:
            self.print("[red]✗ No engagement selected[/red]")
            return

        try:
            stats = self.db.get_engagement_statistics(
                self.state.current_engagement_id
            )
            
            if not stats:
                self.print("[red]✗ No statistics available[/red]")
                return

            stats_text = f"""
[bold]Target:[/bold] {stats.get('target')}
[bold]Progress:[/bold] {stats.get('progress', 0):.1f}%

[bold]Objectives:[/bold]
  Total: {stats.get('objectives', {}).get('total', 0)}
  Completed: {stats.get('objectives', {}).get('completed', 0)}

[bold]Findings:[/bold]
  Total: {stats.get('findings', {}).get('total', 0)}
  Critical: {stats.get('findings', {}).get('critical', 0)}
  High: {stats.get('findings', {}).get('high', 0)}

[bold]Evidence Collected:[/bold] {stats.get('evidence', {}).get('total', 0)} items
"""
            self.print_panel(stats_text.strip(), "Engagement Statistics")
            
        except Exception as e:
            self.print(f"[red]✗ Error retrieving statistics: {str(e)}[/red]")

    # ==================== Help and Utility Commands ====================

    def cmd_help(self):
        """Display help information"""
        help_text = """
[bold cyan]Ted-AI - Penetration Testing Copilot[/bold cyan]

[bold]Engagement Management:[/bold]
  new         - Create new engagement
  list        - List all engagements
  select      - Select current engagement
  status      - Show current engagement status

[bold]Testing Objectives:[/bold]
  obj-add     - Add testing objective
  obj-list    - List objectives

[bold]Evidence Collection:[/bold]
  ev-add      - Add evidence
  ev-list     - List evidence

[bold]Findings:[/bold]
  find-list   - List findings

[bold]Analysis:[/bold]
  analyze     - Analyze engagement and get recommendations
  stats       - Display engagement statistics

[bold]Utility:[/bold]
  help        - Show this help message
  exit        - Exit the application
"""
        self.print(help_text)

    def cmd_exit(self):
        """Exit the application"""
        self.print("[cyan]Closing Ted-AI...[/cyan]")
        self.db.close()
        sys.exit(0)

    # ==================== Main REPL ====================

    def run(self):
        """Run the interactive CLI"""
        self.print_banner()
        
        commands = {
            "new": self.cmd_new_engagement,
            "list": self.cmd_list_engagements,
            "select": self.cmd_select_engagement,
            "status": lambda: self.print(f"Current engagement: {self.state.current_engagement_name or 'None'}"),
            "obj-add": self.cmd_add_objective,
            "obj-list": self.cmd_list_objectives,
            "ev-add": self.cmd_add_evidence,
            "ev-list": self.cmd_list_evidence,
            "find-list": self.cmd_list_findings,
            "analyze": self.cmd_analyze,
            "stats": self.cmd_statistics,
            "help": self.cmd_help,
            "exit": self.cmd_exit,
        }
        
        while True:
            try:
                prompt = f"[{self.state.current_engagement_name or 'TED'}]> " if HAS_RICH else f"[{self.state.current_engagement_name or 'TED'}]> "
                command = Prompt.ask(prompt).strip() if HAS_RICH else input(prompt).strip()
                
                if not command:
                    continue
                
                if command in commands:
                    commands[command]()
                else:
                    self.print(f"[red]Unknown command: {command}[/red]")
                    self.print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                self.print("\n[yellow]Use 'exit' command to quit[/yellow]")
            except Exception as e:
                self.print(f"[red]Error: {str(e)}[/red]")
                logger.error(f"REPL error: {str(e)}")

    def print_banner(self):
        """Print application banner"""
        banner = """
[bold cyan]
  ████████████████████████████
  ████  TED-AI v2.0  ████
  ████████████████████████████
[/bold cyan]

[cyan]Bug Bounty & Penetration Testing Copilot[/cyan]
[dim]Type 'help' for available commands[/dim]
"""
        self.print(banner)


def asdict(obj):
    """Simple dataclass to dict converter"""
    if hasattr(obj, '__dataclass_fields__'):
        return {k: getattr(obj, k) for k in obj.__dataclass_fields__}
    return obj


if __name__ == "__main__":
    cli = TEDCLIInterface()
    cli.run()