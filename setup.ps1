[CmdletBinding()]
param(
    [switch]$Start
)

$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
$virtualEnvironment = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $virtualEnvironment "Scripts\python.exe"

function Find-Python311OrNewer {
    $candidates = @(
        @{ Command = "py"; Arguments = @("-3.12") },
        @{ Command = "py"; Arguments = @("-3.11") },
        @{ Command = "python"; Arguments = @() }
    )

    foreach ($candidate in $candidates) {
        if (-not (Get-Command $candidate.Command -ErrorAction SilentlyContinue)) {
            continue
        }

        try {
            $version = & $candidate.Command @($candidate.Arguments + "-c" + "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
            if ([version]$version -ge [version]"3.11") {
                return $candidate
            }
        }
        catch {
            continue
        }
    }

    throw "Python 3.11 lub nowszy jest wymagany. Zainstaluj go i uruchom setup.ps1 ponownie."
}

if (-not (Test-Path $venvPython)) {
    $python = Find-Python311OrNewer
    Write-Host "Tworzenie lokalnego srodowiska Python..."
    & $python.Command @($python.Arguments + @("-m", "venv", $virtualEnvironment))
}

Write-Host "Instalowanie zaleznosci Nerve Center..."
& $venvPython -m pip install --disable-pip-version-check --editable ".[dev]"

if ($Start) {
    Write-Host "Uruchamianie Nerve Center na http://127.0.0.1:8088..."
    & $venvPython (Join-Path $projectRoot "mcp_server.py")
    exit $LASTEXITCODE
}

Write-Host "Nerve Center jest gotowy. Uruchom .\setup.ps1 -Start, aby wystartowac lokalne API."