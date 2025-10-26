from typing import Dict
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from config import Config
from bash import Bash

class ExecOnConfirm:
    """
    A wrapper around the Bash tool that asks for user confirmation before executing any command.
    """

    def __init__(self, bash: Bash):
        self.bash = bash

    def _confirm_execution(self, cmd: str) -> bool:
        """Ask the user whether the suggested command should be executed."""
        return input(f"    ▶️   Execute '{cmd}'? [y/N]: ").strip().lower() == "y"

    @tool
    def exec_bash_command(self, cmd: str) -> str:
        """Execute a bash command after confirming with the user."""
        if self._confirm_execution(cmd):
            result = self.bash.exec_bash_command(cmd)
            return str(result)
        return "The user declined the execution of this command."

def main(config: Config):
    # Create the client
    llm = ChatOpenAI(
        model=config.llm_model_name,
        openai_api_base=config.llm_base_url,
        openai_api_key=config.llm_api_key,
        temperature=config.llm_temperature,
        top_p=config.llm_top_p,
    )
    
    # Create the tool
    bash = Bash(config)
    exec_tool = ExecOnConfirm(bash)
    tools = [exec_tool.exec_bash_command]
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", config.system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    # Create agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Create memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Create agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)
    
    print("[INFO] Type 'quit' at any time to exit the agent loop.\n")

    # The main loop
    while True:
        user = input(f"['{bash.cwd}' 🙂] ").strip()

        if user.lower() == "quit":
            print("\n[🤖] Shutting down. Bye!\n")
            break
        if not user:
            continue

        # Always tell the agent where the current working directory is to avoid confusions.
        user += f"\n Current working directory: `{bash.cwd}`"
        print("\n[🤖] Thinking...")

        try:
            # Run the agent's logic and get the response.
            result = agent_executor.invoke({"input": user})
            
            # Show the response (without the thinking part, if any)
            response = result["output"].strip()

            if "</think>" in response:
                response = response.split("</think>")[-1].strip()

            if response:
                print(response)
                print("-" * 80 + "\n")
        except Exception as e:
            print(f"Error: {e}")
            print("-" * 80 + "\n")

if __name__ == "__main__":
    # Load the configuration
    config = Config()
    main(config)
