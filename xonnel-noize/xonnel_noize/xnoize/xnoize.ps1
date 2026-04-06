# ================================
# build.ps1 - compile xnoize.cpp → xnoize.dll (MSVC)
# ================================

$ErrorActionPreference = "Stop"

# ---- CONFIG ----
$SRC = "C:\Code\Python\Packages\xonnel-noize\xonnel_noize\xnoize\xnoize.cpp"
$OUT = "C:\Code\Python\Packages\xonnel-noize\xonnel_noize\xnoize\xnoize.dll"
$VCVARS = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

# ---- CHECKS ----
if (!(Test-Path $SRC)) {
    Write-Error "Source file not found: $SRC"
    exit 1
}

if (!(Test-Path $VCVARS)) {
    Write-Error "vcvars64.bat not found: $VCVARS"
    exit 1
}

# ---- BUILD COMMAND ----
$cmd = @"
"$VCVARS" && cl /LD /O2 /Ot /GL /fp:fast "$SRC" /Fe:"$OUT"
"@

Write-Host "=== Building xnoize.dll ==="
cmd /c $cmd

# ---- VERIFY OUTPUT ----
if (Test-Path $OUT) {
    Write-Host "=== SUCCESS ==="
    Write-Host "Output: $OUT"
} else {
    Write-Error "Build failed: DLL not found"
    exit 1
}