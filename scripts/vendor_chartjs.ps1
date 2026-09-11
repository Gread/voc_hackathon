# Vendors Chart.js so the UI never needs the network at demo time.
$ErrorActionPreference = "Stop"
$version = "4.4.1"
$target = Join-Path $PSScriptRoot "..\voc\web\vendor\chart.umd.min.js"
Invoke-WebRequest -Uri "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/$version/chart.umd.min.js" -OutFile $target
Write-Host "vendored Chart.js $version to $target"
