"""
Command-line Interface for PromptSmith.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from promptsmith import __version__, __author__, __website__
from promptsmith.formatter import PromptFormatter
from promptsmith.exceptions import PromptSmithError, InputError
from promptsmith.utils.logger import setup_logger, logger
from promptsmith.utils.clipboard import copy_to_clipboard

# Initialize global rich console for pretty CLI output
console = Console()
error_console = Console(stderr=True)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument("prompt", required=False, type=str)
@click.option(
    "-s",
    "--style",
    type=str,
    default=None,
    help="The prompt style to apply (e.g. general, math, code, or custom styles)."
)
@click.option(
    "-p",
    "--print",
    "print_only",
    is_flag=True,
    help="Print the formatted prompt to the terminal instead of copying to the clipboard."
)
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Path to a text file containing the raw prompt."
)
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False, path_type=Path),
    help="Path to a custom config.toml file."
)
@click.option(
    "-l",
    "--list-styles",
    is_flag=True,
    help="List all registered prompt styles and exit."
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output for debugging."
)
@click.version_option(
    version=__version__,
    prog_name="PromptSmith",
    message="%(prog)s version %(version)s\nDeveloped by Indrajit Ghosh (https://indrajitghosh.onrender.com)"
)
def cli(
    prompt: Optional[str],
    style: Optional[str],
    print_only: bool,
    file: Optional[Path],
    config: Optional[Path],
    list_styles: bool,
    verbose: bool
) -> None:
    """
    PromptSmith: Prepare and format raw prompts for AI chatbots.
    
    If no prompt or file is provided, PromptSmith will read interactively from standard input.
    """
    # 1. Setup logging
    setup_logger(verbose)
    logger.debug("PromptSmith started.")
    
    try:
        # 2. Initialize formatter and load configuration
        formatter = PromptFormatter(config)
        
        with console.status("[bold green]Loading configuration...[/bold green]", spinner="dots"):
            formatter.initialize()
            
        # 3. Handle list styles option
        if list_styles:
            display_styles(formatter)
            sys.exit(0)
            
        # 4. Read the raw input prompt
        raw_prompt = get_raw_prompt(prompt, file)
        
        # 5. Format the prompt
        selected_style = style or formatter.config.settings.get("default_style", "general")
        logger.debug(f"Formatting prompt with style: {selected_style}")
        
        with console.status(f"[bold green]Formatting prompt using '{selected_style}' style...[/bold green]"):
            formatted_prompt = formatter.format_prompt(raw_prompt, selected_style)
            
        # 6. Output the formatted prompt (copy or print)
        # Default behavior: check if config or cli wants clipboard or print
        # cli option `--print` overrides config
        default_clipboard = formatter.config.settings.get("default_to_clipboard", True)
        should_copy = default_clipboard and not print_only
        
        if should_copy:
            with console.status("[bold green]Copying to clipboard...[/bold green]"):
                copy_to_clipboard(formatted_prompt)
            console.print(Panel(
                f"[bold green]Success![/bold green] Formatted prompt copied to the clipboard.\n"
                f"Style applied: [bold cyan]{selected_style}[/bold cyan]\n"
                f"You can now paste (Ctrl+V) it directly into your AI chatbot.",
                title="[bold green]PromptSmith[/bold green]",
                border_style="green"
            ))
        else:
            # Print to stdout
            console.print(formatted_prompt)
            
    except PromptSmithError as e:
        error_console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        error_console.print("\n[bold yellow]Aborted by user.[/bold yellow]")
        sys.exit(130)
    except Exception as e:
        logger.exception("An unexpected error occurred:")
        error_console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
        sys.exit(1)

def get_raw_prompt(prompt_arg: Optional[str], file_path: Optional[Path]) -> str:
    """Retrieves raw prompt from file, args, piped stdin, or interactive terminal."""
    if file_path:
        try:
            logger.debug(f"Reading prompt from file: {file_path}")
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise InputError(f"Failed to read file '{file_path}': {e}")
            
    if prompt_arg:
        logger.debug("Using prompt from CLI positional argument.")
        return prompt_arg
        
    # Read from stdin if piped
    if not sys.stdin.isatty():
        logger.debug("Reading prompt from piped stdin.")
        return sys.stdin.read()
        
    # Interactive input
    eof_key = "Ctrl+Z then Enter" if os.name == "nt" else "Ctrl+D"
    console.print(Panel(
        "[bold cyan]Interactive Raw Prompt Input[/bold cyan]\n"
        f"Enter or paste your raw prompt. Press [bold green]{eof_key}[/bold green] on a new line to finish.",
        title="[bold yellow]PromptSmith[/bold yellow]",
        border_style="cyan"
    ))
    
    try:
        lines = []
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
        
    raw_prompt = "\n".join(lines)
    if not raw_prompt.strip():
        raise InputError("Raw prompt cannot be empty. Please provide a prompt or use --help.")
    return raw_prompt

def display_styles(formatter: PromptFormatter) -> None:
    """Displays available prompt styles in a beautiful table."""
    table = Table(title="[bold cyan]Available PromptSmith Styles[/bold cyan]")
    table.add_column("Style Name", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta", no_wrap=True)
    table.add_column("Description", style="green")
    
    # We want to identify built-in vs user styles
    builtins = {"general", "math", "code"}
    
    for style in formatter.registry.list_styles():
        source = "Built-in" if style.name in builtins else "Custom (Config)"
        table.add_row(style.name, source, style.description)
        
    console.print(table)
    
    # Also print config location
    console.print(f"\nConfiguration file: [yellow]{formatter.config.config_path}[/yellow]")

if __name__ == "__main__":
    cli()
