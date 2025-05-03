import json
from pathlib import Path
from utils.logger import get_logger

def run_orchestration():
    logger = get_logger("Orchestrator")

    with open("config/flow.json") as f:
        flow = json.load(f)

    from agents.agent import Agent

    agents = {}
    for agent_name in flow:
        prompt_path = f"prompts/{agent_name}.txt"
        agents[agent_name] = Agent(agent_name, config={"prompt_path": prompt_path})

    initial_agent = list(flow.keys())[0]
    repo_folder = Path("repository")
    repo_folder.mkdir(exist_ok=True)

    for file_path in repo_folder.glob("*.*"):
        input_file_name = file_path.stem
        logger.info(f"\n=== Processing input file: {file_path.name} ===")
        output_subfolder = Path("output") / input_file_name
        output_subfolder.mkdir(parents=True, exist_ok=True)

        def execute(agent_name, input_path, previous_output=None):
            logger.info(f"Executing {agent_name} on {input_path}...")
            agent = agents[agent_name]
            output_path = output_subfolder / f"{agent_name}.txt"
            agent.run(input_path, output_path, previous_output)
            with open(output_path, 'r') as f:
                current_output = f.read()
            for next_agent in flow.get(agent_name, []):
                execute(next_agent, output_path, current_output)

        execute(initial_agent, file_path)
