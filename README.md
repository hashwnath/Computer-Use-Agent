# NVIDIA Nemotron Bash Computer Use Agent

A bash computer use agent powered by NVIDIA Nemotron Nano 9B v2 that can execute shell commands with user confirmation.

## Features

- Execute bash commands with user confirmation
- Safe command filtering (only allows specific commands)
- Conversation memory and context awareness
- Two implementations: from-scratch and LangGraph

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hashwnath/Computer-Use-Agent
   cd nvidia-bash-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   - Get your NVIDIA API key from [build.nvidia.com](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2)
   - Update `config.py` with your API key:
     ```python
     llm_api_key: str = "your-nvidia-api-key-here"
     ```

## Usage

Run the from-scratch implementation (recommended):
```bash
python main_from_scratch.py
```

Or run the LangGraph implementation:
```bash
python main_langgraph.py
```

## Commands

- Type any request like "list files" or "find Python files"
- The agent will suggest bash commands and ask for confirmation
- Type `y` to execute or `n` to decline
- Type `quit` to exit

## Safety

⚠️ **WARNING**: This software can execute bash commands on your system. Use at your own risk.

The agent is restricted to safe commands like: `cd`, `cp`, `ls`, `cat`, `find`, `touch`, `echo`, `grep`, `pwd`, `mkdir`, `wget`, `sort`, `head`, `tail`, `du`

## License

Based on NVIDIA GenerativeAIExamples repository.
