import google.genai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    client = None


def generate_quiz(topic):
    """Generate quiz questions using Gemini API with error handling."""
    if not client:
        logger.error("Gemini client not configured")
        raise ValueError("AI service is not properly configured. Please try again later.")
    
    if not topic or not isinstance(topic, str) or len(topic.strip()) == 0:
        raise ValueError("Topic cannot be empty.")
    
    try:
        prompt = f"""
        Generate 5 MCQ questions on {topic} for beginners.
        Each question should have 4 options and indicate the correct answer.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if not response or not response.text:
            logger.error(f"Empty response from API for topic: {topic}")
            raise ValueError("Failed to generate quiz content. Please try again.")
        
        return response.text
    
    except Exception as e:
        error_str = str(e)
        logger.error(f"Error generating quiz for '{topic}': {error_str}")
        
        # Handle quota exceeded (429 error)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            raise ValueError("Quiz generation limit reached for today. Please try again tomorrow or upgrade your API plan.")
        
        # Handle other API errors
        if "APIError" in str(type(e).__name__) or "API" in error_str:
            raise ValueError("API service is temporarily unavailable. Please try again later.")
        
        raise ValueError(f"An unexpected error occurred: {str(e)}")
