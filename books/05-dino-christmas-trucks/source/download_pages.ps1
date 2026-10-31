# Run in PowerShell on your PC: downloads the 50 Higgsfield pages as 01.png ... 50.png
$dst = "C:\Users\bibhu\VividFlow-Studio\KDP\Dino-Christmas-Trucks\raw"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Get-Content "$PSScriptRoot\higgsfield_urls.txt" | ForEach-Object {
  $n, $u = $_ -split ' ', 2
  Invoke-WebRequest -Uri $u -OutFile "$dst\$n.png"
}
Write-Host "Done: $dst"
