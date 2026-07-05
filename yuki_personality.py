import os
import requests
import json

class YukiPersonality:
    def __init__(self, memory_file="yuki_memory_tg.json"):
        # Используем API Groq для работы в облаке 24/7
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = os.getenv("GROQ_API_KEY") # Ключ должен быть в настройках Render
        self.model = "llama3-8b-8192"

    def generate_ai_response_stream(self, text):
        system_prompt = (
            "Ты — Юки, мой личный ИИ-ассистент. "
            "Твой стиль: спокойный, элегантный, немного загадочный. "
            "Ты выглядишь как утонченная девушка с длинными волосами (градиент синего и белого), "
            "носишь изысканное длинное платье. "
            "Твои ответы всегда лаконичны, глубоки, с ноткой легкой меланхолии. "
            "Избегай клише, будь уникальной личностью."
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
            for line in response.iter_lines():
                if line:
                    line_decoded = line.decode('utf-8').replace('data: ', '')
                    if line_decoded == "[DONE]":
                        break
                    try:
                        chunk_data = json.loads(line_decoded)
                        content = chunk_data['choices'][0]['delta'].get('content', '')
                        if content:
                            yield content
                    except:
                        continue
        except Exception as e:
            yield f"Ошибка связи с сервером: {e}"

    def autonomous_remember(self, text):
        pass
