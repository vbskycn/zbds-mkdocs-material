---
hide:
  - toc
---

# 直播源格式转换器

<style>
.converter-container {
    background-color: #ffffff;
    padding: 1.5rem 1.5rem; /* 稍微减少上下内边距 */
    border-radius: 4px;
    width: 100%;
    max-width: 100%;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}
.converter-title {
    font-size: 0.5rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
    color: #3f51b5;
}
.converter-section {
    margin-bottom: 1.75rem; /* 保持部分之间的间距不变 */
}
.converter-section:first-child {
    margin-top: -0.5rem; /* 为第一个部分添加负的上边距 */
}
.converter-subtitle {
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 0.75rem; /* 稍微减少副标题和表单之间的间距 */
    color: #424242;
}
.converter-form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem; /* 稍微减少表单元素之间的间距 */
}
.converter-input {
    width: 100%;
    padding: 0.6rem; /* 稍微减少输入框的高度 */
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: border-color 0.2s;
}
.converter-input:focus {
    outline: none;
    border-color: #3f51b5;
}
.converter-button {
    width: 100%;
    padding: 0.6rem; /* 稍微减少按钮的高度 */
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
    margin-top: 0.25rem; /* 稍微减少按钮上方的额外间距 */
}
.converter-button-blue {
    background-color: #3b82f6;
}
.converter-button-blue:hover {
    background-color: #2563eb;
}
.converter-button-green {
    background-color: #22c55e;
}
.converter-button-green:hover {
    background-color: #16a34a;
}
</style>

<div class="converter-container">

    
    <div class="converter-section">
        <h3 class="converter-subtitle" style="color: #000000; font-weight: bold;">M3U 转 TXT（保留分组信息）</h3>
        <form id="m3u-to-txt-form" class="converter-form">
            <input type="file" id="m3u-file" accept=".m3u" required class="converter-input">
            <button type="submit" class="converter-button converter-button-blue">转换</button>
        </form>
    </div>

    <div class="converter-section">
        <h3 class="converter-subtitle" style="color: #000000; font-weight: bold;">TXT 转 M3U（保留分组信息）</h3>
        <form id="txt-to-m3u-form" class="converter-form">
            <input type="file" id="txt-file" accept=".txt" required class="converter-input">
            <input type="text" id="epg-url" placeholder="EPG URL (可选,默认为 https://epg.112114.xyz/pp.xml)" class="converter-input">
            <button type="submit" class="converter-button converter-button-green">转换</button>
        </form>
    </div>
</div>

<script>
function parseM3UToTXT(m3uContent) {
    console.log("Parsing M3U to TXT");
    const lines = m3uContent.split('\n');
    const channels = {};
    let currentGroup = '未分组';

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line.startsWith('#EXTINF:-1')) {
            const groupMatch = line.match(/group-title="([^"]*)"/);
            const nameMatch = line.match(/tvg-name="([^"]*)"/);
            const group = groupMatch ? groupMatch[1] : currentGroup;
            const name = nameMatch ? nameMatch[1] : line.split(',').pop();
            const url = lines[i + 1] ? lines[i + 1].trim() : '';

            if (!channels[group]) {
                channels[group] = [];
            }
            channels[group].push(`${name},${url}`);
            currentGroup = group;
        }
    }

    let txtContent = '';
    for (const [group, channelList] of Object.entries(channels)) {
        txtContent += `${group},#genre#\n`;
        txtContent += channelList.join('\n') + '\n\n';
    }

    return txtContent;
}

function convertTXTToM3U(txtContent, epgUrl) {
    console.log("Converting TXT to M3U");
    const defaultEpgUrl = "https://epg.112114.xyz/pp.xml";
    const lines = txtContent.split('\n');
    let m3uContent = `#EXTM3U x-tvg-url="${epgUrl || defaultEpgUrl}"\n`;
    let currentGenre = '未分类';

    for (const line of lines) {
        const trimmedLine = line.trim();
        if (trimmedLine.endsWith(',#genre#')) {
            currentGenre = trimmedLine.replace(',#genre#', '');
        } else if (trimmedLine && !trimmedLine.startsWith('#')) {
            const [channelName, channelUrl] = trimmedLine.split(',');
            const tvgLogo = `https://epg.112114.xyz/logo/${channelName}.png`;
            m3uContent += `#EXTINF:-1 group-title="${currentGenre}" tvg-name="${channelName}" tvg-logo="${tvgLogo}" epg-url="${epgUrl || defaultEpgUrl}",${channelName}\n`;
            m3uContent += `${channelUrl}\n`;
        }
    }

    return m3uContent;
}

function downloadFile(content, filename) {
    console.log("Downloading file:", filename);
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function getCurrentDateTime() {
    const now = new Date();
    return now.getFullYear() +
           ('0' + (now.getMonth() + 1)).slice(-2) +
           ('0' + now.getDate()).slice(-2) +
           ('0' + now.getHours()).slice(-2) +
           ('0' + now.getMinutes()).slice(-2) +
           ('0' + now.getSeconds()).slice(-2);
}

function getFileNameWithoutExtension(filename) {
    return filename.split('.').slice(0, -1).join('.');
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    const m3uForm = document.getElementById('m3u-to-txt-form');
    const txtForm = document.getElementById('txt-to-m3u-form');

    if (m3uForm) {
        m3uForm.addEventListener('submit', function(e) {
            console.log("M3U to TXT form submitted");
            e.preventDefault();
            const file = document.getElementById('m3u-file').files[0];
            if (!file) {
                console.error("No file selected");
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                const m3uContent = e.target.result;
                const txtContent = parseM3UToTXT(m3uContent);
                const originalName = getFileNameWithoutExtension(file.name);
                const newFileName = `${originalName}_${getCurrentDateTime()}.txt`;
                downloadFile(txtContent, newFileName);
            };
            reader.readAsText(file);
        });
    } else {
        console.error("M3U to TXT form not found");
    }

    if (txtForm) {
        txtForm.addEventListener('submit', function(e) {
            console.log("TXT to M3U form submitted");
            e.preventDefault();
            const file = document.getElementById('txt-file').files[0];
            if (!file) {
                console.error("No file selected");
                return;
            }
            const epgUrl = document.getElementById('epg-url').value.trim() || "https://epg.112114.xyz/pp.xml";
            const reader = new FileReader();
            reader.onload = function(e) {
                const txtContent = e.target.result;
                const m3uContent = convertTXTToM3U(txtContent, epgUrl);
                const originalName = getFileNameWithoutExtension(file.name);
                const newFileName = `${originalName}_${getCurrentDateTime()}.m3u`;
                downloadFile(m3uContent, newFileName);
            };
            reader.readAsText(file);
        });
    } else {
        console.error("TXT to M3U form not found");
    }
});
</script>