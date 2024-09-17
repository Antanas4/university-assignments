<#
.SYNOPSIS
Manages files and directories

.DESCRIPTION
Deletion of files/directories
Creating .zip of files
Sorting .txt file alphabetically
Sorting files by extension and moving them to the specified directories

.PARAMETER DeleteSelectedDirectories
Deletes chosen directories

.PARAMETER DeleteSelectedFiles
Deletes selected files

.PARAMETER Zip
Creates a .zip file for files with a chosen file name extension

.PARAMETER All
Deletes all files by the providede extension

.PARAMETER Confirm
Requests the user for deletion confirmation

.PARAMETER -csv
Used with -DeleteSelectedFiles or -DeleteSelectedDirectories.
Creates a .csv file with deleted and not deleted directories

.PARAMETER -MoveFilesByExtension
Sorts files by extension and creates seperate directories for the same extension file

.PARAMETER -exclude
Used with -MoveFilesByExtension. Does not create directories for files with specified extension name after -exclude

.PARAMETER -SortDocument
Sorts .txt file text alphabetically

.EXAMPLE
Manage-Directory -DeleteSelectedDirectories NamesofYourDirectories -Confirm(optional) -csv(optional)

.EXAMPLE
Manage-Directory -DeleteSelectedFiles NamesofYourFiles -Confirm(optional) -csv(optional)

.EXAMPLE
Manage-Directory -DeleteSelectedFiles .YourFileExtension -All -csv(optional) -Confirm (optional)

.EXAMPLE
.Manage-Directory -MoveFilesByExtension

.EXAMPLE
.Manage-Directory -MoveFilesByExtension .docx -exclude

#>

<# prideti daugiau funkciju #>

function Manage-Directory {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$false)]
        [string[]]$DeleteSelectedDirectories,

        [Parameter(Mandatory=$false)]
        [string[]]$DeleteSelectedFiles,

        [Parameter(Mandatory=$false)]
        [string[]]$Zip,

        [Parameter(Mandatory=$false)]
        [switch]$All,

        [Parameter(Mandatory=$false)]
        [switch]$Confirm,

        [Parameter(Mandatory=$false)]
        [switch]$csv,

        [Parameter (Mandatory=$false)]
        [switch] $MoveFilesByExtension,

        [Parameter(Mandatory=$false)]
        [AllowEmptyCollection()]
        [string[]]$exclude,

        [Parameter(Mandatory=$false)]
        [string] $SortDocument

    )

    if ($DeleteSelectedDirectories) {
        if($Confirm){
            $confirmationMessage = "Are you sure that you want to delete selected directories? (Type 'y'/'Y' to confirm)"
            $result = Read-Host -Prompt $confirmationMessage
            if($result -ne 'Y' -and $result -ne 'y'){
                Write-Host "Deletion cancelled" -ForegroundColor Red
                return
            }
        }
        $deletedDirectories = @()
        $notDeletedDirectories = @()
        foreach ($dirName in $DeleteSelectedDirectories){
            if(Test-Path -Path $dirName -PathType Container){
                Remove-Item -Path $dirName -Recurse -Force
                $deletedDirectories += $dirName
            }else {
                $notDeletedDirectories += $dirName
            }
        }
        if($csv){
            $timeStamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
            $csvFileName = "DeletedDirectories_$timeStamp.csv"
            $csvPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"),$csvFileName)

            $csvData = @()
            $deletedDirectories | ForEach-Object{
                $csvData += [PSCustomObject]@{
                    'Directory' = $_
                    'Status' = 'Deleted'
                }
            }
            $notdeletedDirectories | ForEach-Object{
                $csvData += [PSCustomObject]@{
                    'Directory' = $_
                    'Status' = 'Not Deleted (does not exist)'
                }
            }
            $csvData | Export-Csv -Path $csvPath -NoTypeInformation
        }
        Write-Host "Directories deleted succesfully" -ForegroundColor Green
    }
    if($DeleteSelectedFiles){
        if($Confirm){
            $confirmationMessage = "Are you sure that you want to delete selected files? (Type 'y'/'Y' to confirm)"
            $result = Read-Host -Prompt $confirmationMessage
            if($result -ne 'Y' -and $result -ne 'y'){
                Write-Host "Deletion cancelled" -ForegroundColor Red
                return
            }
        }
        if($All){
            $currentDirectory = Get-Location
            $filesToDelete = Get-ChildItem -Path $currentDirectory -File |
                Where-Object {$DeleteSelectedFiles -contains $_.Extension}
        }
        else{
            $filesToDelete = $DeleteSelectedFiles
        }
        $deletedFiles = @()
        $notDeletedFiles = @()
        foreach ($fileName in $filesToDelete){
            if(Test-Path -Path $fileName -PathType Leaf){
                Remove-Item -Path $fileName -Force
                $deletedFiles += $fileName
            }else {
                $notDeletedFiles += $fileName
            }
        }
        if($csv){
            $timeStamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
            $csvFileName = "DeletedFiles_$timeStamp.csv"
            $csvPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"),$csvFileName)
            $csvData = @()
            $deletedFiles | ForEach-Object{
                $csvData += [PSCustomObject]@{
                    'File' = $_
                    'Status' = 'Deleted'
                }
            }
            $notDeletedFiles | ForEach-Object{
                $csvData += [PSCustomObject]@{
                    'File' = $_
                    'Status' = 'Not Deleted (does not exist)'
                }
            }
            $csvData | Export-Csv -Path $csvPath -NoTypeInformation
        }
        Write-Host "Files deleted succesfully" -ForegroundColor Green
    }

    if ($Zip){
        $timeStamp = Get-Date -Format "yyyy-MM-dd-HH-mm-ss"
        $zipFileName = "MyZippedFiles_$timeStamp.zip"
        $zipPath =  [System.IO.Path]::Combine([System.Environment]::GetFolderPath("Desktop"),$zipFileName)
        Compress-Archive -Path $Zip -DestinationPath $zipPath
        Write-Host ".zip created succesfully" -ForegroundColor Green
    }

    if ($MoveFilesByExtension) {
        $sourceFolder = Get-Location
        $uniqueExtensions = Get-ChildItem -Path $sourceFolder | Where-Object { -not $_.PSIsContainer } | ForEach-Object { $_.Extension } | Sort-Object -Unique
        if($exclude){
            $uniqueExtensions = $uniqueExtensions | Where-Object { $extension = $_.Trim('.').Trim(); -not $exclude.Contains($extension) }
        }
        foreach ($extension in $uniqueExtensions) {
            $extension = $extension.Trim('.').Trim()
            $extensionFolder = [System.IO.Path]::Combine($sourceFolder, $extension)
            if (-not (Test-Path -Path $extensionFolder)) {
                New-Item -ItemType Directory -Path $extensionFolder
            }
            Get-ChildItem -Path $sourceFolder | Where-Object { -not $_.PSIsContainer -and $_.Extension -eq ".$extension" } | ForEach-Object {
                $destinationPath = [System.IO.Path]::Combine($extensionFolder, $_.Name)
                Move-Item -Path $_.FullName -Destination $destinationPath -Force
            }
        }
    }
    if ($SortDocument) {
        if (Test-Path -Path $SortDocument -PathType Leaf) {
            $documentContent = Get-Content $SortDocument
            $sortedContent = $documentContent -split '\s+' | Sort-Object
            $documentName = [System.IO.Path]::GetFileNameWithoutExtension($SortDocument)
            $outputFile = "$documentName-sorted.txt"
            $sortedContent | Out-File -FilePath $outputFile
            Write-Host "Document sorted and saved to $outputFile." -ForegroundColor Green
        } else {
            Write-Host "The specified document file does not exist." -ForegroundColor Red
        }
    }
    
    

}