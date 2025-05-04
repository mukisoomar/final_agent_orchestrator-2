import os
<<<<<<< HEAD
=======
import google.generativeai as genai
>>>>>>> refs/remotes/origin/main
from openai import OpenAI
from utils.logger import get_logger

logger = get_logger("LLM")

class LLMService:
    def __init__(self, model_config):
        self.provider = model_config.get("provider", "openai").lower()
        self.model = model_config.get("model", "gpt-4")
        self.temperature = model_config.get("temperature", 0.7)
        self.top_p = model_config.get("top_p", 1.0)
        self.n = model_config.get("n", 1)
        self.stop = model_config.get("stop", None)
        self.max_tokens = model_config.get("max_tokens", 1024)
        self.presence_penalty = model_config.get("presence_penalty", 0.0)
        self.frequency_penalty = model_config.get("frequency_penalty", 0.0)
        self.logit_bias = model_config.get("logit_bias", None)
        self.user = model_config.get("user", None)

        if self.provider == "openai":
<<<<<<< HEAD
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            self.client = OpenAI(api_key=api_key)
=======
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
>>>>>>> refs/remotes/origin/main
        elif self.provider == "gemini":
            gemini_key = os.getenv("GEMINI_API_NEOTEK_KEY")
            if not gemini_key:
                raise ValueError("GEMINI_API_NEOTEK_KEY environment variable not set.")
            self.client = OpenAI(
                api_key=gemini_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def chat(self, messages):
<<<<<<< HEAD
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            n=self.n,
            stop=self.stop,
            max_tokens=self.max_tokens,
            presence_penalty=self.presence_penalty,
            frequency_penalty=self.frequency_penalty,
            logit_bias=self.logit_bias,
            user=self.user
        )

        usage = response.usage
        logger.info(f"{self.provider.capitalize()} usage: prompt={usage.prompt_tokens}, "
                    f"completion={usage.completion_tokens}, total={usage.total_tokens}")
        return response
=======
        if self.provider == "openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            usage = response.usage
            logger.info(f"OpenAI usage: prompt={usage.prompt_tokens}, "
                        f"completion={usage.completion_tokens}, total={usage.total_tokens}")
            return response.choices[0].message.content
        elif self.provider == "gemini":
            prompt_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
            response = self.gemini_model.generate_content(prompt_text)
            token_usage = response._raw_response.usage_metadata
            logger.info(f"Gemini usage: prompt={token_usage.prompt_token_count}, "
                        f"completion={token_usage.candidates_token_count}, "
                        f"total={token_usage.total_token_count}")
            return response.text
>>>>>>> refs/remotes/origin/main
