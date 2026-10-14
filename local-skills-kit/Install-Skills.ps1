param([switch]$Verify, [switch]$BackupExisting)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$Script = Join-Path $PSScriptRoot 'install_skills.py'
$Python = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -c 'import sys; assert sys.version_info >= (3,9)'
    if ($LASTEXITCODE -eq 0) { $Python = 'py' }
}
if (-not $Python -and (Get-Command python -ErrorAction SilentlyContinue)) {
    & python -c 'import sys; assert sys.version_info >= (3,9)'
    if ($LASTEXITCODE -eq 0) { $Python = 'python' }
}
if (-not $Python) { throw 'Install Python 3.9+ for Windows, then reopen VS Code.' }
$Options = @($Script)
if ($Verify) { $Options += '--verify' }
if ($BackupExisting) { $Options += '--backup-existing' }
if ($Python -eq 'py') { & py -3 @Options } else { & python @Options }
if ($LASTEXITCODE -ne 0) { throw 'Installation or verification failed. Read the ERROR above; no automatic retries.' }
