from typing import Optional
from abstractions import ReActPlugin
import requests

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
