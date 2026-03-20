import json

class ContextManager:
    SAFETY_FACTOR = 0.25  # Default, overwritten by safety.yaml or runtime config
    
    def __init__(self, model_configs, safety_config=None):
        self.model_configs = model_configs # Słownik {model_name: model_cfg}
        if safety_config:
            self.SAFETY_FACTOR = safety_config.get("SAFETY_FACTOR", 0.25)
    
    def get_max_input_tokens(self, model_name):
        limit = self.model_configs.get(model_name, {}).get("context_window", 128000)
        return int(limit * self.SAFETY_FACTOR)
    
    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4  # Zgrubne przybliżenie (1 token = ~4 znaki)

    def build_history_slice(self, thread: list, model_name: str) -> list:
        max_tokens = self.get_max_input_tokens(model_name)
        total_tokens = 0
        active_slice = []

        # Iterujemy od najnowszego wpisu
        for entry in reversed(thread):
            entry_str = json.dumps(entry, ensure_ascii=False)
            tokens = self._estimate_tokens(entry_str)
            if total_tokens + tokens > max_tokens:
                break
            active_slice.append(entry)
            total_tokens += tokens

        return list(reversed(active_slice))
