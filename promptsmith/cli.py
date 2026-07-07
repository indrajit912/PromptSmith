"""
Command-line Interface for PromptSmith.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from promptsmith import __version__, __author__, __website__
from promptsmith.formatter import PromptFormatter
from promptsmith.exceptions import PromptSmithError, InputError
from promptsmith.utils.logger import setup_logger, logger
from promptsmith.utils.clipboard import copy_to_clipboard
from promptsmith.canvas import CanvasManager, launch_editor

# Initialize global rich console for pretty CLI output
console = Console()
error_console = Console(stderr=True)

def show_startup_banner() -> None:
    """Prints a beautiful startup banner to the console."""
    ascii_art = r"""[bold cyan]
 ____                           _   ____            _ _   _     
|  _ \ _ __ ___  _ __ ___  _ __| |_/ ___| _ __ ___ (_) |_| |__  
| |_) | '__/ _ \| '_ ` _ \| '_ \ __\___ \| '_ ` _ \| | __| '_ \ 
|  __/| | | (_) | | | | | | |_) | |_ ___) | | | | | | | |_| | | |
|_|   |_|  \___/|_| |_| |_| .__/ \__|____/|_| |_| |_|_|\__|_| |_|
                          |_|                                   [/]"""

    metadata_text = (
        "\n[bold yellow]PromptSmith CLI[/bold yellow] — [italic white]Craft the perfect prompt[/italic white]\n\n"
        f"🚀 [bold green]Version:[/] {__version__}\n"
        f"💻 [bold green]Developer:[/] {__author__}\n"
        f"🌐 [bold green]Website:[/] [blue underline]{__website__}[/]\n"
        f"🐙 [bold green]GitHub:[/] [blue underline]https://github.com/indrajit912/PromptSmith[/]\n"
    )

    # Create a layout grid for side-by-side display
    grid = Table.grid(expand=True)
    grid.add_column(ratio=6)  # Left column: ASCII art
    grid.add_column(ratio=5)  # Right column: details
    grid.add_row(ascii_art, metadata_text)

    console.print(Panel(
        grid,
        title="[bold yellow] Welcome [/bold yellow]",
        border_style="cyan",
        padding=(1, 2)
    ))

def display_custom_help() -> None:
    """Prints a beautifully styled custom help guide to the console."""
    help_header = Panel(
        "[bold cyan]PROMPTSMITH[/bold cyan]\n"
        "[italic white]- CLI Prompt Preparation Tool -[/italic white]",
        border_style="cyan",
        box=box.DOUBLE,
        expand=False,
        padding=(1, 10)
    )
    console.print(help_header)
    
    console.print("\n[bold yellow]Description:[/bold yellow]")
    console.print("  [white]PromptSmith takes your multi-line raw prompts and formats them using[/white]")
    console.print("  [white]optimized instructions tailored for different AI chatbots. By default,[/white]")
    console.print("  [white]the output is automatically copied directly to your clipboard.[/white]\n")
    
    console.print("[bold yellow]Usage:[/bold yellow]")
    console.print("  [bold green]promptsmith[/bold green] [cyan][OPTIONS][/cyan] [magenta][PROMPT][/magenta]\n")
    
    console.print("[bold yellow]Options & Arguments:[/bold yellow]")
    opt_table = Table(box=None, show_header=False, padding=(0, 2))
    opt_table.add_column("Option", style="bold green", width=25)
    opt_table.add_column("Description", style="white")
    
    opt_table.add_row("[magenta]PROMPT[/magenta]", "Optional raw prompt text. If omitted, PromptSmith opens the editor canvas.")
    opt_table.add_row("-s, --style TEXT", "Format style to apply (e.g., [cyan]math[/cyan] [default], [cyan]general[/cyan], [cyan]code[/cyan]).")
    opt_table.add_row("-p, --print", "Print to console/stdout instead of copying to clipboard.")
    opt_table.add_row("-f, --file PATH", "Path to a text file containing the raw prompt.")
    opt_table.add_row("-c, --config [PATH]", "Path to a custom config.toml, or edit active config directly if PATH is omitted.")
    opt_table.add_row("-l, --list-styles", "List all registered prompt styles and exit.")
    opt_table.add_row("-h, --help", "Show this help menu and exit.")
    opt_table.add_row("--version", "Show application version and developer info.")
    opt_table.add_row("--verbose", "Enable debug logging to standard error.")
    
    console.print(opt_table)
    console.print()
    
    console.print("[bold yellow]Examples:[/bold yellow]")
    console.print("  • [italic]Canvas mode (opens configured editor):[/italic]")
    console.print("    [bold green]promptsmith[/bold green]")
    console.print("  • [italic]Format prompt in default math mode and print to terminal:[/italic]")
    console.print("    [bold green]promptsmith[/bold green] -p [magenta]\"Solve x^2 + 5x + 6 = 0\"[/magenta]")
    console.print("  • [italic]Format using the code template and copy to clipboard:[/italic]")
    console.print("    [bold green]promptsmith[/bold green] -s code [magenta]\"Write a quicksort function\"[/magenta]")
    console.print("  • [italic]Read raw prompt from file, apply general style, print to terminal:[/italic]")
    console.print("    [bold green]promptsmith[/bold green] -f raw_prompt.txt -s general -p")
    console.print("  • [italic]Pipe input from standard utilities:[/italic]")
    console.print("    [bold green]cat[/bold green] raw.txt | [bold green]promptsmith[/bold green] -s general -p")
    console.print()
    
    console.print("[bold yellow]Tips & Extensibility:[/bold yellow]")
    console.print("  💡 [bold green]Clipboard:[/bold green] After formatting completes, paste the prompt in ChatGPT/Claude using [bold cyan]Ctrl+V[/bold cyan].")
    console.print("  💡 [bold green]Custom Styles:[/bold green] Add your own templates by creating or editing the TOML config file at:")
    console.print("     [yellow]%APPDATA%\\Local\\promptsmith\\promptsmith\\config.toml[/yellow]")

class CustomCommand(click.Command):
    """Custom Click Command to intercept optional value for --config flag."""
    def parse_args(self, ctx, args):
        new_args = []
        i = 0
        while i < len(args):
            arg = args[i]
            if arg in ("-c", "--config"):
                # Check if there is a next argument and it doesn't start with '-'
                if i + 1 < len(args) and not args[i+1].startswith("-"):
                    new_args.append(arg)
                    new_args.append(args[i+1])
                    i += 2
                else:
                    # No value provided, insert our sentinel
                    new_args.append(arg)
                    new_args.append("EDIT_CONFIG")
                    i += 1
            else:
                new_args.append(arg)
                i += 1
        return super().parse_args(ctx, new_args)

@click.command(cls=CustomCommand, context_settings=dict(help_option_names=[]))
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
@click.option(
    "-h",
    "--help",
    "show_help",
    is_flag=True,
    help="Show this help message and exit."
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
    verbose: bool,
    show_help: bool
) -> None:
    """
    PromptSmith: Prepare and format raw prompts for AI chatbots.
    
    If no prompt or file is provided, PromptSmith will read interactively from standard input.
    """
    # Force UTF-8 encoding on standard streams to avoid encoding crashes on Windows
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if show_help:
        display_custom_help()
        sys.exit(0)

    if config and str(config) == "EDIT_CONFIG":
        try:
            from promptsmith.config import Configuration, create_default_config
            config_obj = Configuration()
            config_path = config_obj.config_path
            
            # Create config file with default values if it doesn't exist
            if not config_path.exists():
                create_default_config(config_path)
                
            config_obj.load()
            editor_cmd = config_obj.settings.get("editor", "vim")
            
            console.print(f"[bold cyan]Opening configuration file in editor ({editor_cmd})...[/bold cyan]")
            launch_editor(editor_cmd, config_path)
            console.print("[bold green]Configuration updated successfully.[/bold green]")
            sys.exit(0)
        except Exception as e:
            error_console.print(f"[bold red]Error editing configuration:[/] {e}")
            sys.exit(1)

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
            
        # Show startup banner if not printing output directly or if running interactively
        is_interactive = not prompt and not file and sys.stdin.isatty()
        if not print_only or is_interactive:
            show_startup_banner()

        # 4. Read the raw input prompt
        raw_prompt = get_raw_prompt(prompt, file, formatter)
        
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
                f"✨ [bold green]Success![/bold green] Formatted prompt copied to your system clipboard.\n"
                f"🎨 Style applied: [bold cyan]{selected_style}[/bold cyan]\n"
                f"📋 Press [bold yellow]Ctrl+V[/bold yellow] (or Cmd+V) to paste directly into your chatbot.",
                title="[bold green]✔ Prompt Prepared[/bold green]",
                border_style="green",
                padding=(1, 2)
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
    finally:
        is_interactive = not prompt and not file and sys.stdin.isatty()
        if is_interactive:
            try:
                from promptsmith.config import get_default_canvas_path
                CanvasManager(get_default_canvas_path()).reset()
            except Exception:
                pass

def get_raw_prompt(prompt_arg: Optional[str], file_path: Optional[Path], formatter: PromptFormatter) -> str:
    """Retrieves raw prompt from file, args, piped stdin, or editor canvas."""
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
        
    # Editor-based workflow
    canvas_path = formatter.get_canvas_path()
    editor_cmd = formatter.config.settings.get("editor", "vim")
    
    manager = CanvasManager(canvas_path)
    
    # 1. Reset canvas file and populate default header
    manager.reset()
    
    # 2. Launch editor
    console.print(f"[bold cyan]Launching editor ({editor_cmd}) to write prompt...[/bold cyan]")
    launch_editor(editor_cmd, canvas_path)
    
    # 3. Read prompt
    return manager.read_prompt()

def display_styles(formatter: PromptFormatter) -> None:
    """Displays available prompt styles in a beautiful table."""
    table = Table(title="[bold cyan]Available PromptSmith Styles[/bold cyan]")
    table.add_column("Style Name", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta", no_wrap=True)
    table.add_column("Description", style="green")
    
    # We want to identify built-in vs user styles
    from promptsmith.styles.builtins import BUILTIN_STYLES_DATA
    builtins = {"general", "math", "code"} | set(BUILTIN_STYLES_DATA.keys())
    
    for style in formatter.registry.list_styles():
        source = "Built-in" if style.name in builtins else "Custom (Config)"
        table.add_row(style.name, source, style.description)
        
    console.print(table)
    
    # Also print config location
    console.print(f"\nConfiguration file: [yellow]{formatter.config.config_path}[/yellow]")

if __name__ == "__main__":
    cli()
