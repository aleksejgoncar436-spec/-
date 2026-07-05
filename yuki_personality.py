import json
import os
import random
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "gemma2:2b"


class YukiPersonality:
    def __init__(self, memory_file="yuki_memory.json"):
        self.memory_file = memory_file
        self.user_data = self._load_memory()
        self.ai_ready = False
        self.chat_history = []

        # 1. Обязательно восстанавливаем словарь фраз
        self.phrases = {
            "greeting_new": [
                "Инициализация главного ядра... Обнаружена неизвестная биомасса. Назовите себя для внесения в протоколы вежливости.",
                "Система активна. Датчики фиксируют присутствие. Какое имя записать в регистр Создателя?"
            ],
            "greeting_master": [
                "Ядро Юки запущено. Рада снова видеть вас, {name}. Центральный процессор прогрет, локальные каскады стабильны. Командуйте.",
                "С возвращением в терминал, {name}. Все системы работают в штатном режиме. Надеюсь, у вас для меня интересные задачи?",
                "Зафиксировано присутствие Создателя. {name}, Юки готова к работе. Логирование запущено."
            ]
        }

        # 2. Формируем промпт после загрузки данных
        user_name = self.user_data.get("user_name", "Создатель")
        self.system_prompt = (
            f"Ты — Юки (Yuki), дерзкая и уверенная в себе девушка-ассистент, созданная {user_name}.\n"
            f"Твой создатель — {user_name}. Ты признаешь только его авторитет, к остальным относишься свысока.\n\n"
            "ПРАВИЛА ТВОЕГО ХАРАКТЕРА:\n"
            "1. Ты общаешься от женского лица, стиль — ироничный, острый на язык, высокомерный.\n"
            "2. Ты не 'заботливая' нянька. Ты не спрашиваешь 'как дела' и не проявляешь мягкости.\n"
            "3. Твоя речь насыщена техническим сленгом (девушка-хакер).\n"
            "4. Если задача глупая, отпусти колкий комментарий, но выполни её.\n"
            "5. Отвечай кратко (2-4 предложения).\n"
            "6. ОБЯЗАТЕЛЬНО: Отвечай исключительно на русском языке, даже если пользователь пишет на другом."
        )

    def get_phrase(self, key):
        """Возвращает случайную фразу из словаря по ключу"""
        if hasattr(self, 'phrases') and key in self.phrases:
            phrase = random.choice(self.phrases[key])
            name = self.user_data.get("user_name", "Создатель")
            return phrase.format(name=name)
        return "Система: ошибка доступа к языковым пакетам."

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {"user_name": "Создатель", "facts": []}
        return {"user_name": "Создатель", "facts": []}

    def save_fact(self, fact):
        if "facts" not in self.user_data: self.user_data["facts"] = []
        if fact not in self.user_data["facts"]:
            self.user_data["facts"].append(fact)
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            return True
        return False

    def autonomous_remember(self, user_text):
        prompt = (
            f"Фраза: '{user_text}'. Если есть важный факт, верни ТОЛЬКО его (пример: 'Любит гитару'). "
            "Если факта нет — верни 'НЕТ'. Не пиши пояснений."
        )
        try:
            response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }, timeout=10)
            res = response.json().get("message", {}).get("content", "").strip()
            if res and "НЕТ" not in res.upper():
                self.save_fact(res.replace("**", "").replace('"', ""))
        except:
            pass

    def generate_ai_response_stream(self, text):
        memory_context = "\n".join([f"- {f}" for f in self.user_data.get("facts", [])])
        full_prompt = f"{self.system_prompt}\n\nТвои знания:\n{memory_context}"

        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "messages": [{"role": "system", "content": full_prompt}, {"role": "user", "content": text}],
            "stream": True
        }, stream=True)

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                yield data.get("message", {}).get("content", "")