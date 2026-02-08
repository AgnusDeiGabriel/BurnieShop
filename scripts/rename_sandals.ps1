# Rename files inside 'Sandals' replacing 'SANDAL' (case-insensitive) with 'SANDALES', then rename folder
$root = (Get-Location).Path
$candidates = @('Sandals','Sandales')
$targetFolderName = 'Sandales'

foreach ($dirName in $candidates) {
    $full = Join-Path $root $dirName
    if (-not (Test-Path $full)) { continue }
    Write-Host "Processing directory: $full"
    Get-ChildItem -LiteralPath $full -File | ForEach-Object {
        $orig = $_.Name
        $newName = $orig -replace '(?i)SANADL','SANDALES'
        $newName = $newName -replace '(?i)SANDAL','SANDALES'
        if ($orig -ne $newName) {
            Rename-Item -LiteralPath $_.FullName -NewName $newName -Force
            Write-Host "Renamed: $orig -> $newName"
        }
    }
    # If this wasn't already the desired folder name, rename it
    if ($dirName -ieq $targetFolderName) { break }
    $parent = Split-Path $full -Parent
    $targetFull = Join-Path $parent $targetFolderName
    if (-not (Test-Path $targetFull)) {
        Rename-Item -LiteralPath $full -NewName $targetFolderName -Force
        Write-Host "Renamed directory: $dirName -> $targetFolderName"
    } else {
        Write-Host "Target directory '$targetFolderName' already exists; skipping directory rename for $dirName."
    }
    break
}
