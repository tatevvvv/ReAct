# reactagent

A Python package implementing the ReAct framework as described in the 2023 ICLR paper https://arxiv.org/pdf/2210.03629

---

## Option 1: Install and Use as a Package

### 1. Create a Python virtual environment

```bash
mkdir my_project
cd my_project
python -m venv .venv
# Activate venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\activate
```

### 2. Install the package

```bash
pip install git+https://github.com/tatevvvv/ReAct.git@main
```

### 3. Prepare the appsettings.json file

Create a file named `appsettings.json` in your project folder with the following structure:

```json
{
  "model": "gemini",
  "enableCoT-SC": false,
  "plugins": {
    "wikipedia": "on",
    "wolfram": "off"
  },
  "persistence": "mongodb",
  "mongodb": {
    "uri": "",
    "db": "",
    "collection": ""
  }
}
```

For persistence there is one option available. mongodb
If you prefer skipping persistence, put the value 'dummy'
If you want to continue old conversation, provide the conversation session_id, and it will load in memory
conversation context.

### 4. Use the package in your code

Below is an example on how to create a Python script (e.g., `agentclient.py`) to run the agent:
Pass transparency value as True if you prefer to see agent reasoning-action sequence. 
```python
from uuid import uuid4
from reactagent import Agent

tag = str(uuid4())
agent = Agent(tag, settings_path="appsettings.json")

question = input("Your question: ")

agent.start(question, transparency=True)
```

Run it:

```bash
python agentclient.py
```

---

## Option 2: Clone the Repository and Run `client.py`

If you prefer to work directly with the source code and `reactclient.py` script, follow these steps.

### 1. Clone the repository

```bash
git clone https://github.com/tatevvvv/ReAct.git
cd ReAct
```

### 2. (Optional) Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate    # Windows PowerShell
pip install -e .
```

### 3. Ensure the configuration file

Make sure `appsettings.json` exists in the repo root (or create it as shown above).

### 4. Run `reactclient.py`

```bash
python reactclient.py
```

This script will prompt you to enter a question and then display the agent’s response.

Please note that you need to have a Gemini API key and store it in the environment variable GEMINI_API_KEY
