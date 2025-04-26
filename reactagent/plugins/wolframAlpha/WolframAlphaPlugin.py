from typing import List

import gym
import requests

from reactagent.intelligence.abstractions import ReActPlugin


class WolframAlphaPlugin(ReActPlugin):
    @property
    def action_names(self) -> List[str]:
        return ['compute', 'finish']

    def step(self, action):
        return self.env.step(action)
    def reset(self):
        self.env.reset()
    def prompt_header(self) -> str:
        return r"""If user question includes mathematical calculation question, solve mathematical calculation questions with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types:

(1) Compute[expression], which sends a query to Wolfram Alpha API in the format {"input": query}, where 'query' is a simplified keyword query or a mathematical expression following Wolfram Alpha's guidelines:
- Convert inputs to simplified keyword queries whenever possible.
- Send queries in English only.
- Always use proper Markdown formatting for math, scientific, and chemical expressions.
- Always use exponent notation: '6*10^14', NEVER '6e14'.
- Use single-letter variable names.
- Include spaces between compound units (e.g., "Ω m" for "ohm*meter").


(3) Finish[answer], which returns the answer and completes the task.

Here are relevant examples:

Question: What is the derivative of \( x^2 \sin(x) \)?
Thought 1: I need to compute the derivative of the function.
Action 1: Compute[{"input": "derivative x^2 sin(x)"}]
Observation 1: The derivative is \( 2 x \sin(x) + x^2 \cos(x) \).
Thought 2: The derivative is obtained, so the answer is \( 2 x \sin(x) + x^2 \cos(x) \).
Action 2: Finish[\( 2 x \sin(x) + x^2 \cos(x) \)]

Question: Evaluate the integral \( \int_0^\infty e^{-x^2} \, dx \).
Thought 1: Known Gaussian integral.
Action 1: Compute[{"input": "integral exp(-x^2) from 0 to infinity"}]
Observation 1: The integral evaluates to \( \frac{\sqrt{\pi}}{2} \).
Thought 2: Integral computed correctly, so the answer is \( \frac{\sqrt{\pi}}{2} \).
Action 2: Finish[\( \frac{\sqrt{\pi}}{2} \)]

Question: Solve the equation \( x^2 - 5x + 6 = 0 \).
Thought 1: A simple quadratic equation.
Action 1: Compute[{"input": "solve x^2 - 5x + 6 = 0"}]
Observation 1: Solutions are \( x = 2 \) and \( x = 3 \).
Thought 2: Solutions clearly computed, so the answer is \( x = 2 \) and \( x = 3 \).
Action 2: Finish[\( x = 2 \) and \( x = 3 \)]

Question: Calculate determinant of \( \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \).
Thought 1: Need determinant of a 2x2 matrix.
Action 1: Compute[{"input": "determinant {{1, 2}, {3, 4}}"}]
Observation 1: The determinant is \( -2 \).
Thought 2: Determinant calculation clear, answer is \( -2 \).
Action 2: Finish[\( -2 \)]

Question: What is the value of \( \pi \) to 10 decimal places?
Thought 1: Need precise value of \( \pi \).
Action 1: Compute[{"input": "Pi to 10 decimal places"}]
Observation 1: The value is 3.1415926535.
Thought 2: Obtained Pi value clearly.
Action 2: Finish[3.1415926535]
    """

    def __init__(self, api_key):
        super().__init__("WolframAlpha")
        self.env = WolframEnv(api_key)

class WolframEnv(gym.Env):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.obs = None  # current observation
        self.steps = 0  # current number of steps
        self.answer = None  # current answer from the agent

    def _get_obs(self):
        return self.obs

    def _get_info(self):
        return {"steps": self.steps, "answer": self.answer}

    def reset(self, seed=None, return_info=False, options=None):
        self.obs = ("Interact with wolfram alpha using compute[] and "
                    "finish[].\n")
        self.steps = 0  # current number of steps
        self.answer = None  # current answer from the agent
        observation = self._get_obs()
        info = self._get_info()
        return (observation, info) if return_info else observation

    def search_step(self, entity):
        start = entity.find('"input": "') + len('"input": "')
        end = entity.find('"', start)

        input_value = entity[start:end]
        input_value=input_value.replace(" ", "+")
        url = f"https://www.wolframalpha.com/api/v1/llm-api?input={input_value}&appid={self.api_key}&maxchars=500"
        response_text = requests.get(url).text
        if response_text =="":  # mismatch
            self.obs = f"Could not solve {entity}."
        else:
            self.obs = response_text
    def step(self, action):
        done = False
        action = action.strip()
        if self.answer is not None:  # already finished
            done = True
            return self.obs, done, self._get_info()

        if action.startswith("compute[") and action.endswith("]"):
            entity = action[len("compute["):-1]
            self.search_step(entity)
        elif action.startswith("finish[") and action.endswith("]"):
            answer = action[len("finish["):-1]
            self.answer = answer
            done = True
            self.obs = f"Finished\n"
        elif action.startswith("think[") and action.endswith("]"):
            self.obs = "Nice thought."
        else:
            self.obs = "Invalid action: {}".format(action)
        self.steps += 1
        return self.obs, done, self._get_info()