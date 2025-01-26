import json
import os
from typing import Dict, Any

class SettingsManager:
    _instance = None
    DEFAULT_SETTINGS = {
        "sound_enabled": True,
        "music_enabled": True,
        "sound_volume": 0.7,
        "music_volume": 0.4
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.settings_file = os.path.join(os.path.dirname(__file__), 'settings.json')
            self.settings = self.load_settings()
            self.initialized = True
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create with defaults if not exists."""
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.save_settings(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings to file."""
        self.settings = settings
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
    
    def get_setting(self, key: str) -> Any:
        """Get a setting value."""
        return self.settings.get(key, self.DEFAULT_SETTINGS.get(key))
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a setting value and save to file."""
        self.settings[key] = value
        self.save_settings(self.settings)