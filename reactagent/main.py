from helper import Helper
from reactagent.core.ReActMainAgent import ReActMainAgent
import json
from uuid import uuid4
from typing import Dict

def main():
    with open("appsettings.json") as f:
        cfg: Dict = json.load(f)

    intro = "Starting a chat. Please don't say 'Thank you' or 'Please' it costs millions for us. Provide the session_id if you want to continue previous session. Type ‘new’ to start a new session.Type 'quit' to exit."
    cnt = True
    while cnt:
        cnt = False
        try:
          user_input = input(f"{intro}").strip()
        except (EOFError, KeyboardInterrupt):
          print("Invalid input. Try again.")
          cnt = True
        if not user_input or user_input.lower() in {"exit","quit"}:
          return ## terminate program
        if user_input.lower() == "new":
          session_id = str(uuid4())
        else:
          session_id = user_input

    llm, plugins, ltm = Helper.resolve_dependencies(cfg)
    agent = ReActMainAgent(session_id,llm, plugins, ltm)
    ## todo: validate session id
    print(f"Session: {session_id} started. Ask a question")


    while True:
        try:
            question = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        answer, info = agent.ask(question)
        print(answer)

    agent.flush()

    if __name__ == '__main__':
        main()