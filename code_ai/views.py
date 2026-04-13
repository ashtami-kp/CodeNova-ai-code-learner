from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from django.shortcuts import render
from django.utils.safestring import mark_safe
from .ai_engine import explain_code, debug_code, convert_code,generate_code
from activity.models import Activity
import markdown
import logging

logger = logging.getLogger(__name__)


# Helper function to format errors as markdown
def format_error_response(error_message):
    """Convert error message to formatted markdown HTML"""
    error_markdown = f"## ⚠️ Error Occurred\n\n```\n{error_message}\n```\n\nPlease try again later or contact support if the issue persists."
    return mark_safe(markdown.markdown(error_markdown, extensions=['fenced_code', 'tables']))


# Helper function to convert response to markdown HTML
def convert_to_html(text):
    """Convert markdown text to safe HTML"""
    try:
        return mark_safe(markdown.markdown(text, extensions=['fenced_code', 'tables']))
    except Exception as e:
        logger.error(f"Error converting markdown: {str(e)}")
        return mark_safe(f"<p>{text}</p>")


# -------------------------------
# Explain Code View
# -------------------------------
def explain_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        if not code or not language:
            return render(request, 'code_ai/explain.html', {'error': 'Please enter code and language'})
        
        try:
            explanation = explain_code(code, language)
            html_result = convert_to_html(explanation)

            # Track activity
            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action="code_explained",
                    description=f"Explained code in {language}"
                )

            return render(request, 'code_ai/result.html', {'result': html_result})
        
        except Exception as e:
            logger.error(f"Error in explain_view: {str(e)}")
            html_result = format_error_response(str(e))
            return render(request, 'code_ai/result.html', {'result': html_result})

    return render(request, 'code_ai/explain.html')


# -------------------------------
# Debug Code View
# -------------------------------
def debug_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        
        if not code or not language:
            error_msg = "Please provide both code and language"
            html_result = format_error_response(error_msg)
            return render(request, 'code_ai/debug_result.html', {'result': html_result})

        try:
            result = debug_code(code, language)
            html_result = convert_to_html(result)

            # Track activity
            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action="code_debugged",
                    description=f"Debugged code in {language}"
                )

        except Exception as e:
            logger.error(f"Error in debug_view: {str(e)}")
            html_result = format_error_response(str(e))

        return render(request, 'code_ai/debug_result.html', {'result': html_result})

    return render(request, 'code_ai/debug.html')


# -------------------------------
# Convert Code View
# -------------------------------
def convert_view(request):
    result = ""
    
    if request.method == "POST":
        code = request.POST.get("code")
        from_lang = request.POST.get("from_lang")
        to_lang = request.POST.get("to_lang")
        
        if not code or not from_lang or not to_lang:
            error_msg = "Please provide code, source language, and target language"
            result = format_error_response(error_msg)
            return render(request, "code_ai/convert.html", {"result": result})

        try:
            converted = convert_code(code, from_lang, to_lang)
            result = convert_to_html(converted)

            # Track activity
            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action="code_converted",
                    description=f"Converted code from {from_lang} to {to_lang}"
                )
        
        except Exception as e:
            logger.error(f"Error in convert_view: {str(e)}")
            result = format_error_response(str(e))

    return render(request, "code_ai/convert.html", {"result": result})
    # --------------------------------------
# Download Result as PDF
# --------------------------------------
def download_pdf_view(request):
    content = request.POST.get("content")

    if not content:
        return HttpResponse("No content to download.")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="codenova_result.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        spaceAfter=10
    )

    # Split content by line and add to PDF
    lines = content.split('\n')
    for line in lines:
        elements.append(Paragraph(line, custom_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return response

# --------------------------------------
# Generate Code from Topic
# --------------------------------------
def generate_view(request):
    result = ""

    if request.method == "POST":
        topic = request.POST.get("topic")
        language = request.POST.get("language")

        if not topic or not language:
            return render(request, "code_ai/generate.html",
                          {"error": "Please enter topic and language"})

        try:
            generated_code = generate_code(topic, language)
            result = convert_to_html(generated_code)

            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action="code_generated",
                    description=f"Generated code for {topic} in {language}"
                )

        except Exception as e:
            result = format_error_response(str(e))

    return render(request, "code_ai/generate.html",
                  {"result": result})


