from Core.ReActReasoner import ReActReasoner

class ReActMainAgent:
    def __init__(self, reasoner: ReActReasoner):
        self.reasoner = reasoner

    def ask(self, question: str, transparency: bool = True) -> str:
        answer, trace = self.reasoner.run(question)
        if transparency:
            print("--- Trace ---")
            for step in trace:
                print(step)
        return answer
