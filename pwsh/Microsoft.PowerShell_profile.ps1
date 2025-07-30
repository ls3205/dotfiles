

# oh-my-posh init pwsh --config "C:\Users\leons\omp\leon.omp.json" | Invoke-Expression
oh-my-posh init pwsh --config "C:\Users\leons\.cache\wal\posh-wal-atomic.omp.json" | Invoke-Expression

Import-Module Terminal-Icons
# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}

Import-Module "C:\Users\leons\Documents\vsCodeProjects\winwal\winwal.psm1"

New-Alias nc ncat
New-Alias wget wget2
