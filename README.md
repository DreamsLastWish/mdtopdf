# mdtopdf

`mdtopdf` 是一个 macOS 本地 Markdown 转 PDF 小工具，支持中文、英文、表格和 LaTeX 风格公式。它底层使用 `pandoc + xelatex`，所以比简单的浏览器打印更适合中文资料、课程笔记、复习题库和带公式的 Markdown。

## 功能

- 终端命令：`mdtopdf /path/to/aaa.md`
- 自动在 Markdown 同目录生成 PDF：`/path/to/aaa.pdf`
- GUI 小窗口：支持选择文件，也支持直接粘贴 Markdown 路径
- 默认中文字体：`PingFang SC`
- 默认英文字体：`Times New Roman`
- 默认等宽字体：`Menlo`
- 支持表格、标题元信息、美元符号公式和本地图片相对路径

## 安装前准备

本工具需要 3 个东西：

```bash
python3
pandoc
xelatex
```

先检查是否已经安装：

```bash
command -v python3
command -v pandoc
command -v xelatex
```

如果三条命令都能输出路径，就可以直接进入“安装 mdtopdf”。

如果缺少 `pandoc`，用 Homebrew 安装：

```bash
brew install pandoc
```

如果缺少 `xelatex`，安装 MacTeX：

```bash
brew install --cask mactex
```

MacTeX 安装后，如果当前终端暂时找不到 `xelatex`，请打开一个新终端，或执行：

```bash
export PATH="/Library/TeX/texbin:$PATH"
```

## 安装 mdtopdf

克隆仓库：

```bash
git clone https://github.com/DreamsLastWish/mdtopdf.git
cd mdtopdf
```

给脚本执行权限：

```bash
chmod +x install.sh mdtopdf md-to-pdf.command
```

运行安装脚本：

```bash
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

安装完成后，验证命令是否可用：

```bash
command -v mdtopdf
mdtopdf
```

如果 `command -v mdtopdf` 没有输出，但安装脚本显示成功，请打开新终端，或执行：

```bash
rehash
```

## 终端使用

最常用命令：

```bash
mdtopdf /Users/yourname/Documents/aaa.md
```

输出文件会自动生成在同一个文件夹：

```text
/Users/yourname/Documents/aaa.pdf
```

如果路径里有空格，请加引号：

```bash
mdtopdf "/Users/yourname/My Notes/aaa.md"
```

也可以通过 Python 脚本直接运行：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md
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

## GUI 使用

双击：

```text
md-to-pdf.command
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

先确认安装脚本是否执行过：

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

### `Missing required tool: pandoc`

安装 pandoc：

```bash
brew install pandoc
```

### `Missing required tool: xelatex`

安装 MacTeX：

```bash
brew install --cask mactex
```

然后打开新终端，再检查：

```bash
command -v xelatex
```

### 中文乱码或字体报错

默认使用 macOS 自带的 `PingFang SC`。如果系统里没有这个字体，可以换成其它中文字体：

```bash
python3 md_to_pdf_converter.py /path/to/aaa.md --cjk-font "Songti SC"
```

### 图片无法显示

图片路径建议写成相对 Markdown 文件所在目录的路径，例如：

```markdown
![diagram](images/diagram.png)
```

转换时程序会把 Markdown 所在目录作为资源目录。

## 卸载

如果安装到了 `/opt/homebrew/bin`：

```bash
rm /opt/homebrew/bin/mdtopdf
```

如果安装到了 `/usr/local/bin`：

```bash
rm /usr/local/bin/mdtopdf
```

卸载只会删除终端命令链接，不会删除本仓库文件。

