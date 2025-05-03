from agents.base_agent import BaseAgent
from pathlib import Path
import openai
import os

class Agent(BaseAgent):
    def run(self, input_path, output_path, previous_output=None):
        # Load system prompt
        prompt_path = Path(self.config.get("prompt_path", "prompts/default.txt"))
        system_prompt = prompt_path.read_text() if prompt_path.exists() else "You are a helpful assistant."

        # Load user input
        with open(input_path, 'r') as f:
            user_input = f.read()

        # Prepare messages for OpenAI Chat API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        if previous_output:
            messages.append({"role": "assistant", "content": previous_output})

        # Make the API call to OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        model = self.config.get("model", "gpt-4")

        try:
            self.logger.info(f"Calling OpenAI API for {self.name}")
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.3,
                max_tokens=1024
            )
            output = response.choices[0].message["content"]
        except Exception as e:
            self.logger.error(f"OpenAI API call failed for {self.name}: {e}")
            output = f"[ERROR from {self.name}: {str(e)}]"

        # Save output
        with open(output_path, 'w') as f:
            f.write(output)
