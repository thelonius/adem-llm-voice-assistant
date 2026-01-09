"""}
ADEM LLM Voice Assistant - Core Configuration Module
Полная система конфигурации для голосового ассистента с LLM
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()


@dataclass
class STTConfig:
    """Speech-to-Text Configuration"""
    provider: str = "whisper"  # whisper | google | azure
    model: str = "base"  # для Whisper: tiny, base, small, medium, large
    language: str = "ru"  # код языка ISO 639-1
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    
    # API ключи (из .env)
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    google_credentials: Optional[str] = field(default_factory=lambda: os.getenv("GOOGLE_CREDENTIALS_PATH"))
    azure_key: Optional[str] = field(default_factory=lambda: os.getenv("AZURE_SPEECH_KEY"))
    azure_region: Optional[str] = field(default_factory=lambda: os.getenv("AZURE_REGION"))
    
    # Расширенные параметры
    enable_vad: bool = True  # Voice Activity Detection
    vad_threshold: float = 0.5
    silence_duration: float = 1.0  # секунды тишины перед остановкой записи


@dataclass
class LLMConfig:
    """Large Language Model Configuration"""
    provider: str = "openai"  # openai | google | anthropic | ollama
    model: str = "gpt-4"  # gpt-4, gpt-3.5-turbo, gemini-pro, claude-3-opus
    temperature: float = 0.7
    max_tokens: int = 500
    top_p: float = 0.9
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    
    # API ключи
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    google_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    ollama_base_url: str = "http://localhost:11434"
    
    # System prompt
    system_prompt: str = """Ты — голосовой ассистент ADEM для работы с LLM и генеративными паттернами.
    Помогай пользователю с параметрическим моделированием, 3D-графикой и AI интеграциями.
    Отвечай кратко и по существу."""
    
    # Контекст и история
    max_history_length: int = 10  # количество сообщений в истории
    enable_streaming: bool = False  # потоковый вывод ответа


@dataclass
class TTSConfig:
    """Text-to-Speech Configuration"""
    provider: str = "elevenlabs"  # elevenlabs | google | azure | pyttsx3
    voice_id: str = "default"
    model: str = "eleven_multilingual_v2"
    stability: float = 0.5
    similarity_boost: float = 0.75
    
    # API ключи
    elevenlabs_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY"))
    google_credentials: Optional[str] = field(default_factory=lambda: os.getenv("GOOGLE_CREDENTIALS_PATH"))
    azure_key: Optional[str] = field(default_factory=lambda: os.getenv("AZURE_SPEECH_KEY"))
    azure_region: Optional[str] = field(default_factory=lambda: os.getenv("AZURE_REGION"))
    
    # Параметры аудио
    output_format: str = "mp3_44100_128"  # для ElevenLabs
    speed: float = 1.0  # скорость речи
    pitch: float = 0.0  # высота тона (-20 до 20)
    volume: float = 1.0  # громкость (0.0 до 1.0)


@dataclass
class AudioConfig:
    """Audio System Configuration"""
    input_device: Optional[int] = None  # None = default device
    output_device: Optional[int] = None
    sample_rate: int = 44100
    channels: int = 2
    buffer_size: int = 2048
    
    # Обработка аудио
    enable_noise_reduction: bool = True
    enable_echo_cancellation: bool = True
    enable_auto_gain: bool = True
    
    # Файлы
    recordings_dir: Path = Path("recordings")
    temp_dir: Path = Path("temp")


@dataclass
class IntegrationConfig:
    """Integration with External Systems"""
    
    # Grasshopper/Rhino
    grasshopper_enabled: bool = False
    grasshopper_port: int = 8080
    grasshopper_host: str = "localhost"
    
    # TouchDesigner
    touchdesigner_enabled: bool = False
    touchdesigner_port: int = 9000
    touchdesigner_osc_ip: str = "127.0.0.1"
    
    # Manim
    manim_enabled: bool = False
    manim_quality: str = "high"  # low, medium, high, 4k
    manim_output_dir: Path = Path("animations")
    
    # WebSocket для real-time
    websocket_enabled: bool = False
    websocket_port: int = 8765
    websocket_host: str = "0.0.0.0"


@dataclass
class AppConfig:
    """Main Application Configuration"""
    
    # Подконфигурации
    stt: STTConfig = field(default_factory=STTConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    integration: IntegrationConfig = field(default_factory=IntegrationConfig)
    
    # Общие настройки
    app_name: str = "ADEM LLM Voice Assistant"
    version: str = "0.1.0"
    debug_mode: bool = field(default_factory=lambda: os.getenv("DEBUG", "False").lower() == "true")
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    
    # Директории
    base_dir: Path = Path(__file__).parent
    config_dir: Path = base_dir / "config"
    logs_dir: Path = base_dir / "logs"
    data_dir: Path = base_dir / "data"
    
    # Производительность
    max_concurrent_requests: int = 5
    request_timeout: int = 30  # секунды
    cache_enabled: bool = True
    cache_ttl: int = 3600  # секунды
    
    def __post_init__(self):
        """Создание необходимых директорий"""
        for directory in [self.config_dir, self.logs_dir, self.data_dir, 
                         self.audio.recordings_dir, self.audio.temp_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save(self, filepath: Union[str, Path]) -> None:
        """Сохранение конфигурации в JSON"""
        filepath = Path(filepath)
        config_dict = {
            "stt": self.stt.__dict__,
            "llm": self.llm.__dict__,
            "tts": self.tts.__dict__,
            "audio": {k: str(v) if isinstance(v, Path) else v 
                     for k, v in self.audio.__dict__.items()},
            "integration": {k: str(v) if isinstance(v, Path) else v 
                           for k, v in self.integration.__dict__.items()},
            "app_name": self.app_name,
            "version": self.version,
            "debug_mode": self.debug_mode,
            "log_level": self.log_level,
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, filepath: Union[str, Path]) -> 'AppConfig':
        """Загрузка конфигурации из JSON"""
        filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        return cls(
            stt=STTConfig(**config_dict.get("stt", {})),
            llm=LLMConfig(**config_dict.get("llm", {})),
            tts=TTSConfig(**config_dict.get("tts", {})),
            audio=AudioConfig(**config_dict.get("audio", {})),
            integration=IntegrationConfig(**config_dict.get("integration", {})),
            app_name=config_dict.get("app_name", "ADEM LLM Voice Assistant"),
            version=config_dict.get("version", "0.1.0"),
            debug_mode=config_dict.get("debug_mode", False),
            log_level=config_dict.get("log_level", "INFO"),
        )
    
    def validate(self) -> List[str]:
        """Валидация конфигурации"""
        errors = []
        
        # Проверка API ключей
        if self.stt.provider == "whisper" and not self.stt.openai_api_key:
            errors.append("Whisper STT требует OPENAI_API_KEY")
        
        if self.llm.provider == "openai" and not self.llm.openai_api_key:
            errors.append("OpenAI LLM требует OPENAI_API_KEY")
        
        if self.tts.provider == "elevenlabs" and not self.tts.elevenlabs_api_key:
            errors.append("ElevenLabs TTS требует ELEVENLABS_API_KEY")
        
        # Проверка диапазонов значений
        if not 0 <= self.llm.temperature <= 2:
            errors.append("LLM temperature должен быть между 0 и 2")
        
        if not 0 <= self.tts.volume <= 1:
            errors.append("TTS volume должен быть между 0 и 1")
        
        return errors


# Создание глобального экземпляра конфигурации
config = AppConfig()


if __name__ == "__main__":
    # Пример использования
    print(f"Приложение: {config.app_name} v{config.version}")
    print(f"STT Provider: {config.stt.provider}")
    print(f"LLM Provider: {config.llm.provider}")
    print(f"TTS Provider: {config.tts.provider}")
    
    # Валидация
    errors = config.validate()
    if errors:
        print("\nОшибки конфигурации:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\nКонфигурация валидна!")
    
    # Сохранение примера конфигурации
    config.save("config_example.json")
    print("\nПример конфигурации сохранён в config_example.json")
