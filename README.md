# mdtopdf

`mdtopdf` 是一个本地 Markdown 转 PDF 小工具，支持 macOS 和 Windows。它可以把中文、英文、表格和 LaTeX 风格公式一起转成 PDF，底层使用 `pandoc + xelatex`，适合课程笔记、复习题库、实验报告和带公式的 Markdown 文档。

## 功能

- 终端命令：`mdtopdf /path/to/aaa.md`
- Windows 终端命令：`mdtopdf C:\path\to\aaa.md`
- 自动在 Markdown 同目录生成 PDF：`aaa.md` -> `aaa.pdf`
- GUI 小窗口：支持选择文件，也支持直接粘贴 Markdown 路径
- macOS 默认中文字体：`PingFang SC`
- Windows 默认中文字体：`Microsoft YaHei`
- 默认英文字体：`Times New Roman`
- 支持表格、标题元信息、美元符号公式和本地图片相对路径

## 依赖

本工具需要：

```bash
python3
pandoc
xelatex
```

其中 `xelatex` 通常来自 MacTeX、MiKTeX 或 TeX Live。

## macOS 安装

先检查依赖：

```bash
command -v python3
command -v pandoc
command -v xelatex
```

如果缺少 `pandoc`：

```bash
brew install pandoc
```

如果缺少 `xelatex`：

```bash
brew install --cask mactex
```

MacTeX 安装后，如果当前终端暂时找不到 `xelatex`，请打开一个新终端，或执行：

```bash
export PATH="/Library/TeX/texbin:$PATH"
```

克隆仓库：

```bash
git clone https://github.com/DreamsLastWish/mdtopdf.git
cd mdtopdf
```

安装 `mdtopdf` 命令：

```bash
chmod +x install.sh mdtopdf md-to-pdf.command
./install.sh
```

安装脚本会优先把 `mdtopdf` 链接到：

```text
/opt/homebrew/bin/mdtopdf
```

如果没有 `/opt/homebrew/bin`，会尝试使用：

```text
/usr/local/bin/mdtopdf
```

验证：

```bash
command -v mdtopdf
mdtopdf
```

如果刚安装完仍然找不到命令，请打开新终端，或执行：

```bash
rehash
```

## Windows 安装

先打开 PowerShell，检查依赖：

```powershell
python --version
pandoc --version
xelatex --version
```

如果缺少 Python，可以安装 Python 3：

```powershell
winget install --id Python.Python.3
```

如果缺少 Pandoc：

```powershell
winget install --id JohnMacFarlane.Pandoc
```

如果缺少 `xelatex`，推荐安装 MiKTeX：

```powershell
winget install --id MiKTeX.MiKTeX
```

安装完成后，重新打开 PowerShell，再检查：

```powershell
python --version
pandoc --version
xelatex --version
```

克隆仓库：

```powershell
git clone https://github.com/DreamsLastWish/mdtopdf.git
cd mdtopdf
```

安装 `mdtopdf` 命令：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

安装脚本会创建：

```text
%LOCALAPPDATA%\mdtopdf\bin\mdtopdf.bat
```

并把这个目录加入当前用户的 `PATH`。安装完成后，请打开一个新的 PowerShell 窗口，然后验证：

```powershell
where mdtopdf
mdtopdf
```

## 终端使用

macOS：

```bash
mdtopdf /Users/yourname/Documents/aaa.md
```

Windows：

```powershell
mdtopdf C:\Users\yourname\Documents\aaa.md
```

输出文件会自动生成在 Markdown 同目录：

```text
aaa.md -> aaa.pdf
```

如果路径里有空格，请加引号。

macOS：

```bash
mdtopdf "/Users/yourname/My Notes/aaa.md"
```

Windows：

```powershell
mdtopdf "C:\Users\yourname\My Notes\aaa.md"
```

也可以通过 Python 脚本直接运行：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md
```

Windows：

```powershell
python .\md_to_pdf_converter.py C:\path\to\aaa.md
```

指定输出路径：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md -o /path/to/result.pdf
```

生成目录：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md --toc
```

自定义字体：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md \
  --cjk-font "PingFang SC" \
  --main-font "Times New Roman" \
  --mono-font "Menlo"
```

Windows 可改成：

```powershell
python .\md_to_pdf_converter.py C:\path\to\aaa.md --cjk-font "Microsoft YaHei"
```

## GUI 使用

macOS 双击：

```text
md-to-pdf.command
```

Windows 可以运行：

```powershell
python .\md_to_pdf_converter.py
```

打开窗口后有两种输入方式：

1. 点击 `Choose...` 选择 Markdown 文件
2. 直接把 `.md` 文件路径粘贴到 `Markdown file`

输出 PDF 路径会自动填好，也可以用 `Save As...` 修改。

## Markdown 写法示例

```markdown
---
title: 测试文档
author: mdtopdf
---

# 中文与 English

这是一段中文。

This is an English paragraph.

$$
\dot{x}(t)=-Lx(t)
$$

| 项目 | Result |
|---|---|
| 中文 | 正常 |
| English | OK |
```

运行：

```bash
mdtopdf /path/to/test.md
```

即可得到：

```text
/path/to/test.pdf
```

## 常见问题

### `mdtopdf: command not found`

macOS 先确认安装脚本是否执行过：

```bash
./install.sh
```

再确认终端能找到命令：

```bash
command -v mdtopdf
```

如果刚安装完仍然找不到，打开新终端，或执行：

```bash
rehash
```

### Windows 提示找不到 `mdtopdf`

重新打开一个 PowerShell 窗口，再运行：

```powershell
where mdtopdf
```

如果仍然找不到，请重新执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

### `Missing required tool: pandoc`

macOS：

```bash
brew install pandoc
```

Windows：

```powershell
winget install --id JohnMacFarlane.Pandoc
```

### `Missing required tool: xelatex`

macOS：

```bash
brew install --cask mactex
```

Windows：

```powershell
winget install --id MiKTeX.MiKTeX
```

安装后请打开新终端，再检查：

```bash
xelatex --version
```

### 中文乱码或字体报错

macOS 默认使用 `PingFang SC`，Windows 默认使用 `Microsoft YaHei`。如果系统里没有对应字体，可以换成其它中文字体。

macOS 示例：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md --cjk-font "Songti SC"
```

Windows 示例：

```powershell
python .\md_to_pdf_converter.py C:\path\to\aaa.md --cjk-font "SimSun"
```

### 图片无法显示

图片路径建议写成相对 Markdown 文件所在目录的路径，例如：

```markdown
![diagram](images/diagram.png)
```

转换时程序会把 Markdown 所在目录作为资源目录。

## 卸载

macOS 如果安装到了 `/opt/homebrew/bin`：

```bash
rm /opt/homebrew/bin/mdtopdf
```

macOS 如果安装到了 `/usr/local/bin`：

```bash
rm /usr/local/bin/mdtopdf
```

Windows：

```powershell
Remove-Item "$env:LOCALAPPDATA\mdtopdf\bin\mdtopdf.bat"
```

然后可以在“系统属性 -> 环境变量”里从当前用户的 `Path` 删除：

```text
%LOCALAPPDATA%\mdtopdf\bin
```

卸载只会删除终端命令，不会删除本仓库文件。

