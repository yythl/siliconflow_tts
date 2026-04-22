from openai import OpenAI
import httpx
import os
from .config import Config

class SiliconFlowClient:
    def __init__(self):
        self.api_key_valid = False
        
        if Config.API_KEY and Config.API_KEY != "sk-your_key_here":
            self.api_key_valid = True
            self.client = OpenAI(
                api_key=Config.API_KEY,
                base_url=Config.BASE_URL
            )
            self.headers = {"Authorization": f"Bearer {Config.API_KEY}"}
        else:
            self.client = None
            self.headers = {}

    def _check_client(self):
        if not self.client:
            raise Exception("API Key未配置，请在设置中配置API Key")

    def generate_speech(self, text, voice=None, model=None, response_format="mp3", output_path="output.mp3", speed=1.0, gain=0.0, stream=False):
        self._check_client()

        model = model or Config.DEFAULT_MODEL

        if voice in Config.VOICES:
            voice_id = Config.VOICES[voice]
        else:
            voice_id = voice or Config.VOICES["alex"]

        print(f"生成语音 - 模型: {model}, 音色: '{voice_id}', 语速: {speed}, 音量: {gain}")

        try:
            extra_body = {}
            if gain != 0.0:
                extra_body["gain"] = gain

            response = self.client.audio.speech.create(
                model=model,
                voice=voice_id,
                input=text,
                speed=speed,
                response_format=response_format,
                extra_body=extra_body if extra_body else None
            )

            if stream:
                return response.iter_bytes()
            else:
                response.stream_to_file(output_path)
                return output_path

        except Exception as e:
            print(f"生成语音错误: {e}")
            raise

    def upload_voice(self, file_path, text, custom_name, model=None):
        self._check_client()

        model = model or Config.DEFAULT_MODEL
        url = f"{Config.BASE_URL}/uploads/audio/voice"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"音频文件不存在: {file_path}")

        try:
            with open(file_path, "rb") as f:
                files = {
                    "file": (os.path.basename(file_path), f, "audio/mpeg")
                }
                data = {
                    "model": model,
                    "customName": custom_name,
                    "text": text
                }

                print(f"上传音色: {custom_name} 从 {file_path}...")
                response = httpx.post(url, headers=self.headers, data=data, files=files, timeout=120.0)

                if response.status_code != 200:
                    raise Exception(f"上传失败: {response.status_code} - {response.text}")

                result = response.json()
                print(f"上传响应: {result}")
                return result

        except Exception as e:
            print(f"上传音色错误: {e}")
            raise

    def list_voices(self, model=None):
        self._check_client()

        model = model or Config.DEFAULT_MODEL
        url = f"{Config.BASE_URL}/audio/voice/list"

        try:
            response = httpx.get(url, headers=self.headers, params={"model": model}, timeout=30.0)

            if response.status_code != 200:
                raise Exception(f"获取音色列表失败: {response.status_code} - {response.text}")

            result = response.json()
            print(f"音色列表响应: {result}")
            return result

        except Exception as e:
            print(f"获取音色列表错误: {e}")
            raise

    def delete_voice(self, uri):
        self._check_client()

        url = f"{Config.BASE_URL}/audio/voice/deletions"

        try:
            response = httpx.post(url, headers=self.headers, json={"uri": uri}, timeout=30.0)

            if response.status_code != 200:
                raise Exception(f"删除失败: {response.status_code} - {response.text}")

            result = response.json()
            print(f"删除响应: {result}")
            return result

        except Exception as e:
            print(f"删除音色错误: {e}")
            raise