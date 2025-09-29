"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyDwNMPZl7J-Wl-pKYM2N92-TsYTvE_X93k")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [ """GPT-3.5와 GPT-4의 차이에 대해 더 알려주세요. 

1. 이해력

GPT-3.5: 복잡한 문제나 추상적인 개념을 이해하는 데 한계가 있을 수 있습니다.
GPT-4: 더 깊은 이해력을 가지고 있어, 복잡한 질문이나 추상적인 개념에 대해 더 잘 대응할 수 있습니다.
2. 최신 정보 습득 가능성

GPT-3.5: 출시 당시 학습한 데이터를 기반으로 정보를 제공하기 때문에, 최신 정보에는 다소 뒤떨어질 수 있습니다.
GPT-4: 더 최근에 학습된 데이터를 기반으로 하기 때문에 최신 정보를 반영하는 데 더 유리합니다.
3. 정확도

GPT-3.5: 좋은 정확도를 제공하지만, 복잡하거나 전문적인 주제에 대해서는 오류를 범할 수 있습니다.
GPT-4: 보다 향상된 정확도를 제공합니다. 더 많은 데이터와 개선된 알고리즘 덕분에 더 정확한 정보를 제공할 수 있습니다.
4. 창의성

GPT-3.5: 창의적인 콘텐츠를 생성할 수 있지만, 때로는 예측 가능하거나 반복적인 패턴을 보일 수 있습니다.
GPT-4: 더 발전된 학습 능력 덕분에 창의적이고 다양한 콘텐츠를 생성할 수 있습니다. 이는 영상 대본 작성 등의 창의적 작업에 유용합니다.
5. 생성 속도


GPT-3.5: 상대적으로 빠른 생성 속도를 자랑하지만, 때때로 복잡한 요청에는 시간이 더 걸릴 수 있습니다.
GPT-4: 더 큰 모델이기 때문에 약간 느릴 수 있지만, 이는 더 정교한 응답을 위한 시간이 필요하기 때문입니다.
                
                 위의 글은 타인이 작성한 블로그 글이다. 이 글에 댓글을 생성하려고 한다. 친절하고 정중한 표현으로 블로그에 내가 직접 만든 댓글을 한글 10자~30자 이내로, 한국어로 자연스러운 말로  주제에 어울리는 댓글로 자연스럽게 만들어줘. 최대한 위의 주제를 잘 읽어서 도움이 되었고, 감사하는 말투로 말이지. 자연스럽게 '..니다'라는 말보다는 '...요'라는 식으로 부탁해. '블로그 댓글'이란 단어는 절대 안들어가게 작성해줘. 정중하면서 자연스러운 글에 대한 감상을 전해주세요.'댓글'이란 단어는 금지한다.  글자수를 꼭 지켜서 작성해줘. 한글 50자 이내로 생성해줘."""
]

response = model.generate_content(prompt_parts)
print(response.text)