from agents.base_agent import BaseAgent
from pathlib import Path
import json
from utils.llm_interface import LLMService

class Agent(BaseAgent):
    def __init__(self, name, config):
        super().__init__(name, config)
        self.logger.info(f"Initializing Agent: {name}")
        self.model_config = self.load_model_config(name)
        self.llm = LLMService(self.model_config)

    def load_model_config(self, agent_name):
        self.logger.info(f"Loading model config for {agent_name}")
        with open("config/default_model_config.json") as f:
            default_config = json.load(f)
        with open("config/agent_config.json") as f:
            overrides = json.load(f).get(agent_name, {})
        return {**default_config, **overrides}

    def run(self, input_path, output_path, previous_output=None):
        self.logger.info(f"Running agent {self.name}...")
        prompt_path = Path(self.config.get("prompt_path", "prompts/default.txt"))
        self.logger.info(f"Loading system prompt from {prompt_path}")
        system_prompt = prompt_path.read_text() if prompt_path.exists() else "You are a helpful assistant."

        self.logger.info(f"Reading input from {input_path}")
        with open(input_path, 'r') as f:
            user_input = f.read()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        if previous_output:
            messages.append({"role": "assistant", "content": previous_output})
            self.logger.info("Previous output included in message chain")

        try:
            self.logger.info(f"Sending request to LLM for {self.name}")
            output = self.llm.chat(messages)
        except Exception as e:
            self.logger.error(f"{self.name} LLM call failed: {e}")
            output = f"[ERROR from {self.name}: {str(e)}]"

        self.logger.info(f"Writing output to {output_path}")
        with open(output_path, 'w') as f:
            f.write(output)
