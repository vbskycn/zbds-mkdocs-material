---
hide:
  - toc
---

# 直播源格式转换器

<style>
.converter-container {
    background-color: #ffffff;
    padding: 2rem 1.5rem; /* 稍微增加上下内边距 */
    border-radius: 4px;
    width: 100%;
    max-width: 100%;
    margin: 1rem 0;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
}
.converter-title {
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 1.5rem;
    color: #3f51b5;
}
.converter-section {
    margin-bottom: 2rem; /* 增加部分之间的间距 */
}
.converter-subtitle {
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 1rem; /* 增加副标题和表单之间的间距 */
    color: #424242;
}
.converter-form {
    display: flex;
    flex-direction: column;
    gap: 1rem; /* 增加表单元素之间的间距 */
}
.converter-input {
    width: 100%;
    padding: 0.75rem; /* 增加输入框的高度 */
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
    padding: 0.75rem; /* 增加按钮的高度 */
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
    margin-top: 0.5rem; /* 在按钮上方添加一些额外的间距 */
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
    // ... 保持原有的函数实现 ...
}

function convertTXTToM3U(txtContent, epgUrl) {
    // ... 保持原有的函数实现 ...
}

function downloadFile(content, filename) {
    // ... 保持原有的函数实现 ...
}

function getCurrentDateTime() {
    // ... 保持原有的函数实现 ...
}

function getFileNameWithoutExtension(filename) {
    // ... 保持原有的函数实现 ...
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('m3u-to-txt-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const file = document.getElementById('m3u-file').files[0];
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

    document.getElementById('txt-to-m3u-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const file = document.getElementById('txt-file').files[0];
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
});
</script>