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
