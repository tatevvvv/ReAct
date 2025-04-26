from typing import List, Dict, Any
from reactagent.intelligence.abstractions import LLMModel, ReActPlugin
from reactagent.helper import Helper
from reactagent.persistence.ContextMemory import ContextMemory


class ReActReasoner:
    def __init__(
        self,
        llm: LLMModel,
        plugins: List[ReActPlugin],
        memory: ContextMemory,
        step_limit: int = 7
    ):
        self.llm = llm
        self.plugins = plugins
        self.memory = memory
        self.step_limit = step_limit ## how many steps we will tolerate llm to perform before finding the answer.
        headers = [p.prompt_header() for p in plugins]
        self.prompt_header = "".join(headers)
        self.memory.add_prompt(self.prompt_header)

    def run(self, question: str, transparency: bool = True) -> Any:
        summary = self.memory.context["summaries"]
        for plugin in self.plugins:
            plugin.reset()
        current_plugin = None
        qNa = question
        if transparency:
            print(question)
        prompt = self.prompt_header
        if summary:
            prompt += f"This is summary of previous conversations: {summary} + \n"

        prompt += f"Question: {question}" + "\n"
        n_calls, n_badcalls= 0,0

        for i in range(1, self.step_limit + 1):
            n_calls+=1
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
                try:
                 action = self.llm(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()
                except:
                    done = True
                    obs = ""
                    info=""
                    break
            tool_name = action.split("[", 1)[0].lower()
            if current_plugin is None:
                plugin = Helper.get_plugin(self.plugins, tool_name)
                current_plugin = plugin
            else:
                plugin = Helper.get_plugin(self.plugins, tool_name)

                if plugin.name != current_plugin.name:
                    # switch plugin
                    print(f'plugin switched from {current_plugin.name} to {plugin.name}')
                    current_plugin = plugin

            obs, done, info = Helper.step(current_plugin, action[0].lower() + action[1:])
            obs = obs.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {obs}\n"
            prompt += step_str
            if transparency:
                print(step_str)
            if done:
                break

        qNa += f'\nAnswer:{thought}'
        self.memory.upsert_conversation(question, prompt)

        summary_prompt = f"Summarize the conversation into one paragraph include what was the question, what was the answer:\n The conversation: {qNa}\nSummary:"
        new_summary = self.llm.generate(summary_prompt, stop=["\n"]).strip()
        self.memory.upsert_summary(new_summary)

        if not done:
            obs, done, info = Helper.step(plugin, "finish[]")

        if transparency:
            print(info, "\n")

        info.update({'n_calls': n_calls, 'n_badcalls': n_badcalls, 'traj': prompt})
        return obs, info
