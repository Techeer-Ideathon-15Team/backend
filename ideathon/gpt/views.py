import json

from django.shortcuts import render
from django.http import JsonResponse
from .models import GptAnswer, Character
from django.conf import settings
import openai
from django.views.decorators.csrf import csrf_exempt


def gpt_answer_list(request):
    answers = GptAnswer.objects.all()
# POST 요청을 처리하는 뷰 함수

# @csrf_exempt
# def send_to_gpt(request):
#     if request.method == 'POST':
#         # 폼 데이터 추출
#         character_name = request.POST.get('character_name')
#         tone = request.POST.get('tone')
#         text_length = request.POST.get('text_length')
#         situation = request.POST.get('situation')
#         language = request.POST.get('language')
#
#
#         print("11111")
#
#         # 캐릭터 정보 생성 및 저장
#         new_character = Character.objects.create(
#             character_name=character_name,
#             tone=tone,
#             text_length=text_length,
#             situation=situation,
#             language=language
#         )
#
#         print("22222")
#
#         # 프롬프트 생성
#         prompt = f"{situation} [Tone: {tone}, Length: {text_length}, Language: {language}]"
#
#         print("33333")
#         # OpenAI GPT 호출
#         response = openai.Completion.create(
#             engine="gpt-4o",
#             prompt=prompt,
#             max_tokens=300,
#             api_key=settings.OPENAI_API_KEY
#         )
#
#         print("44444")
#
#         # 생성된 응답 저장
#         GptAnswer.objects.create(
#             character=new_character,
#             response_content=response['choices'][0]['text'],
#         )
#         print("55555")



@csrf_exempt  # CSRF 검증 비활성화 (테스트 목적으로만 사용)
def send_to_gpt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            character_name = data.get('character_name')
            if not character_name:
                return JsonResponse({'error': 'Character name is required'}, status=400)

            # 기타 필드도 동일하게 처리
            tone = data.get('tone')
            text_length = data.get('text_length')
            situation = data.get('situation')
            language = data.get('language')

            # 데이터베이스 객체 생성
            new_character = Character.objects.create(
                character_name=character_name,
                tone=tone,
                text_length=text_length,
                situation=situation,
                language=language
            )

            # 프롬프트 생성
            prompt = f"{situation} [Tone: {tone}, Length: {text_length}, Language: {language}]"
            # OpenAI GPT 호출
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "GPT-3.5 사용자와 대화를 시작합니다."},
                          {"role": "user", "content": prompt}],
                api_key=settings.OPENAI_API_KEY
            )

            msg = response['choices'][0]['message']['content']

            # 생성된 응답 저장
            GptAnswer.objects.create(
                character=new_character,
                response_content=msg,
            )

            return JsonResponse({'message': 'Character created successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)