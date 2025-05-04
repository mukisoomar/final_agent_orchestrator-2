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

    def load_user_prompt_template(self, template_path, context_vars):
        self.logger.info(f"Loading user prompt template: {template_path}")
        if not Path(template_path).exists():
            return ""
        template = Path(template_path).read_text()
        try:
            return template.format(**context_vars)
        except KeyError as e:
            self.logger.error(f"Missing placeholder key: {e}")
            return template

    def run(self, input_path, output_path, previous_outputs=None):
        self.logger.info(f"Running agent {self.name}...")

<<<<<<< HEAD
        system_prompt_path = Path(f"prompts/{self.name}/system.txt")
        system_prompt = system_prompt_path.read_text() if system_prompt_path.exists() else "You are a helpful assistant."

        user_template_path = Path(f"prompts/{self.name}/user_template.txt")
        context_vars = previous_outputs if previous_outputs else {}
=======
        # Load system prompt
        system_prompt_path = Path(f"prompts/{self.name}/system.txt")
        system_prompt = system_prompt_path.read_text() if system_prompt_path.exists() else "You are a helpful assistant."

        # Prepare user prompt
        user_template_path = Path(f"prompts/{self.name}/user_template.txt")
        context_vars = {}
        if previous_outputs:
            for idx, val in enumerate(previous_outputs):
                context_vars[f"previous_{idx+1}"] = val.strip()
>>>>>>> refs/remotes/origin/main
        user_prompt = self.load_user_prompt_template(user_template_path, context_vars)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            self.logger.info(f"Sending request to LLM for {self.name}")
            output = self.llm.chat(messages)
        except Exception as e:
            self.logger.error(f"{self.name} LLM call failed: {e}")
            output = f"[ERROR from {self.name}: {str(e)}]"

        self.logger.info(f"Writing output to {output_path}")
        with open(output_path, 'w') as f:
            f.write(output)
