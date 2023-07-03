.\city_hall.ps1
Write-Output "City Hall started"
Start-Sleep -Seconds 3

.\citizen_1.ps1
Write-Output "Citizen 1 started"
Start-Sleep -Seconds 3

.\citizen_2.ps1
Write-Output "Citizen 2 started"
Start-Sleep -Seconds 3

.\rec_company.ps1
Write-Output "Recycle Company started"
Start-Sleep -Seconds 3

.\container_1.ps1
Write-Output "Container 1 started"
Start-Sleep -Seconds 3

.\container_2.ps1
Write-Output "Container 2 started"
Start-Sleep -Seconds 3

Set-Location ..

Remove-Item -Path ".\data\*" -Force -Recurse

python -m scripts.load_governance
Write-Output "Governance loaded"

Write-Output "Deploy finished"