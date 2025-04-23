import helper
from abstractions import LLMModel
from helper import *

class ReActReasoner:
    def __init__(self,
                 llm: LLMModel,
                 plugins,
                 step_limit: int = 7):
        self.llm = llm
        self.plugins = plugins
        self.step_limit = step_limit

        header_sections = []

        for plugin in plugins:
            header_sections.append(plugin.prompt_header())
        self.prompt_header = "".join(header_sections)

    def run(self, question, to_print=True):
        if to_print:
            print(question)
        prompt = self.prompt_header
        prompt += f"Question: {question}\n"

        n_calls, n_badcalls = 0, 0
        for i in range(1, self.step_limit + 1):
            n_calls += 1
            thought_action = self.llm.generate(prompt + f"Thought {i}:", stop=[f"\nObservation {i}:"])
            try:
                thought, action = thought_action.strip().split(f"\nAction {i}: ")
            except:
                print('ohh...', thought_action)
                n_badcalls += 1
                n_calls += 1
                thought = thought_action.strip().split('\n')[0]
                action = self.llm.generate(prompt + f"Thought {i}: {thought}\nAction {i}:", stop=[f"\n"]).strip()
            action_name = action.split('[', 1)[0]
            print(f'action: {action_name.lower()}')
            plugin = Helper.get_plugin(self.plugins, action_name.lower())
            print(f'plugin: {plugin.name}')
            obs, r, done, info = Helper.step(plugin, action[0].lower() + action[1:])
            obs = obs.replace('\\n', '')
            step_str = f"Thought {i}: {thought}\nAction {i}: {action}\nObservation {i}: {obs}\n"
            prompt += step_str
            if to_print:
                print(step_str)
            if done:
                break
        if not done:
            obs, r, done, info = Helper.step(plugin, "finish[]")
        if to_print:
            print(info, '\n')
        info.update({'n_calls': n_calls, 'n_badcalls': n_badcalls, 'traj': prompt})
        return r, info
