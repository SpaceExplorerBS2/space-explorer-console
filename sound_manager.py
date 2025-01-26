import pygame.mixer
import os
from typing import Dict, Optional
from settings_manager import SettingsManager
import random

class SoundManager:
    _instance: Optional['SoundManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            try:
                pygame.mixer.init(44100, -16, 2, 512)
                pygame.mixer.set_num_channels(8)
                self.music_channel = pygame.mixer.Channel(0)
                self.sfx_channel = pygame.mixer.Channel(1)
                
                self.sounds: Dict[str, pygame.mixer.Sound] = {}
                self.background_tracks: Dict[str, pygame.mixer.Sound] = {}
                self.current_track: Optional[str] = None
                self.settings = SettingsManager()
                self.load_sounds()
                print("Sound manager initialized successfully")
                self.initialized = True
            except Exception as e:
                print(f"Error initializing sound manager: {e}")
                self.initialized = False

    def load_sounds(self) -> None:
        """Load all sound effects from the sfx directory."""
        sfx_dir = os.path.join(os.path.dirname(__file__), 'sfx')
        print(f"Loading sounds from: {sfx_dir}")
        
        if not os.path.exists(sfx_dir):
            print(f"Warning: sfx directory not found at {sfx_dir}")
            return
        
        sound_files = {
            'blip': 'blip.wav',
            'thrust': 'thrust.wav',
            'crash': 'crash.wav',
            'collect': 'collect.wav',
            'game_over': 'game_over.wav'
        }
        
        for sound_name, filename in sound_files.items():
            file_path = os.path.join(sfx_dir, filename)
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"Loaded sound: {sound_name} from {file_path}")
                else:
                    print(f"Warning: Sound file not found: {file_path}")
            except Exception as e:
                print(f"Error loading sound {filename}: {e}")
        
        # Load background music tracks
        music_files = {
            'corridors': 'corridors_of_time.mp3',
            'space': 'outer_space.wav'
        }
        
        for track_name, filename in music_files.items():
            music_path = os.path.join(sfx_dir, filename)
            try:
                if os.path.exists(music_path):
                    self.background_tracks[track_name] = pygame.mixer.Sound(music_path)
                    print(f"Loaded background track: {track_name} from {music_path}")
                else:
                    print(f"Warning: Background music file not found: {music_path}")
            except Exception as e:
                print(f"Error loading background track {filename}: {e}")

    def check_and_play_next_track(self) -> None:
        """Check if current track is done and play next one if needed."""
        if not self.music_channel.get_busy() and self.background_tracks:
            # Current track finished, play another random one
            self.play_background_music()

    def play_menu_sound(self) -> None:
        """Play the menu navigation sound."""
        try:
            if not hasattr(self, 'initialized') or not self.initialized:
                print("Sound manager not properly initialized")
                return
                
            if not self.settings.get_setting('sound_enabled'):
                return
                
            if 'blip' not in self.sounds:
                print("Warning: Blip sound not loaded")
                return
                
            volume = self.settings.get_setting('sound_volume')
            self.sounds['blip'].set_volume(volume)
            self.sfx_channel.play(self.sounds['blip'])
        except Exception as e:
            print(f"Error playing menu sound: {e}")
    
    def play(self, sound_name: str, volume_scale: float = 1.0) -> None:
        """Play a sound effect by its name with optional volume scaling."""
        try:
            if not hasattr(self, 'initialized') or not self.initialized:
                return
                
            if not self.settings.get_setting('sound_enabled'):
                return
                
            if sound_name not in self.sounds:
                print(f"Warning: Sound {sound_name} not loaded")
                return
                
            base_volume = self.settings.get_setting('sound_volume')
            final_volume = base_volume * volume_scale
            self.sounds[sound_name].set_volume(final_volume)
            self.sfx_channel.play(self.sounds[sound_name])
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    
    def play_background_music(self, track_name: str = None) -> None:
        """Play a background music track. If no track specified, plays a random track."""
        try:
            if not hasattr(self, 'initialized') or not self.initialized:
                return
                
            if not self.settings.get_setting('music_enabled'):
                return
                
            if not self.background_tracks:
                print("No background tracks loaded")
                return

            # If no track specified, choose a random one (different from current)
            if track_name is None:
                tracks = list(self.background_tracks.keys())
                if len(tracks) > 1 and self.current_track:
                    # Remove current track from options to ensure we switch
                    tracks.remove(self.current_track)
                track_name = random.choice(tracks)
            
            if track_name not in self.background_tracks:
                print(f"Warning: Track {track_name} not found")
                return
                
            volume = self.settings.get_setting('music_volume')
            self.background_tracks[track_name].set_volume(volume)
            self.music_channel.play(self.background_tracks[track_name])  # Remove -1 to not loop infinitely
            self.current_track = track_name
            print(f"Now playing: {track_name}")
            
        except Exception as e:
            print(f"Error playing background music: {e}")
    
    def stop_background_music(self) -> None:
        """Stop the background music."""
        try:
            if hasattr(self, 'music_channel'):
                self.music_channel.stop()
        except Exception as e:
            print(f"Error stopping background music: {e}")
    
    def stop_all(self) -> None:
        """Stop all sounds and music."""
        try:
            pygame.mixer.stop()
        except Exception as e:
            print(f"Error stopping all sounds: {e}")