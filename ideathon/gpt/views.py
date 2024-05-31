# gpt/views.py
from django.shortcuts import render
from .models import GptAnswer, Character

def gpt_answer_list(request):
    
    answers = GptAnswer.objects.all()
    
    return render(request, 'gpt/answer_list.html', {'answers': answers})

def send_to_gpt(request):
    if request.method == 'POST':
       
        character_name = request.POST.get('character_name')
        tone = request.POST.get('tone')
        text_length = request.POST.get('text_length')
        situation = request.POST.get('situation')
        language = request.POST.get('language')
        
        
        new_character = Character.objects.create(
            character_name=character_name,
            tone=tone,
            text_length=text_length,
            situation=situation,
            language=language
        )

        
        return render(request, 'gpt/send_to_gpt.html', {'new_character': new_character})

    return render(request, 'gpt/send_to_gpt_form.html')
