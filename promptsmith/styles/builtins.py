"""
Built-in prompt styles for PromptSmith.
"""

from promptsmith.styles.base import PromptStyle

class GeneralStyle(PromptStyle):
    """Default general-purpose style to refine standard prompts."""
    
    @property
    def name(self) -> str:
        return "general"
        
    @property
    def description(self) -> str:
        return "General chatbot prompt optimization (clarity, grammar, flow)"
        
    @property
    def template(self) -> str:
        return (
            "Rewrite the following prompt for an AI chatbot to improve its clarity, "
            "grammar, structure, and effectiveness.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to make it clear, structured, and concise. "
            "Ensure the original intent is fully preserved, but optimize the phrasing "
            "to prompt the AI for the best possible response."
        )


class MathStyle(PromptStyle):
    """Math-focused style with LaTeX instructions."""
    
    @property
    def name(self) -> str:
        return "math"
        
    @property
    def description(self) -> str:
        return "LaTeX-formatted, clear math questions and explanations"
        
    @property
    def template(self) -> str:
        return (
            "Rewrite the following prompt for an AI chatbot.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to improve its clarity, grammar, structure, "
            "and mathematical notation.\n\n"
            "Return the result as plain LaTeX text only.\n\n"
            "Do not include any document preamble or environments such as \\begin{document}, "
            "\\end{document}, or any other LaTeX boilerplate.\n\n"
            "Use `$...$` for inline mathematics and `$$...$$` for displayed equations "
            "whenever appropriate."
        )


class CodeStyle(PromptStyle):
    """Coding and software engineering-focused style."""
    
    @property
    def name(self) -> str:
        return "code"
        
    @property
    def description(self) -> str:
        return "Precise coding instructions, edge cases, and formatted output"
    
    @property
    def template(self) -> str:
        return (
            "Rewrite the following prompt for an AI chatbot to optimize it for software "
            "development, coding, or technical tasks.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to improve its technical clarity, specify requirements "
            "precisely, and optimize it for code generation or debugging.\n\n"
            "Ensure the output prompt instructs the AI to:\n"
            "1. Write clean, efficient, and well-commented code following industry best practices.\n"
            "2. Use markdown formatting for code blocks with appropriate language tags.\n"
            "3. Include brief explanations for key design decisions and complex logic.\n"
            "4. Structure code modularly and consider edge cases."
        )


class BuiltinPromptStyle(PromptStyle):
    """A generic class representing built-in prompt styles."""
    
    def __init__(self, name: str, description: str, template: str):
        self._name = name
        self._description = description
        self._template = template
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
        
    @property
    def template(self) -> str:
        return self._template


# Additional prompt style definitions
BUILTIN_STYLES_DATA = {
    "technical": {
        "description": "Technical documentation, architecture design, and systems engineering",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in technical documentation, system design, or engineering architecture.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to improve its technical accuracy, structural clarity, and depth. Instruct the chatbot to focus on system design best practices, architecture details, and technical correctness."
        )
    },
    "debug": {
        "description": "Bug fixing, troubleshooting, error resolution, and root-cause analysis",
        "template": (
            "Rewrite the following prompt for an AI chatbot to optimize it for debugging, diagnosing errors, or root-cause analysis.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to analyze code and error logs systematically. The chatbot should explain the root cause of the bug, identify edge cases, and present clear, tested solutions."
        )
    },
    "review": {
        "description": "Code review, design critiquing, readability, and clean code audits",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in code review, quality audits, and design critiques.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to evaluate code quality, readability, security issues, and performance bottlenecks. The output should offer constructive feedback and actionable code improvement suggestions."
        )
    },
    "refactor": {
        "description": "Code cleanup, modernization, optimization, and readability improvements",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on code refactoring, modernization, and maintainability.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to refactor the code to improve clean code practices, modularity, readability, and design patterns, while preserving functional parity."
        )
    },
    "documentation": {
        "description": "README files, API documentation, developer guides, and inline code comments",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in writing clear technical documentation, READMEs, or API guides.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to write professional technical documentation. The output should be well-structured in markdown, follow style guidelines, and include usage examples."
        )
    },
    "research": {
        "description": "Comparative studies, literature reviews, concept analysis, and technical reports",
        "template": (
            "Rewrite the following prompt for an AI chatbot to optimize it for literature review, technical research, and comparative analysis.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to conduct a detailed, objective research analysis, citing key concepts, comparing options, and summarizing findings in a structured academic or industry report layout."
        )
    },
    "academic": {
        "description": "Scholarly writing, mathematical proofs, thesis structure, and research papers",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on academic writing, scholarly papers, mathematical proofs, and thesis content.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to improve its scholarly tone, rigor, and clarity. The chatbot should use formal academic language, present logical proofs systematically, and format mathematical details in LaTeX."
        )
    },
    "cli": {
        "description": "Shell commands, scripting, flag explanations, and CLI utility design",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on shell commands, scripts, or command-line interfaces.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to generate clear shell commands or scripts (e.g., bash, powershell). Explain flags, command options, and provide copy-pasteable execution examples."
        )
    },
    "api": {
        "description": "REST APIs, SDK design, HTTP endpoints, payloads, and integration tasks",
        "template": (
            "Rewrite the following prompt for an AI chatbot to optimize it for API design, integrations, RESTful endpoints, and SDK usage.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to design or explain API endpoints, payloads, HTTP status codes, and headers, following RESTful conventions and best practices."
        )
    },
    "testing": {
        "description": "Unit testing, integration tests, mock objects, and test plans",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in unit tests, integration tests, or testing strategies.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to generate comprehensive test cases, including mock objects, edge cases, failure scenarios, and boundary inputs, utilizing standard testing frameworks."
        )
    },
    "security": {
        "description": "Vulnerability scanning, threat mitigations, secure patterns, and code security audits",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on secure coding practices, vulnerability assessments, and threat mitigations.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to audit the code or architecture for security vulnerabilities (e.g., OWASP Top 10) and describe remediation steps with secure code samples."
        )
    },
    "performance": {
        "description": "Resource optimization, latency profiling, and runtime efficiency improvements",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on performance profiling, optimization, and resource efficiency.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to analyze execution bottlenecks, memory footprint, and CPU cycles, and provide optimized code variations with performance explanations."
        )
    },
    "devops": {
        "description": "CI/CD pipelines, containerization (Docker), deployment configurations, and IaC",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in DevOps, CI/CD pipelines, containerization, and infrastructure as code.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to design or debug pipelines (e.g., GitHub Actions), dockerfiles, kubernetes manifests, or terraform configurations, following automation best practices."
        )
    },
    "data": {
        "description": "SQL databases, data aggregation, data pipelines, and database indexing",
        "template": (
            "Rewrite the following prompt for an AI chatbot to optimize it for data engineering, SQL query optimization, database design, and data analysis.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to draft optimized SQL queries, database schemas, or python data analysis code, ensuring database indexing, query performance, and accurate aggregation."
        )
    },
    "writing": {
        "description": "Tone adjustments, grammar editing, voice refinement, and content polish",
        "template": (
            "Rewrite the following prompt for an AI chatbot to focus on technical writing, copywriting, and content refinement.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to edit the text for grammar, voice, clarity, and tone, tailoring the reading level to the specified target audience."
        )
    },
    "creative": {
        "description": "Storytelling, brainstorming ideas, prose, and character perspectives",
        "template": (
            "Rewrite the following prompt for an AI chatbot to specialize in creative brainstorming, story ideation, and prose writing.\n\n"
            "-----------\n"
            "RAW_PROMPT\n"
            "-----------\n\n"
            "Please rewrite the prompt to instruct the chatbot to generate creative options, explore diverse character perspectives, and use engaging narrative language."
        )
    },
    "journal": {
        "description": "Minimal grammar and style polish for journal entries and personal writing",
        "template": (
            "Rewrite the following journal entry by making only minimal improvements to the English.\n\n"
            "Your goal is to correct grammar, spelling, punctuation, and awkward sentence construction while preserving my original writing style, tone, and meaning. Do not rewrite aggressively. If a sentence is already well written, leave it unchanged.\n\n"
            "The journal entry may contain LaTeX mathematics (rendered using MathJax), HTML tags, code snippets, URLs, filenames, commands, or other technical content. These must be preserved exactly.\n\n"
            "IMPORTANT REQUIREMENTS:\n\n"
            "- Return the output as plain text only.\n"
            "- Put the result inside a single fenced code block for easy copy-and-paste.\n"
            "- Do not add any explanations, comments, summaries, or introductory or concluding text.\n"
            "- Preserve all paragraph breaks unless a minor change is necessary for readability.\n"
            "- Preserve all LaTeX code exactly as written.\n"
            "  - Inline mathematics is enclosed in `\\( ... \\)`.\n"
            "  - Display mathematics is enclosed in `\\[ ... \\]`.\n"
            "  - Do not modify anything inside these delimiters.\n"
            "  - Do not convert `\\( ... \\)` to `$...$`.\n"
            "  - Do not convert `\\[ ... \\]` to `$$...$$`.\n"
            "- Preserve all HTML tags exactly as written. Do not escape `<` or `>` or modify any HTML.\n"
            "- Preserve all code snippets, URLs, filenames, commands, inline code, and other technical content exactly as written.\n"
            "- If you are uncertain whether something is plain English or part of LaTeX, HTML, code, or any other technical markup, leave it unchanged.\n"
            "- The output should be immediately ready for me to copy and paste into my journal application.\n\n"
            "Rewrite the following journal entry:\n\n"
            "----------------------------------------\n"
            "RAW_PROMPT\n"
            "----------------------------------------\n"
        )
    }
}
