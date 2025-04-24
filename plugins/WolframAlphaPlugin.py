import json
from typing import List
import os
from intelligence.abstractions import ReActPlugin


class WolframAlphaPlugin(ReActPlugin):
    @property
    def action_names(self) -> List[str]:
        return ["solve"]

    def prompt_header(self) -> str:
        base_dir = os.path.dirname(__file__)  # folder containing WikipediaPlugin.py
        filepath = os.path.join(base_dir, 'prompts', 'prompts_naive.json')
        with open(filepath, 'r') as f:
            prompt_dict = json.load(f)

        webthink_examples = prompt_dict['webthink_simple6']
        instruction = """Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types: 
        (1) Search[entity], which searches the exact entity on wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.
        (2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.
        (3) Finish[answer], which returns the answer and finishes the task.
        Here are some examples.
        """
        webthink_prompt = instruction + webthink_examples
        return webthink_prompt

        return (
                "If you see mathematical question solve it with interleaving Thought, Action, Observation steps."
                " Thought can reason about the current situation, and Action can be two types: "
                " (1) Solve[equation], which solves the exact equation on Wolfram and returns the first paragraph if it exists. "
                " If not, it will return some similar equations to solve. "
                " (2) Finish[answer], which returns the answer and finishes the task.")

    @property
    def exemplars(self) -> str:
        return (
            "Question: What is the derivative of x^3 function?\n"
            "Thought 1: I need to solve the equation form for derivative of x^3 to solve.\n"
            "Action 1: solve[df/dx, f(x) = x^3]\n"
            "Observation 1:  \n"
            "Thought 2: The author is Jane Austen.\n"
            "Action 2: finish[Jane Austen]\n"
        )

    def __init__(self, env):
        super().__init__("WolframAlpha")
        self.env = env

    def step(self, action):
        self.env.step(action)