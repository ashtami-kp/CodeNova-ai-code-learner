from django.shortcuts import render
from .ai_engine import generate_quiz
from activity.models import Activity
import markdown 

def quiz_view(request):
    if request.method == "POST":
        try:
            topic = request.POST.get("topic")
            difficulty = request.POST.get("difficulty", "medium")
            
            if not topic or topic.strip() == "":
                return render(request, "quizzes/quiz_form.html", {
                    "error": "Please enter a valid topic"
                })
            
            quiz_text = generate_quiz(topic)
            
            if not quiz_text:
                return render(request, "quizzes/quiz_form.html", {
                    "error": "Failed to generate quiz. Please try again."
                })

            # Convert quiz text (Markdown) to HTML
            html_quiz = markdown.markdown(
                quiz_text,
                extensions=["fenced_code", "codehilite", "tables"]
            )

            # Track activity
            if request.user.is_authenticated:
                Activity.objects.create(
                    user=request.user,
                    action="quiz_attempt",
                    description=f"Generated quiz on topic: {topic}"
                )

            return render(request, "quizzes/quiz_result.html", {
                "quiz": html_quiz,
                "topic": topic,
                "difficulty": difficulty
            })
        
        except Exception as e:
            return render(request, "quizzes/quiz_form.html", {
                "error": f"An error occurred: {str(e)}"
            })

    return render(request, "quizzes/quiz_form.html")
