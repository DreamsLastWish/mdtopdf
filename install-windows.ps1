$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$InstallDir = Join-Path $env:LOCALAPPDATA "mdtopdf\bin"
$Launcher = Join-Path $InstallDir "mdtopdf.bat"

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Set-Content -Encoding ASCII -Path $Launcher -Value "@echo off`r`npython `"$ScriptDir\md_to_pdf_converter.py`" %*`r`n"

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$paths = @()
if ($userPath) {
    $paths = $userPath -split ";"
}

if ($paths -notcontains $InstallDir) {
    $newPath = if ($userPath) { "$userPath;$InstallDir" } else { $InstallDir }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Added to user PATH: $InstallDir"
    Write-Host "Open a new PowerShell window before using mdtopdf."
}

Write-Host "Installed: $Launcher"
Write-Host "Usage: mdtopdf C:\path\to\file.md"
