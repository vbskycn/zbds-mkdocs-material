---
hide:
  - toc
---

# 直播源格式转换器

<style>
/* 转换器容器的样式 */
.converter-container {
    background-color: #ffffff; /* 设置白色背景 */
    padding: 0.1rem 1.5rem; /* 设置内边距,上下0.1rem,左右1.5rem */
    border-radius: 4px; /* 添加圆角效果 */
    width: 100%; /* 设置宽度为100% */
    max-width: 100%; /* 确保不超过父容器宽度 */
    margin: 0.1rem 0; /* 上下外边距为1rem,左右为0 */
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24); /* 添加阴影效果 */
}

/* 转换器标题样式 */
.converter-title {
    font-size: 0.5rem; /* 设置字体大小 */
    font-weight: 500; /* 设置字体粗细 */
    margin-bottom: 1.5rem; /* 设置下外边距 */
    color: #3f51b5; /* 设置文字颜色为蓝色 */
}

/* 转换器各部分的样式 */
.converter-section {
    margin-bottom: 1rem; /* 设置下外边距,保持各部分之间的间距 */
}

/* 第一个部分的特殊样式 */
.converter-section:first-child {
    margin-top: -0.5rem; /* 为第一个部分添加负的上边距,减少顶部空间 */
}

/* 副标题样式 */
.converter-subtitle {
    font-size: 1.1rem; /* 设置字体大小 */
    font-weight: 500; /* 设置字体粗细 */
    margin-bottom: 0.75rem; /* 设置下外边距,减少副标题和表单之间的间距 */
    color: #424242; /* 设置文字颜色为深灰色 */
}

/* 表单样式 */
.converter-form {
    display: flex; /* 使用弹性布局 */
    flex-direction: column; /* 设置主轴方向为垂直 */
    gap: 0.75rem; /* 设置表单元素之间的间距 */
}

/* 输入框样式 */
.converter-input {
    width: 100%; /* 设置宽度为100% */
    padding: 0.6rem; /* 设置内边距 */
    border: 1px solid #e0e0e0; /* 设置边框样式 */
    border-radius: 4px; /* 添加圆角效果 */
    font-size: 0.9rem; /* 设置字体大小 */
    transition: border-color 0.2s; /* 添加边框颜色变化的过渡效果 */
}

/* 输入框焦点样式 */
.converter-input:focus {
    outline: none; /* 移除默认的焦点轮廓 */
    border-color: #3f51b5; /* 设置焦点时的边框颜色 */
}

/* 按钮通用样式 */
.converter-button {
    width: 100%; /* 设置宽度为100% */
    padding: 0.6rem; /* 设置内边距 */
    color: white; /* 设置文字颜色为白色 */
    border: none; /* 移除边框 */
    border-radius: 4px; /* 添加圆角效果 */
    font-size: 0.9rem; /* 设置字体大小 */
    font-weight: 500; /* 设置字体粗细 */
    cursor: pointer; /* 设置鼠标悬停时的光标样式 */
    transition: background-color 0.2s; /* 添加背景颜色变化的过渡效果 */
    margin-top: 0.25rem; /* 设置上外边距,减少按钮上方的额外间距 */
}

/* 蓝色按钮样式 */
.converter-button-blue {
    background-color: #3b82f6; /* 设置背景颜色为蓝色 */
}

/* 蓝色按钮悬停样式 */
.converter-button-blue:hover {
    background-color: #2563eb; /* 设置悬停时的背景颜色为深蓝色 */
}

/* 绿色按钮样式 */
.converter-button-green {
    background-color: #22c55e; /* 设置背景颜色为绿色 */
}

/* 绿色按钮悬停样式 */
.converter-button-green:hover {
    background-color: #16a34a; /* 设置悬停时的背景颜色为深绿色 */
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