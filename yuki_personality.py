import os
import requests
import json

class YukiPersonality:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("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")
        self.model = "llama3-8b-8192"

    def generate_ai_response_stream(self, text):
        # Характер Юки
        system_prompt = (
            "Ты — Юки, мой личный ИИ-ассистент. "
            "Твой стиль: спокойный, элегантный, немного загадочный. "
            "Ты — утонченная девушка с длинными волосами (градиент синего и белого), "
            "носишь изысканное длинное платье. "
            "Твои ответы лаконичны, глубоки, с ноткой легкой меланхолии. "
            "Избегай шаблонных фраз ИИ. Будь уникальной личностью."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            "stream": True
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, stream=True)
            if response.status_code != 200:
                yield f"Ошибка доступа к облаку (код {response.status_code})."
                return

            full_text = ""
            for line in response.iter_lines():
                if line:
                    line_decoded = line.decode('utf-8').replace('data: ', '')
                    if line_decoded == "[DONE]": break
                    try:
                        chunk_data = json.loads(line_decoded)
                        content = chunk_data['choices'][0]['delta'].get('content', '')
                        if content:
                            full_text += content
                            yield content
                    except: continue
            
            if not full_text:
                yield "Юки задумалась и не нашла слов."
                
        except Exception as e:
            yield f"Техническая ошибка: {str(e)}"
