# MD to PDF Converter

This folder contains a small local Markdown-to-PDF converter.

## GUI usage

Double-click:

```text
md-to-pdf.command
```

Then either choose a Markdown file with `Choose...`, or paste/type the `.md` file path directly into `Markdown file`. The output path is filled automatically and can be changed with `Save As...`.

## Command-line usage

After installation, use:

```bash
mdtopdf /path/to/input.md
```

This creates `/path/to/input.pdf` in the same folder as the Markdown file.

You can still call the Python script directly:

```bash
python3 md_to_pdf_converter.py /path/to/input.md
```

With a custom output path:

```bash
python3 md_to_pdf_converter.py /path/to/input.md -o /path/to/output.pdf
```

With a table of contents:

```bash
python3 md_to_pdf_converter.py /path/to/input.md --toc
```

## Notes

- Chinese font defaults to `PingFang SC`.
- English font defaults to `Times New Roman`.
- The converter uses `pandoc + xelatex`, which is good for Chinese, English, tables, and LaTeX-style formulas.
- Images referenced from the Markdown file are resolved relative to the Markdown file's folder.
