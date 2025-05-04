import os
import openai
import google.generativeai as genai
from utils.logger import get_logger

logger = get_logger("LLM")

class LLMService:
    def __init__(self, model_config):
        self.provider = model_config.get("provider", "openai").lower()
        self.model = model_config.get("model", "gpt-4")
        self.temperature = model_config.get("temperature", 0.3)
        self.max_tokens = model_config.get("max_tokens", 1024)

        if self.provider == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
        elif self.provider == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.gemini_model = genai.GenerativeModel(self.model)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def chat(self, messages):
        if self.provider == "openai":
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            usage = response["usage"]
            logger.info(f"OpenAI usage: prompt={usage['prompt_tokens']}, "
                        f"completion={usage['completion_tokens']}, total={usage['total_tokens']}")
            return response["choices"][0]["message"]["content"]
        elif self.provider == "gemini":
            prompt_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
            response = self.gemini_model.generate_content(prompt_text)
            token_usage = response._raw_response.usage_metadata
            logger.info(f"Gemini usage: prompt={token_usage.prompt_token_count}, "
                        f"completion={token_usage.candidates_token_count}, "
                        f"total={token_usage.total_token_count}")
            return response.text
