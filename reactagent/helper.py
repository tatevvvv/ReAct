from typing import Optional
import os

from reactagent.intelligence.GeminiModel import GeminiModel
from reactagent.intelligence.abstractions import ReActPlugin
import requests

from reactagent.persistence.DummyRepository import DummyRepository
from reactagent.persistence.MongoDbRepository import MongoDbRepository
from reactagent.plugins.wikipedia.WikipediaPlugin import WikipediaPlugin
from reactagent.plugins.wolframAlpha.WolframAlphaPlugin import WolframAlphaPlugin


class Helper:
    @staticmethod
    def get_plugin(plugin_list, action_name: str) -> Optional[ReActPlugin]:
        for p in plugin_list:
            if action_name in p.action_names:
                return p
        return None

    @staticmethod
    def step(plugin, action):
        attempts = 0
        while attempts < 10:
            try:
                return plugin.step(action)
            except requests.exceptions.Timeout:
                print('timed out')
                attempts += 1

    @staticmethod
    def resolve_dependencies(configuration):
        model_name = configuration.get("model").lower()
        if model_name == "gemini":
            api_key = os.environ.get("GEMINI_API_KEY")
            llm = GeminiModel(name='gemini', api_key=api_key)
        else:
            raise Exception(f"Unsupported llm model: {model_name}")
        plugins = []
        if configuration.get("plugins", {}).get("wikipedia", "off").lower() == "on":
            plugins.append(WikipediaPlugin())
        if configuration.get("plugins", {}).get("wolfram", "off").lower() == "on":
            wolfram_api_key = os.environ.get("WOLFRAM_API_KEY")
            plugins.append(WolframAlphaPlugin(wolfram_api_key))
        ltm = None
        ltm_backend = configuration.get("persistence").lower()
        if ltm_backend == "mongodb":
            ltm = MongoDbRepository(configuration)
        elif ltm_backend == "dummy":
            ltm = DummyRepository()
        else:
            raise Exception(f"Unsupported ltm backend: {ltm_backend}")

        return llm, plugins, ltm
