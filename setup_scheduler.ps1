$python = "C:\Users\johnr\AppData\Local\Programs\Python\Python312\python.exe"
$script = "C:\Users\johnr\OneDrive\Desktop\Claude Projects\flight-checker\flight_checker.py"
$logFile = "C:\Users\johnr\OneDrive\Desktop\Claude Projects\flight-checker\run.log"

$action = New-ScheduledTaskAction -Execute $python -Argument "`"$script`"" -WorkingDirectory (Split-Path $script)
$trigger = New-ScheduledTaskTrigger -Daily -At "8:00AM"
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 30)

Register-ScheduledTask `
    -TaskName "FlightChecker" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Daily cheap flight scan from SLC" `
    -Force

Write-Host "Scheduled task created. Runs daily at 8:00 AM."
Write-Host "To run it right now: Start-ScheduledTask -TaskName FlightChecker"
