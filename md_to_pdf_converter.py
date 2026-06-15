#!/usr/bin/env python3
"""Small local Markdown-to-PDF converter with GUI and CLI modes."""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import threading
from pathlib import Path
from shutil import which


APP_NAME = "MD to PDF Converter"
DEFAULT_MARGIN = "2cm"


def default_cjk_font() -> str:
    if os.name == "nt":
        return "Microsoft YaHei"
    if sys.platform == "darwin":
        return "PingFang SC"
    return "Noto Sans CJK SC"


def default_mono_font() -> str:
    if os.name == "nt":
        return "Consolas"
    if sys.platform == "darwin":
        return "Menlo"
    return "DejaVu Sans Mono"


DEFAULT_CJK_FONT = default_cjk_font()
DEFAULT_MAIN_FONT = "Times New Roman"
DEFAULT_MONO_FONT = default_mono_font()


def extra_paths() -> list[str]:
    if os.name != "nt":
        return [
            "/opt/homebrew/bin",
            "/usr/local/bin",
            "/Library/TeX/texbin",
            "/opt/anaconda3/bin",
            "/usr/bin",
            "/bin",
            "/usr/sbin",
            "/sbin",
        ]

    candidates: list[Path] = []
    program_files = [os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")]
    local_app_data = os.environ.get("LOCALAPPDATA")

    for base in program_files:
        if not base:
            continue
        root = Path(base)
        candidates.extend(
            [
                root / "Pandoc",
                root / "MiKTeX" / "miktex" / "bin" / "x64",
                root / "MiKTeX" / "miktex" / "bin",
            ]
        )

    if local_app_data:
        candidates.extend(
            [
                Path(local_app_data) / "Pandoc",
                Path(local_app_data) / "Programs" / "MiKTeX" / "miktex" / "bin" / "x64",
                Path(local_app_data) / "Programs" / "MiKTeX" / "miktex" / "bin",
            ]
        )

    for year in range(2020, 2031):
        candidates.append(Path(f"C:/texlive/{year}/bin/windows"))

    return [str(path) for path in candidates if path.exists()]


def ensure_path() -> None:
    current = os.environ.get("PATH", "")
    parts = [p for p in extra_paths() if p and p not in current.split(os.pathsep)]
    if parts:
        os.environ["PATH"] = os.pathsep.join(parts + [current])


def find_tool(name: str) -> str:
    ensure_path()
    found = which(name)
    if not found:
        raise RuntimeError(
            f"Missing required tool: {name}\n"
            "Install pandoc and a TeX engine first.\n"
            "macOS:\n"
            "  brew install pandoc\n"
            "  brew install --cask mactex\n"
            "Windows:\n"
            "  winget install --id JohnMacFarlane.Pandoc\n"
            "  winget install --id MiKTeX.MiKTeX"
        )
    return found


def open_pdf(path: Path) -> None:
    if os.name == "nt":
        os.startfile(str(path))  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(path)])
        return
    subprocess.Popen(["xdg-open", str(path)])


def default_output_path(md_path: Path) -> Path:
    return md_path.with_suffix(".pdf")


def convert_md_to_pdf(
    md_path: str | Path,
    output_path: str | Path | None = None,
    *,
    cjk_font: str = DEFAULT_CJK_FONT,
    main_font: str = DEFAULT_MAIN_FONT,
    mono_font: str = DEFAULT_MONO_FONT,
    margin: str = DEFAULT_MARGIN,
    toc: bool = False,
) -> tuple[Path, str]:
    md = Path(str(md_path).strip().strip("\"'")).expanduser()
    if not md.exists():
        raise FileNotFoundError(f"Markdown file does not exist: {md}")
    if not md.is_file():
        raise ValueError(f"Input path is not a file: {md}")
    if md.suffix.lower() not in {".md", ".markdown", ".mdown"}:
        raise ValueError(f"Input file should be a Markdown file: {md}")

    out = Path(str(output_path).strip().strip("\"'")).expanduser() if output_path else default_output_path(md)
    if out.suffix.lower() != ".pdf":
        out = out.with_suffix(".pdf")
    out.parent.mkdir(parents=True, exist_ok=True)

    pandoc = find_tool("pandoc")
    xelatex = find_tool("xelatex")

    cmd = [
        pandoc,
        str(md),
        "--standalone",
        "--from",
        "markdown+tex_math_dollars+yaml_metadata_block+pipe_tables+raw_tex",
        "--pdf-engine",
        xelatex,
        "--resource-path",
        str(md.parent),
        "-V",
        f"CJKmainfont={cjk_font}",
        "-V",
        f"mainfont={main_font}",
        "-V",
        f"monofont={mono_font}",
        "-V",
        f"geometry:a4paper,margin={margin}",
        "-o",
        str(out),
    ]
    if toc:
        cmd.insert(2, "--toc")

    result = subprocess.run(
        cmd,
        cwd=str(md.parent),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    command_text = " ".join(shlex.quote(part) for part in cmd)
    log = f"$ {command_text}\n\n{result.stdout}".strip()
    if result.returncode != 0:
        raise RuntimeError(log or "Pandoc failed without output.")
    if not out.exists():
        raise RuntimeError("Pandoc finished, but the PDF was not created.")
    return out, log


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF using pandoc + xelatex.")
    parser.add_argument("input", nargs="?", help="Markdown file path. If omitted, the GUI opens.")
    parser.add_argument("-o", "--output", help="Output PDF path. Defaults to the input file with .pdf.")
    parser.add_argument("--toc", action="store_true", help="Add a table of contents.")
    parser.add_argument("--cjk-font", default=DEFAULT_CJK_FONT, help=f"Chinese font, default: {DEFAULT_CJK_FONT}")
    parser.add_argument("--main-font", default=DEFAULT_MAIN_FONT, help=f"Latin font, default: {DEFAULT_MAIN_FONT}")
    parser.add_argument("--mono-font", default=DEFAULT_MONO_FONT, help=f"Monospace font, default: {DEFAULT_MONO_FONT}")
    parser.add_argument("--margin", default=DEFAULT_MARGIN, help=f"Page margin, default: {DEFAULT_MARGIN}")
    return parser.parse_args(argv)


def run_cli(args: argparse.Namespace) -> int:
    try:
        out, log = convert_md_to_pdf(
            args.input,
            args.output,
            cjk_font=args.cjk_font,
            main_font=args.main_font,
            mono_font=args.mono_font,
            margin=args.margin,
            toc=args.toc,
        )
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(log)
    print(f"\nCreated: {out}")
    return 0


def run_gui() -> int:
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
    except Exception as exc:
        print(f"Tkinter is unavailable: {exc}", file=sys.stderr)
        return 1

    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("760x560")
    root.minsize(680, 500)

    input_var = tk.StringVar()
    output_var = tk.StringVar()
    cjk_var = tk.StringVar(value=DEFAULT_CJK_FONT)
    main_var = tk.StringVar(value=DEFAULT_MAIN_FONT)
    mono_var = tk.StringVar(value=DEFAULT_MONO_FONT)
    margin_var = tk.StringVar(value=DEFAULT_MARGIN)
    toc_var = tk.BooleanVar(value=False)
    open_var = tk.BooleanVar(value=True)
    status_var = tk.StringVar(value="Ready")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    frame = ttk.Frame(root, padding=18)
    frame.grid(row=0, column=0, sticky="nsew")
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(8, weight=1)

    def set_default_output(*_args: object) -> None:
        raw = input_var.get().strip().strip("\"'")
        if not raw:
            return
        try:
            output_var.set(str(default_output_path(Path(raw).expanduser())))
        except Exception:
            pass

    def choose_input() -> None:
        path = filedialog.askopenfilename(
            title="Choose Markdown file",
            filetypes=[("Markdown files", "*.md *.markdown *.mdown"), ("All files", "*.*")],
        )
        if path:
            input_var.set(path)
            set_default_output()

    def choose_output() -> None:
        initial = output_var.get() or None
        path = filedialog.asksaveasfilename(
            title="Choose output PDF",
            initialfile=Path(initial).name if initial else "output.pdf",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
        )
        if path:
            output_var.set(path)

    ttk.Label(frame, text="Markdown file").grid(row=0, column=0, sticky="w", pady=(0, 6))
    input_entry = ttk.Entry(frame, textvariable=input_var)
    input_entry.grid(row=0, column=1, sticky="ew", padx=(12, 8), pady=(0, 6))
    ttk.Button(frame, text="Choose...", command=choose_input).grid(row=0, column=2, sticky="ew", pady=(0, 6))

    ttk.Label(frame, text="Output PDF").grid(row=1, column=0, sticky="w", pady=6)
    ttk.Entry(frame, textvariable=output_var).grid(row=1, column=1, sticky="ew", padx=(12, 8), pady=6)
    ttk.Button(frame, text="Save As...", command=choose_output).grid(row=1, column=2, sticky="ew", pady=6)

    ttk.Separator(frame).grid(row=2, column=0, columnspan=3, sticky="ew", pady=14)

    ttk.Label(frame, text="Chinese font").grid(row=3, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=cjk_var).grid(row=3, column=1, sticky="ew", padx=(12, 8), pady=4)

    ttk.Label(frame, text="English font").grid(row=4, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=main_var).grid(row=4, column=1, sticky="ew", padx=(12, 8), pady=4)

    ttk.Label(frame, text="Mono font").grid(row=5, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=mono_var).grid(row=5, column=1, sticky="ew", padx=(12, 8), pady=4)

    ttk.Label(frame, text="Margin").grid(row=6, column=0, sticky="w", pady=4)
    ttk.Entry(frame, textvariable=margin_var).grid(row=6, column=1, sticky="w", padx=(12, 8), pady=4)

    options = ttk.Frame(frame)
    options.grid(row=7, column=1, columnspan=2, sticky="w", padx=(12, 0), pady=(6, 10))
    ttk.Checkbutton(options, text="Table of contents", variable=toc_var).grid(row=0, column=0, sticky="w")
    ttk.Checkbutton(options, text="Open PDF after conversion", variable=open_var).grid(row=0, column=1, sticky="w", padx=(18, 0))

    log_box = tk.Text(frame, height=10, wrap="word")
    log_box.grid(row=8, column=0, columnspan=3, sticky="nsew", pady=(8, 8))

    controls = ttk.Frame(frame)
    controls.grid(row=9, column=0, columnspan=3, sticky="ew")
    controls.columnconfigure(0, weight=1)
    ttk.Label(controls, textvariable=status_var).grid(row=0, column=0, sticky="w")

    convert_button = ttk.Button(controls, text="Convert to PDF")
    convert_button.grid(row=0, column=1, sticky="e")

    def append_log(text: str) -> None:
        log_box.insert("end", text + "\n")
        log_box.see("end")

    def set_busy(is_busy: bool) -> None:
        convert_button.configure(state="disabled" if is_busy else "normal")
        status_var.set("Converting..." if is_busy else "Ready")

    def worker() -> None:
        try:
            out, log = convert_md_to_pdf(
                input_var.get(),
                output_var.get() or None,
                cjk_font=cjk_var.get().strip() or DEFAULT_CJK_FONT,
                main_font=main_var.get().strip() or DEFAULT_MAIN_FONT,
                mono_font=mono_var.get().strip() or DEFAULT_MONO_FONT,
                margin=margin_var.get().strip() or DEFAULT_MARGIN,
                toc=toc_var.get(),
            )
        except Exception as exc:
            root.after(0, lambda: append_log(str(exc)))
            root.after(0, lambda: messagebox.showerror(APP_NAME, str(exc)))
            root.after(0, lambda: set_busy(False))
            return

        def finish() -> None:
            output_var.set(str(out))
            append_log(log)
            append_log(f"Created: {out}")
            status_var.set(f"Created: {out.name}")
            convert_button.configure(state="normal")
            if open_var.get():
                open_pdf(out)

        root.after(0, finish)

    def start_conversion() -> None:
        log_box.delete("1.0", "end")
        set_busy(True)
        threading.Thread(target=worker, daemon=True).start()

    convert_button.configure(command=start_conversion)
    input_var.trace_add("write", set_default_output)

    root.mainloop()
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    if args.input:
        return run_cli(args)
    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())
