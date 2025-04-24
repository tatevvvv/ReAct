from typing import List, Dict, Any
from intelligence.abstractions import LLMModel, ReActPlugin
from helper import Helper
from persistence.ContextMemory import ContextMemory


class ReActReasoner:
    def __init__(
        self,
        session_id,
        llm: LLMModel,
        plugins: List[ReActPlugin],
        memory: ContextMemory,
        step_limit: int = 7
    ):
        self.llm = llm
        self.plugins = plugins
        self.memory = memory
        self.step_limit = step_limit

        headers = [p.prompt_header() for p in plugins]
        self.prompt_header = "".join(headers)

    def run(self, question: str, to_print: bool = True) -> Any:
        convo = self.memory.context("conversation", "")
        print(f'chat history: {convo}')
        if to_print:
            print(question)
        prompt = self.prompt_header
        if convo:
            prompt += convo + "\n"

        prompt += f"Question: {question}" + "\n"
        n_calls, n_badcalls= 0,0
        for i in range(1, self.step_limit + 1):
            n_calls+=1
            print(f'prompt is : {prompt}')
            thought_action = self.llm.generate(
                prompt + f"Thought {i}:",
                stop=[f"\nObservation {i}:"]
            )
            try:
                thought, action = thought_action.strip().split(f"\nAction {i}: ")
            except:
                print('ohh....', thought_action)
                n_badcalls+=1
                n_calls+=1
                thought = thought_action.strip().split('\n')[0]
                action = self.llm(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()

            tool_name = action.split("[", 1)[0].lower()
            plugin = Helper.get_plugin(self.plugins, tool_name)
            obs, r, done, info = Helper.step(plugin, action[0].lower() + action[1:])
            obs = obs.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {obs}\n"
            prompt += step_str
            if to_print:
                print(step_str)
            if done:
                print(f'last thought: {thought}')
                self.memory.upsert_conversation(question, thought)

                summary_prompt = f"Summarize the conversation so far into one paragraph:\n{convo}\nSummary:"
                new_summary = self.llm.generate(summary_prompt, stop=["\n"]).strip()
                self.memory.upsert_conversation(new_summary)
                break

        if not done:
            obs, r, done, info = Helper.step(plugin, "finish[]")

        if to_print:
            print(info, "\n")

        info.update({'n_calls': n_calls, 'n_badcalls': n_badcalls, 'traj': prompt})
        return r, info
