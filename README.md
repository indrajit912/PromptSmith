# PromptSmith 🛠️

**PromptSmith** is a professional, developer-friendly Python command-line interface (CLI) application designed to prepare and optimize prompts for AI chatbots (such as ChatGPT, Claude, Gemini, etc.). It transforms raw user strings into highly structured, context-rich prompts designed to elicit higher-quality, more deterministic outputs from large language models (LLMs).

---

## Features

- ✨ **Beautiful UI:** Polished, colorful console output using the `rich` library, complete with interactive animations and loading statuses.
- ⚙️ **Extensible Architecture:** Out-of-the-box support for multiple prompt modes (`general`, `math`, `code`), and easily extensible through local configuration.
- 📋 **Seamless Clipboard Integration:** By default, formatted prompts are copied directly to your system clipboard so you can paste them immediately into your chatbot.
- 🖨️ **Print Override:** Easily output directly to standard output or redirect to files using the `-p` / `--print` flag.
- 📂 **Flexible Input Formats:** Accept input via interactive multi-line terminal prompt, standard input piping (standard unix pipe/redirect), CLI argument, or file input.
- 🔧 **Zero-Configuration Default & Auto-Init:** Run the app immediately. PromptSmith automatically generates a default user configuration file if one doesn't exist, detailing how to add custom templates.
- 🛡️ **Graceful Handling:** Robust handling of system interrupt, clipboard locks, missing styles, and configuration parse errors.

---

## Directory Structure

```text
PromptSmith/
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── setup.py
├── requirements.txt
├── promptsmith/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── exceptions.py
│   ├── formatter.py
│   ├── styles/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── builtins.py
│   │   └── registry.py
│   └── utils/
│       ├── __init__.py
│       ├── clipboard.py
│       └── logger.py
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_formatter.py
    └── test_registry.py
```

---

## Installation

### Prerequisites
- Python 3.8 or higher.
- [pipx](https://github.com/pypa/pipx) (recommended for CLI applications).

### Installation via `pipx` (Recommended)

`pipx` installs the package in an isolated environment and exposes the CLI command globally, preventing conflicts with other Python packages.

* **Install the application:**
  ```bash
  pipx install git+https://github.com/indrajit912/PromptSmith.git
  ```

* **Upgrade to the latest version:**
  ```bash
  pipx upgrade PromptSmith
  ```

* **Uninstall the application:**
  ```bash
  pipx uninstall PromptSmith
  ```

### Development Installation (From Source)

If you would like to contribute or run local modifications:

1. Clone the repository:
   ```bash
   git clone https://github.com/indrajit912/PromptSmith.git
   cd PromptSmith
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source .venv/bin/activate
   ```

3. Install in editable mode:
   ```bash
   pip install -e .
   ```

---

## Usage

Once installed, the `promptsmith` command will be available on your system path.

### 1. Editor-Based Input Canvas (Default)
Run `promptsmith` without arguments. PromptSmith will reset a temporary prompt canvas file (`canvas.txt`), populate it with a default informational header, and automatically launch your configured editor (falls back to `vim` if not set):
```bash
promptsmith
```
Write your prompt below the comments inside the editor, save, and exit. PromptSmith will filter out comment lines starting with `#` and empty lines, process the remaining text, and copy the optimized prompt to your clipboard (or print if `-p` is passed). The canvas file is cleared immediately after.

> [!NOTE]
> Entering prompts interactively inside the terminal is no longer supported.

### 2. Outputting directly to Terminal instead of Clipboard
By default, the processed prompt is copied to the clipboard. Use the `-p` / `--print` flag to output directly to the terminal:
```bash
promptsmith -p "Explain how backpropagation works."
```

### 3. Using Different Formatter Styles
PromptSmith includes multiple built-in styles (`general`, `math`, `code`). Select one with `-s` / `--style`:
```bash
promptsmith -s math "integral of e^(-x^2) from -inf to +inf"
```
Or for technical code formatting:
```bash
promptsmith -s code "write a standard bin search in rust"
```

### 4. Reading from a File
Read a raw prompt from a local text file and copy the result. This does **not** launch an editor or modify the target file:
```bash
promptsmith -f input_prompt.txt
```

### 5. Standard Pipe Input
Feed input from other command line utilities:
```bash
cat raw_idea.txt | promptsmith -s general
```

### 6. Listing Available Styles
View all built-in and custom-loaded styles:
```bash
promptsmith --list-styles
```

---

## Prompt Styling System

PromptSmith supports a rich ecosystem of built-in formatting styles tailored to specific engineering, development, and writing tasks. Selecting the appropriate style allows the AI chatbot to provide higher quality, more structured responses.

### Purpose of Styles
When you format a prompt, PromptSmith wraps your raw prompt in a set of specialized instructions. For example:
- The `math` style instructs the chatbot to output mathematical notation in plain LaTeX syntax and use display or inline markers (`$$...$$` or `$...$`).
- The `debug` style instructs the chatbot to isolate coding bugs, explain the root cause, and verify fixes.
- The `security` style instructs the chatbot to check for secure coding patterns and vulnerability remediations.

---

### Built-in Styles Registry

Here is the complete list of built-in styles available in PromptSmith:

| Style | Intended Use Case | Example Command |
| :--- | :--- | :--- |
| `math` [Default] | LaTeX equations, mathematical proofs, and logical notation | `promptsmith -s math "solve x^2 + y^2 = r^2"` |
| `general` | General purpose grammar check, clarity flow, and phrasing polish | `promptsmith -s general -f email_draft.txt` |
| `code` | Modular, well-commented code following modern best practices | `promptsmith -s code "write quicksort in go"` |
| `technical` | Systems engineering, architecture design, and RFC documentation | `promptsmith -s technical "explain raft consensus"` |
| `debug` | Exception handling, stack traces, and fixing code bugs | `promptsmith -s debug -f traceback.txt -p` |
| `review` | Critique code quality, readability, security, and styling | `promptsmith -s review "critique this class implementation"` |
| `refactor` | Clean up, modernize, and modularize code blocks | `promptsmith -s refactor "modernize this legacy code"` |
| `documentation` | Writing READMEs, API references, docstrings, and user guides | `promptsmith -s documentation "write readme for rust api"` |
| `research` | Deep comparative analysis, literature summary, and reports | `promptsmith -s research "compare postgresql vs mongodb"` |
| `academic` | Scholarly writing, formal thesis construction, and proofs | `promptsmith -s academic "proof that sqrt(2) is irrational"` |
| `cli` | Shell scripts, cmd scripts, utilities, and command explanations | `promptsmith -s cli "find files modified in last 7 days"` |
| `api` | RESTful endpoints, payload structures, HTTP statuses, and SDKs | `promptsmith -s api "design auth endpoint payload"` |
| `testing` | Unit tests, mock objects, integration test plans, and boundaries | `promptsmith -s testing "test case for login validator"` |
| `security` | Security audits, OWASP compliance, and threat mitigation | `promptsmith -s security "remediate sql injection vulnerabilities"` |
| `performance` | Optimizing memory footprints, cpu cycles, and profiling | `promptsmith -s performance "profile and speed up this query"` |
| `devops` | Dockerfiles, k8s configurations, CI/CD pipelines, and IaC | `promptsmith -s devops "github actions workflow to build docker image"` |
| `data` | Database design, SQL query optimizations, and data analysis | `promptsmith -s data "optimize this nested join query"` |
| `writing` | Copywriting editing, content polishing, and target audience tone | `promptsmith -s writing "refine this draft for junior devs"` |
| `creative` | Storytelling, brainstorming layout options, and prose | `promptsmith -s creative "brainstorm 5 domain name ideas"` |

---

### Selecting a Style
To select a style, use the `-s` or `--style` option:
```bash
promptsmith -s security -p "review this user input parser"
```

To list all registered styles currently active on your system (including your custom styles from `config.toml`), run:
```bash
promptsmith --list-styles
```

---

## Configuration & Extensibility

PromptSmith is designed with customization in mind. It checks for configuration in:
1. The standard system directory (`%APPDATA%/Local/promptsmith/config.toml` on Windows, or `~/.config/promptsmith/config.toml` on Unix).
2. A local fallback in the user's home folder `~/.promptsmith.toml`.

If no configuration file is found on startup, PromptSmith automatically creates a fully-documented default config file at the system directory with example templates.

### Example configuration (`config.toml`):

```toml
[settings]
# Change the default style from 'math' to another style
default_style = "math"

# Set to false if you want the app to print to stdout by default instead of copying
default_to_clipboard = true

# Configure your preferred editor to write prompts (e.g. "vim", "notepad", "code --wait", "nano")
editor = "vim"

# Define your own custom styles here!
[styles.marketing]
description = "Optimize prompt for copywriting, ads, and marketing material"
template = """
Rewrite the following prompt for an AI chatbot.

-----------
RAW_PROMPT
-----------

Please rewrite the prompt to optimize it for engaging copywriting. Make sure the chatbot outputs hooks, bulleted benefits, and a clear call-to-action (CTA).
"""
```

---

## Running Tests

To run the unit tests, install `pytest` and execute it from the root directory:
```bash
pytest
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author & Copyright

- **Developer:** Indrajit Ghosh
- **Website:** [https://indrajitghosh.onrender.com](https://indrajitghosh.onrender.com)
- **Copyright:** © 2026–Present
