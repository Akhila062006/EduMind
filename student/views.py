
import os
from groq import Groq

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Home page
def home(request):
    return render(request, 'student/home.html')


# Student registration
def register(request):
    error = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = "Please check your username and password."

    return render(request, 'student/register.html', {
        'error': error
    })


# Student dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'student/dashboard.html')


# AI Tutor
@login_required(login_url='login')
def ai_tutor(request):
    answer = None
    error = None
    question = ""

    if request.method == 'POST':
        question = request.POST.get('question', '').strip()

        if not question:
            error = "Please enter a question."

        elif not os.environ.get('GROQ_API_KEY'):
            error = "AI API key is missing. We need to configure it."

        else:
            try:
                client = Groq(
                    api_key=os.environ.get('GROQ_API_KEY')
                )

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are EduMind AI Tutor. Teach students using simple English, clear explanations, examples and step-by-step guidance."
                        },
                        {
                            "role": "user",
                            "content": question
                        }
                    ]
                )

                answer = response.choices[0].message.content

            except Exception as e:
                print("GROQ ERROR:", str(e))
                error = "AI service is temporarily unavailable. Please try again later."

    return render(request, 'student/ai_tutor.html', {
        'question': question,
        'answer': answer,
        'error': error
    })


# Topic Explainer
@login_required(login_url='login')
def topic_explainer(request):
    explanation = None
    error = None
    topic = ""

    if request.method == 'POST':
        topic = request.POST.get('topic', '').strip()

        if not topic:
            error = "Please enter a topic."

        elif not os.environ.get('GROQ_API_KEY'):
            error = "AI API key is missing. We need to configure it."

        else:
            try:
                client = Groq(
                    api_key=os.environ.get('GROQ_API_KEY')
                )

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are EduMind Topic Explainer. Explain topics in simple English with a definition, important points, examples and a short summary."
                        },
                        {
                            "role": "user",
                            "content": f"Explain this topic: {topic}"
                        }
                    ]
                )

                explanation = response.choices[0].message.content

            except Exception as e:
                print("TOPIC EXPLAINER ERROR:", str(e))
                error = "AI service is temporarily unavailable. Please try again later."

    return render(request, 'student/topic_explainer.html', {
        'topic': topic,
        'explanation': explanation,
        'error': error
    })
