import google.generativeai as genai
import os
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# Gemini Configuration
# -----------------------------
try:
    API_KEY = os.getenv("GEMINI_API_KEY")

    if not API_KEY:
        raise ValueError("GEMINI_API_KEY environment variable is not set")

    genai.configure(api_key=API_KEY)

    # Use a valid model
    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    logger.info("Gemini API configured successfully")

except Exception as e:
    logger.error(f"Failed to configure Gemini API: {e}")
    model = None


# -----------------------------
# Explain Code
# -----------------------------
def explain_code(code: str, language: str) -> str:
    if not model:
        raise ValueError("AI service is not properly configured")

    try:
        prompt = f"""
        Explain the following {language} code in simple terms:

        {code}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error = str(e)
        logger.error(f"Error explaining code: {error}")

        if "429" in error or "quota" in error.lower():
            raise ValueError("API quota limit reached. Please try again later.")

        raise ValueError("Failed to explain code. Please try again later.")


# -----------------------------
# Debug Code
# -----------------------------
def debug_code(code: str, language: str) -> str:
    if not model:
        raise ValueError("AI service is not properly configured")

    try:
        prompt = f"""
        Debug the following {language} code and explain the errors clearly:

        {code}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error = str(e)
        logger.error(f"Error debugging code: {error}")

        if "429" in error or "quota" in error.lower():
            raise ValueError("API quota limit reached. Please try again later.")

        raise ValueError("Failed to debug code. Please try again later.")


# -----------------------------
# Convert Code
# -----------------------------
def convert_code(code: str, from_lang: str, to_lang: str) -> str:
    if not model:
        raise ValueError("AI service is not properly configured")

    try:
        prompt = f"""
        Convert the following {from_lang} code to {to_lang}.
        Maintain the same logic and add helpful comments.

        {code}
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error = str(e)
        logger.error(f"Error converting code: {error}")

        if "429" in error or "quota" in error.lower():
            raise ValueError("API quota limit reached. Please try again later.")

        raise ValueError("Failed to convert code. Please try again later.")


def generate_code(topic: str, language: str) -> str:
    if not model:
        raise ValueError("AI service is not properly configured")

    try:
        prompt = f"""
        You are an expert {language} programmer.

        Generate complete, working, beginner-friendly source code for:

        Topic: {topic}

        Rules:
        - Only return source code
        - Include comments
        - No explanation
        - No markdown
        - No backticks
        """

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_str = str(e)
        logger.error(f"Error generating code: {error_str}")

        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            raise ValueError("API quota limit reached. Please try again tomorrow or upgrade your API plan.")

        raise ValueError("Failed to generate code. Please try again later.")
