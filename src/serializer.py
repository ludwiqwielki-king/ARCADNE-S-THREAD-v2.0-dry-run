import json
import toon  # hypothetical library or custom parser

class Serializer:
    @staticmethod
    def to_hot_format(data):
        # Minified JSON for API input
        return json.dumps(data, separators=(',', ':'))
    
    @staticmethod
    def to_cold_format(data):
        # TOON for Archive storage (saving space)
        return toon.dumps(data) # Or custom compact format
    
    @staticmethod
    def from_cold_format(raw_data):
        # Convert back to JSON for model processing
        return toon.loads(raw_data)
