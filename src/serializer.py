import json

class Serializer:
    """
    Serializer for Ariadne's Thread v2.0
    Uses native JSON only - no external dependencies.
    """
    @staticmethod
    def to_hot_format(data: dict) -> str:
        """Minified JSON for API input (saves tokens)."""
        return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

    @staticmethod
    def to_cold_format(data: dict) -> str:
        """Pretty-printed JSON for archive storage."""
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def from_json(raw_data: str) -> dict:
        """Parse JSON string to dict."""
        return json.loads(raw_data)
