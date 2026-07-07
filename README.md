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

### 1. Interactive Multi-line Capture (Default)
Run `promptsmith` without arguments. PromptSmith will open an interactive prompt allowing you to type or paste any multi-line raw string. Press `Ctrl+Z` then `Enter` (on Windows) or `Ctrl+D` (on Linux/macOS) on a new line to process it:
```bash
promptsmith
```

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
Read a raw prompt from a local text file and copy the result:
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

## Configuration & Extensibility

PromptSmith is designed with future customization in mind. It checks for configuration in:
1. The standard system directory (`%APPDATA%/Local/promptsmith/config.toml` on Windows, or `~/.config/promptsmith/config.toml` on Unix).
2. A local fallback in the user's home folder `~/.promptsmith.toml`.

If no configuration file is found on startup, PromptSmith automatically creates a fully-documented default config file at the system directory with example templates.

### Example configuration (`config.toml`):

```toml
[settings]
# Change the default style from 'general' to another style
default_style = "general"

# Set to false if you want the app to print to stdout by default instead of copying
default_to_clipboard = true

# Define your own custom styles here!
[styles.marketing]
description = "Optimize prompt for copywriting, ads, and marketing material"
template = """
Rewrite the following prompt for an AI chatbot.

=== RAW PROMPT ===
RAW_PROMPT
==================

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
