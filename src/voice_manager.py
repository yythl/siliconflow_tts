import json
import os
from .config import Config

class VoiceManager:
    def __init__(self, client=None):
        self.client = client
        self.local_storage_path = "voices.json"
        self.custom_voices = {}
        self.load_local()

    def set_client(self, client):
        self.client = client

    def load_local(self):
        if os.path.exists(self.local_storage_path):
            try:
                with open(self.local_storage_path, "r", encoding="utf-8") as f:
                    self.custom_voices = json.load(f)
            except Exception as e:
                print(f"加载本地音色失败: {e}")
                self.custom_voices = {}
        else:
            self.custom_voices = {}

    def save_local(self):
        try:
            with open(self.local_storage_path, "w", encoding="utf-8") as f:
                json.dump(self.custom_voices, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存本地音色失败: {e}")

    def get_voice_uri(self, name):
        if name in Config.VOICES:
            return Config.VOICES[name]

        if name in self.custom_voices:
            return self.custom_voices[name]["uri"]

        return None

    def sync_remote_voices(self):
        if not self.client:
            print("客户端未设置，跳过同步")
            return

        print("同步远程音色...")
        try:
            response = self.client.list_voices()

            voices_list = []
            if isinstance(response, dict):
                if 'result' in response:
                    voices_list = response['result']
                elif 'data' in response:
                    voices_list = response['data']
                elif 'voice' in response:
                    voices_list = [response['voice']] if response.get('voice') else []
            elif isinstance(response, list):
                voices_list = response

            count = 0
            for v in voices_list:
                uri = v.get('uri')
                name = v.get('customName')
                if uri and name:
                    self.custom_voices[name] = {
                        "uri": uri,
                        "model": v.get('model'),
                        "text": v.get('text', ''),
                        "raw": v
                    }
                    count += 1

            self.save_local()
            print(f"已同步 {count} 个自定义音色")

        except Exception as e:
            print(f"同步失败: {e}")
            raise

    def add_custom_voice(self, file_path, text, custom_name):
        if not self.client:
            raise Exception("客户端未设置")

        print(f"添加自定义音色 '{custom_name}'...")
        try:
            result = self.client.upload_voice(file_path, text, custom_name)

            if 'uri' in result:
                uri = result['uri']
                self.custom_voices[custom_name] = {
                    "uri": uri,
                    "model": Config.DEFAULT_MODEL,
                    "text": text,
                    "raw": result
                }
                self.save_local()
                print(f"音色 '{custom_name}' 添加成功。URI: {uri}")
                return uri
            else:
                print(f"上传成功但未在响应中找到URI: {result}")
                return None

        except Exception as e:
            print(f"添加自定义音色失败: {e}")
            raise

    def delete_custom_voice(self, name):
        if name not in self.custom_voices:
            raise Exception(f"音色 '{name}' 不存在")

        voice_data = self.custom_voices[name]
        uri = voice_data.get("uri")

        if self.client and uri:
            self.client.delete_voice(uri)

        del self.custom_voices[name]
        self.save_local()
        print(f"音色 '{name}' 已删除")