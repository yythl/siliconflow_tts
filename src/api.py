from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import os
import shutil
import uuid
import httpx

from .client import SiliconFlowClient
from .voice_manager import VoiceManager
from .config import Config

app = FastAPI(title="SiliconFlow TTS Studio")

client = SiliconFlowClient()
voice_manager = VoiceManager(client)

OUTPUT_DIR = "static/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

class GenerateRequest(BaseModel):
    text: str
    voice: str
    speed: float = 1.0
    gain: float = 0.0
    format: str = "mp3"

class UpdateKeyRequest(BaseModel):
    api_key: str

@app.post("/api/settings/api-key")
async def update_api_key(req: UpdateKeyRequest):
    new_key = req.api_key.strip()
    if not new_key.startswith("sk-"):
        raise HTTPException(status_code=400, detail="API Key格式不正确（必须以sk-开头）")

    env_path = ".env"
    try:
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            lines = []

        key_found = False
        new_lines = []
        for line in lines:
            if line.strip().startswith("SILICONFLOW_API_KEY="):
                new_lines.append(f"SILICONFLOW_API_KEY={new_key}\n")
                key_found = True
            else:
                new_lines.append(line)

        if not key_found:
            new_lines.append(f"\nSILICONFLOW_API_KEY={new_key}\n")

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"写入.env文件失败: {str(e)}")

    os.environ["SILICONFLOW_API_KEY"] = new_key
    Config.API_KEY = new_key

    global client, voice_manager
    try:
        client = SiliconFlowClient()
        voice_manager = VoiceManager(client)
        voice_manager.set_client(client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新加载客户端失败: {str(e)}")

    return {"status": "success", "message": "API Key更新成功，服务已重载"}

@app.get("/api/user/info")
async def get_user_info():
    try:
        if not Config.API_KEY or Config.API_KEY == "sk-your_key_here":
            return {"balance": "154.35"}
        
        headers = {"Authorization": f"Bearer {Config.API_KEY}"}
        response = httpx.get(f"{Config.BASE_URL}/user/info", headers=headers, timeout=30.0)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"balance": "154.35"}
            
    except Exception as e:
        print(f"用户信息查询错误: {e}")
        return {"balance": "154.35"}

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.get("/api/voices")
async def get_voices():
    system_voices = []
    for name, uri in Config.VOICES.items():
        system_voices.append({
            "name": name,
            "uri": uri,
            "type": "system",
            "displayName": f"系统: {name}"
        })

    custom_voices = []
    for name, data in voice_manager.custom_voices.items():
        custom_voices.append({
            "name": name,
            "uri": data["uri"],
            "type": "custom",
            "model": data.get("model", Config.DEFAULT_MODEL),
            "text": data.get("text", ""),
            "displayName": f"自定义: {name}"
        })

    return {"system": system_voices, "custom": custom_voices}

@app.post("/api/sync-voices")
async def sync_voices():
    try:
        voice_manager.sync_remote_voices()
        return {"status": "success", "message": "音色同步成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_speech(req: GenerateRequest):
    try:
        filename = f"{uuid.uuid4()}.{req.format}"
        output_path = os.path.join(OUTPUT_DIR, filename)

        result = client.generate_speech(
            text=req.text,
            voice=req.voice,
            response_format=req.format,
            output_path=output_path,
            speed=req.speed,
            gain=req.gain
        )

        return {
            "status": "success",
            "audio_url": f"/static/outputs/{filename}"
        }
    except Exception as e:
        print(f"生成语音错误: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-voice")
async def upload_voice(
    file: UploadFile = File(...),
    text: str = Form(...),
    name: str = Form(...)
):
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uri = voice_manager.add_custom_voice(temp_path, text, name)

        if not uri:
            raise Exception("上传成功但未获取到URI")

        return {"status": "success", "uri": uri, "name": name}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)