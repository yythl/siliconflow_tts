# SiliconFlow TTS Studio

基于硅基流动（SiliconFlow）API 的文本转语音工具，支持自定义音色训练和多种系统音色。
本项目需要注册登录硅基流动，硅基流动登录注册页面：https://cloud.siliconflow.cn/i/tyNkWQeb 填写我的邀请码：tyNkWQeb 领取16元免费额度

## 功能特点

- 🎙️ **文本转语音** - 支持 FunAudioLLM/CosyVoice2-0.5B 模型
- 🎤 **音色训练** - 上传音频文件训练自定义音色
- 🎵 **系统音色** - 内置 8 种系统预置音色
- 📊 **音色管理** - 查看和管理所有音色
- ⚙️ **API 配置** - 支持在线修改 API Key
- 💰 **余额查询** - 实时查询账户余额
- 本项目提供前端UI界面，便于使用。页面背景调用bing图片api，不喜欢可以点击导航栏左上角四叶草🍀刷新背景
<img width="1910" height="873" alt="PixPin_2026-04-23_03-17-48" src="https://github.com/user-attachments/assets/b84f9ec6-28f5-433b-8e5e-09ab36046890" />
<img width="1910" height="873" alt="PixPin_2026-04-23_03-18-02" src="https://github.com/user-attachments/assets/136fa7d1-0a87-4b62-b459-51674531e10e" />
<img width="1910" height="873" alt="PixPin_2026-04-23_03-18-14" src="https://github.com/user-attachments/assets/93d6f649-a69a-493d-93ec-9bee758997cd" />
<img width="1910" height="873" alt="PixPin_2026-04-23_03-18-44" src="https://github.com/user-attachments/assets/68ad56fc-f147-42ce-af88-2f5631d29e69" />


## 系统预置音色

| 性别 | 名称 | 描述 |
|------|------|------|
| 男声 | alex | 沉稳男声 |
| 男声 | benjamin | 低沉男声 |
| 男声 | charles | 磁性男声 |
| 男声 | david | 欢快男声 |
| 女声 | anna | 沉稳女声 |
| 女声 | bella | 激情女声 |
| 女声 | claire | 温柔女声 |
| 女声 | diana | 欢快女声 |

## 安装依赖

### 环境要求

- Python 3.8+
- pip 包管理器

## 安装步骤（两种任选一种）

### 安装方式一

1.直接点击链接https://github.com/yythl/siliconflow_tts/releases/download/siliconflow_tts/siliconflow_tts.1.0.0.zip下载压缩包

2.解压到任意位置，双击"启动应用.bat"会自动自检安装环境，并打开浏览器前端页面

### 安装方式二

1. **克隆项目**
```bash
git clone <repository-url>
cd siliconflow_tts
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API Key**
```bash
# 编辑 .env 文件，填入你的 API Key
SILICONFLOW_API_KEY=your_api_key_here
```

4. **启动服务**
```bash
python launcher.py
```

或者双击 `启动应用.bat` 快速启动。

## 使用说明

### 上传自定义音色

1. 点击左侧菜单"上传音色"
2. 选择音频文件（建议 8-10 秒，发音清晰，最多30s，超过30s会拦截）
3. 输入音色名称（只支持英文、数字、下划线、连字符）
4. 输入参考文本（音频对应的文字内容，懒得打字可以搜一个提供stt服务的网站，比如https://turboscribe.ai/zh-CN/dashboard）
5. 点击"上传"按钮
6. 上传成功后，音色会自动同步到云端

### 文本转语音

1. 点击左侧菜单"文本转语音"
2. 选择模型（FunAudioLLM/CosyVoice2-0.5B）
3. 选择音色（系统音色或自定义音色）
4. 输入文本内容（最多 200 字，约 30 秒音频）
5. 调整语速和音量参数
6. 选择输出格式（MP3/WAV）
7. 点击"生成语音"按钮
8. 生成完成后可在线播放或下载音频

### 音色管理

1. 点击左侧菜单"音色管理"
2. 点击"刷新"按钮同步云端音色
3. 可查看所有自定义音色的名称、URI、模型信息
4. 点击"复制"按钮复制音色 URI

### API 配置

1. 点击左侧菜单"API 配置"
2. 输入新的 API Key
3. 点击"保存配置"按钮
4. 服务会自动重载

## API 文档

本项目基于硅基流动官方 API 文档开发：

- [文本转语音 API 文档](https://docs.siliconflow.cn/cn/userguide/capabilities/text-to-speech)
- [音色上传 API 文档](https://docs.siliconflow.cn/cn/userguide/capabilities/text-to-speech#_2-2-用户预置音色)

## 项目结构

```
siliconflow_tts/
├── src/
│   ├── __init__.py          # 包初始化
│   ├── api.py               # FastAPI 后端接口
│   ├── client.py            # SiliconFlow API 客户端
│   ├── config.py            # 配置管理
│   └── voice_manager.py     # 音色管理
├── static/
│   ├── index.html           # 前端页面
│   ├── style.css           # 样式文件
│   ├── script.js            # JavaScript 脚本
│   └── outputs/            # 生成的音频文件
├── .env                    # 环境变量配置
├── .gitignore              # Git 忽略文件
├── launcher.py             # 启动脚本
├── requirements.txt         # Python 依赖
└── 启动应用.bat             # Windows 快速启动
```

## 配置说明

### 环境变量 (.env)

```env
SILICONFLOW_API_KEY=your_api_key_here
```

硅基流动登录注册 [硅基流动登录注册](https://cloud.siliconflow.cn/i/tyNkWQeb) 
你可以在 [硅基流动控制台](https://cloud.siliconflow.cn/account/ak) 获取 API Key。

## 注意事项

- 自定义音色名称只支持英文、数字、下划线和连字符
- 文本转语音限制 200 字（约 30 秒音频），超出部分会被截断
- 上传的音频文件建议 8-10 秒，发音清晰，无背景噪音
- 请确保 API Key 有足够的额度

## 常见问题

### Q: 提示 "audio longer than 30s is not supported"

A: 这是因为生成的音频超过了 30 秒限制。请减少输入文本长度，建议控制在 200 字以内。

### Q: 上传音色失败

A: 请检查：
1. 音频文件格式是否正确（支持 mp3、wav 等常见格式）
2. 音色名称是否只包含英文、数字、下划线、连字符
3. 参考文本是否与音频内容一致
4. API Key 是否有权限

### Q: 余额查询失败

A: 请检查 API Key 是否正确，或稍后重试。

## 技术栈

- **后端**: FastAPI + Python 3.8+
- **前端**: HTML5 + CSS3 + JavaScript
- **API**: SiliconFlow API;Bing API

## 免责声明

本项目仅供学习和研究使用，严禁商业售卖。生成内容使用请遵守硅基流动的服务条款和相关法律法规。

## Star History

如果你觉得这个项目对你有帮助，欢迎给个 Star！⭐
联系我：邮箱3127695049@qq.com

## License

MIT License
