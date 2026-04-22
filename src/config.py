import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("SILICONFLOW_API_KEY", "sk-your_key_here")
    BASE_URL = "https://api.siliconflow.cn/v1"
    DEFAULT_MODEL = "FunAudioLLM/CosyVoice2-0.5B"

    VOICES = {
        "alex": "FunAudioLLM/CosyVoice2-0.5B:alex",
        "anna": "FunAudioLLM/CosyVoice2-0.5B:anna",
        "bella": "FunAudioLLM/CosyVoice2-0.5B:bella",
        "benjamin": "FunAudioLLM/CosyVoice2-0.5B:benjamin",
        "charles": "FunAudioLLM/CosyVoice2-0.5B:charles",
        "claire": "FunAudioLLM/CosyVoice2-0.5B:claire",
        "david": "FunAudioLLM/CosyVoice2-0.5B:david",
        "diana": "FunAudioLLM/CosyVoice2-0.5B:diana"
    }

    @staticmethod
    def validate():
        if not Config.API_KEY or Config.API_KEY == "sk-your_key_here":
            raise ValueError("SILICONFLOW_API_KEY 未设置或无效")