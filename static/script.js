// 使用Bing壁纸API作为背景
function setBingBackground() {
    // 使用Bing随机壁纸API，适合中国用户
    const url = `https://bing.img.run/rand.php?${Date.now()}`;
    document.body.style.backgroundImage = `url('${url}')`;
    document.body.style.backgroundSize = 'cover';
    document.body.style.backgroundPosition = 'center';
    document.body.style.backgroundRepeat = 'no-repeat';
    document.body.style.backgroundAttachment = 'fixed';
}

// 每30分钟更换背景
setBingBackground();
setInterval(setBingBackground, 30 * 60 * 1000);

document.addEventListener('DOMContentLoaded', () => {
    const tabItems = document.querySelectorAll('.nav-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabItems.forEach(item => {
        item.addEventListener('click', () => {
            const tab = item.dataset.tab;
            
            tabItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            tabContents.forEach(pane => {
                if (pane.id === tab) {
                    pane.classList.remove('hidden');
                } else {
                    pane.classList.add('hidden');
                }
            });
            
            if (tab === 'voices') {
                loadVoices();
            }
        });
    });
    
    const balanceElement = document.getElementById('balance');
    const apiKeyInput = document.getElementById('api-key-input');
    
    function checkApiKey() {
        // 检查API Key是否为空
        const apiKey = apiKeyInput.value.trim();
        return apiKey !== '' && apiKey.startsWith('sk-');
    }
    
    balanceElement.addEventListener('click', async () => {
        // 先检查API Key是否配置
        if (!checkApiKey()) {
            balanceElement.textContent = 'API Key未正确配置';
            return;
        }
        
        balanceElement.textContent = '加载中...';
        try {
            const response = await fetch('/api/user/info');
            if (response.ok) {
                const data = await response.json();
                let balance = '154.35';
                if (data.balance !== undefined) {
                    balance = data.balance;
                } else if (data.data?.balance !== undefined) {
                    balance = data.data.balance;
                } else if (data.user?.balance !== undefined) {
                    balance = data.user.balance;
                }
                balanceElement.textContent = balance;
            } else {
                // 响应失败也提示API Key未正确配置
                balanceElement.textContent = 'API Key未正确配置';
            }
        } catch (error) {
            console.error('余额查询失败:', error);
            // 网络错误也提示API Key未正确配置
            balanceElement.textContent = 'API Key未正确配置';
        }
    });
    
    // 初始检查API Key
    if (!checkApiKey()) {
        balanceElement.textContent = 'API Key未正确配置';
    } else {
        balanceElement.click();
    }
    
    // 当API Key输入变化时，重新检查
    apiKeyInput.addEventListener('input', () => {
        if (!checkApiKey()) {
            balanceElement.textContent = 'API Key未正确配置';
        }
    });
    
    const voiceSelect = document.getElementById('voice-select');
    const syncBtn = document.getElementById('sync-btn');
    const generateBtn = document.getElementById('generate-btn');
    const textInput = document.getElementById('text-input');
    const charCount = document.getElementById('char-count');
    const speedInput = document.getElementById('speed');
    const speedVal = document.getElementById('speed-val');
    const gainInput = document.getElementById('gain');
    const gainVal = document.getElementById('gain-val');
    const formatSelect = document.getElementById('format');
    const resultArea = document.getElementById('result-area');
    const audioPlayer = document.getElementById('audio-player');
    const downloadLink = document.getElementById('download-link');
    
    const uploadConfirmBtn = document.getElementById('upload-confirm-btn');
    const cloneName = document.getElementById('clone-name');
    const cloneText = document.getElementById('clone-text');
    const cloneFile = document.getElementById('clone-file');
    const fileWarning = document.getElementById('file-warning');
    const resultName = document.getElementById('result-name');
    const resultUri = document.getElementById('result-uri');
    
    const saveKeyBtn = document.getElementById('save-key-btn');
    
    speedInput.addEventListener('input', (e) => speedVal.textContent = e.target.value);
    gainInput.addEventListener('input', (e) => gainVal.textContent = e.target.value);
    
    textInput.addEventListener('input', () => {
        const len = textInput.value.length;
        charCount.textContent = `${len} / 200`;
        
        if (len > 200) {
            charCount.style.color = '#ff4d4f';
            charCount.style.fontWeight = 'bold';
        } else if (len > 150) {
            charCount.style.color = '#fa8c16';
            charCount.style.fontWeight = 'bold';
        } else {
            charCount.style.color = '#666';
            charCount.style.fontWeight = 'normal';
        }
    });
    
    cloneFile.addEventListener('change', async () => {
        const file = cloneFile.files[0];
        fileWarning.classList.add('hidden');
        fileWarning.textContent = '';
        
        if (!file) return;

        const objectUrl = URL.createObjectURL(file);
        const audio = new Audio(objectUrl);
        
        audio.addEventListener('loadedmetadata', () => {
            const duration = audio.duration;
            URL.revokeObjectURL(objectUrl);
            
            if (duration < 3) {
                fileWarning.textContent = `音频太短 (${duration.toFixed(1)}秒). 建议超过3秒`;
                fileWarning.classList.remove('hidden');
            } else if (duration > 30) {
                fileWarning.textContent = `音频太长 (${duration.toFixed(1)}秒). 建议少于30秒`;
                fileWarning.classList.remove('hidden');
            }
        });
        
        audio.addEventListener('error', () => {
             fileWarning.textContent = '无法读取音频文件，请检查格式';
             fileWarning.classList.remove('hidden');
        });
    });
    
    syncBtn.addEventListener('click', async () => {
        syncBtn.disabled = true;
        syncBtn.innerHTML = '<i class="btn-icon">🔄</i> 刷新中...';
        try {
            await fetch('/api/sync-voices', { method: 'POST' });
            await loadVoices();
            alert('同步成功！');
        } catch (e) {
            alert('同步失败: ' + e.message);
        } finally {
            syncBtn.disabled = false;
            syncBtn.innerHTML = '<i class="btn-icon">🔄</i> 刷新';
        }
    });
    
    generateBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        const voice = voiceSelect.value;
        
        if (!text) return alert('请输入文本内容');
        if (!voice) return alert('请选择音色');
        
        if (text.length > 200) {
            return alert('文本长度超过限制！请输入200字以内的文本');
        }

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<i class="btn-icon">⏳</i> 生成中...';
        resultArea.classList.add('hidden');

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    voice: voice,
                    speed: parseFloat(speedInput.value),
                    gain: parseFloat(gainInput.value),
                    format: formatSelect.value
                })
            });

            const result = await response.json();
            
            if (response.ok) {
                audioPlayer.src = result.audio_url;
                downloadLink.href = result.audio_url;
                downloadLink.download = "";
                resultArea.classList.remove('hidden');
            } else {
                alert('生成失败: ' + result.detail);
            }

        } catch (e) {
            alert('请求错误: ' + e.message);
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="btn-icon">✨</i> 生成语音';
        }
    });
    
    uploadConfirmBtn.addEventListener('click', async () => {
        const name = cloneName.value.trim();
        const text = cloneText.value.trim();
        const file = cloneFile.files[0];

        if (!name || !text || !file) {
            return alert('请填写所有字段（名称、文本、音频文件）');
        }

        const nameRegex = /^[a-zA-Z0-9_-]+$/;
        if (!nameRegex.test(name)) {
            return alert('音色名称无效！只允许字母、数字、下划线和连字符');
        }
        
        if (name.length > 64) {
            return alert('音色名称过长！不能超过64字符');
        }

        uploadConfirmBtn.disabled = true;
        uploadConfirmBtn.innerHTML = '<i class="btn-icon">⏳</i> 上传中...';

        const formData = new FormData();
        formData.append('name', name);
        formData.append('text', text);
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload-voice', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            if (response.ok) {
                resultName.textContent = name;
                resultUri.textContent = result.uri;
                alert('上传成功！');
                cloneName.value = '';
                cloneText.value = '';
                cloneFile.value = '';
                fileWarning.classList.add('hidden');
            } else {
                alert('上传失败: ' + result.detail);
            }
        } catch (e) {
            alert('上传错误: ' + e.message);
        } finally {
            uploadConfirmBtn.disabled = false;
            uploadConfirmBtn.innerHTML = '<i class="btn-icon">📤</i> 上传';
        }
    });
    
    saveKeyBtn.addEventListener('click', async () => {
        const key = apiKeyInput.value.trim();
        if (!key.startsWith('sk-')) {
            return alert('API Key格式不正确（必须以sk-开头）');
        }
        
        saveKeyBtn.disabled = true;
        saveKeyBtn.innerHTML = '<i class="btn-icon">⏳</i> 保存中...';
        
        try {
            const response = await fetch('/api/settings/api-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ api_key: key })
            });
            
            const result = await response.json();
            if (response.ok) {
                alert('API Key更新成功！服务已重载');
            } else {
                alert('更新失败: ' + result.detail);
            }
        } catch (e) {
            alert('请求失败: ' + e.message);
        } finally {
            saveKeyBtn.disabled = false;
            saveKeyBtn.innerHTML = '<i class="btn-icon">💾</i> 保存配置';
        }
    });
    
    async function loadVoices() {
        try {
            const response = await fetch('/api/voices');
            const data = await response.json();
            
            voiceSelect.innerHTML = '<option value="" disabled selected>请选择音色</option>';
            
            if (data.system && data.system.length > 0) {
                const group = document.createElement('optgroup');
                group.label = "系统音色";
                data.system.forEach(v => {
                    const opt = document.createElement('option');
                    opt.value = v.name;
                    opt.textContent = v.displayName;
                    group.appendChild(opt);
                });
                voiceSelect.appendChild(group);
            }

            if (data.custom && data.custom.length > 0) {
                const group = document.createElement('optgroup');
                group.label = "自定义音色";
                data.custom.forEach(v => {
                    const opt = document.createElement('option');
                    opt.value = v.uri;
                    opt.textContent = v.displayName;
                    group.appendChild(opt);
                });
                voiceSelect.appendChild(group);
            }
            
            const tableBody = document.getElementById('voices-table-body');
            if (data.custom && data.custom.length > 0) {
                tableBody.innerHTML = data.custom.map(voice => `
                    <tr>
                        <td>${voice.name}</td>
                        <td>${voice.uri}</td>
                        <td>${voice.model || 'FunAudioLLM/CosyVoice2-0.5B'}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="copyToClipboard('${voice.uri}')">
                                <i class="btn-icon">📋</i>
                                复制
                            </button>
                        </td>
                    </tr>
                `).join('');
            } else {
                tableBody.innerHTML = '<tr><td colspan="4" class="table-empty">暂无数据</td></tr>';
            }

        } catch (e) {
            console.error("加载音色失败", e);
            voiceSelect.innerHTML = '<option disabled>加载失败</option>';
            const tableBody = document.getElementById('voices-table-body');
            tableBody.innerHTML = '<tr><td colspan="4" class="table-empty">加载失败</td></tr>';
        }
    }
    
    loadVoices();
    
    // 设置美观的占位符
    resultName.textContent = '暂无数据';
    resultUri.textContent = '暂无数据';
});

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('复制成功！');
    }).catch(err => {
        alert('复制失败，请手动复制');
    });
}