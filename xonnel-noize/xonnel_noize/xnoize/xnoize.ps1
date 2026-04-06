# ================================
# build.ps1 - compile each noize cpp -> its own dll (MSVC)
# ================================

$ErrorActionPreference = "Stop"

# ---- CONFIG ----
$ROOT   = "C:\Code\Python\Packages\xonnel-noize\xonnel_noize\xnoize"
$VCVARS = "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

$NAMES = @(
    "pnoize2",
    "pnoize3",
    "snoize2",
    "snoize3",
    "wnoize2",
    "wnoize3"
)

# ---- CHECKS ----
if (!(Test-Path $ROOT)) {
    Write-Error "Source directory not found: $ROOT"
    exit 1
}

if (!(Test-Path $VCVARS)) {
    Write-Error "vcvars64.bat not found: $VCVARS"
    exit 1
}

foreach ($NAME in $NAMES) {
    $SRC = Join-Path $ROOT "$NAME.cpp"
    if (!(Test-Path $SRC)) {
        Write-Error "Source file not found: $SRC"
        exit 1
    }
}

# ---- BUILD ALL ----
foreach ($NAME in $NAMES) {
    $SRC = Join-Path $ROOT "$NAME.cpp"
    $OUT = Join-Path $ROOT "$NAME.dll"

    $cmd = @"
"$VCVARS" && cl /LD /O2 /Ot /GL /fp:fast "`"$SRC`"" /Fe:"`"$OUT`""
"@

    Write-Host ""
    Write-Host "=== Building $NAME.dll ==="
    cmd /c $cmd

    if (Test-Path $OUT) {
        Write-Host "SUCCESS: $OUT"
    } else {
        Write-Error "Build failed: $OUT not found"
        exit 1
    }
}

Write-Host ""
Write-Host "=== ALL BUILDS SUCCESSFUL ==="