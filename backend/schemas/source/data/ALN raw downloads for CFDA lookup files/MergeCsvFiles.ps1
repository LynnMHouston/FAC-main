# Define Parameters
param(
    [string]$InputFolder = "backend/schemas/source/data/ALN raw downloads for CFDA lookup files"
)

# Define Output Path
$ParentFolder = (Get-Item -Path $InputFolder).Parent.FullName
$DateSuffix = (Get-Date).ToString("yyyyMMdd")
$OutputFile = Join-Path -Path $ParentFolder -ChildPath "cfda-lookup-$DateSuffix.csv"
# Get all CSV files in the input folder
$CsvFiles = Get-ChildItem -Path $InputFolder -Filter "*.csv"
if ($CsvFiles.Count -eq 0) {
    Write-Host "No CSV files found in the input folder: $InputFolder"
    return
}

# Import and prepare data
$AllData = foreach ($File in $CsvFiles) {
    try {
        Import-Csv -Path $File.FullName
    } catch {
        Write-Error "Failed to import CSV file: $($File.FullName). Error: $_"
    }
}

# Check if there is any data
if (-not $AllData) {
    Write-Host "No data found in the imported files."
    return
}

# Identify all unique columns across all files
$AllColumns = $AllData | ForEach-Object { $_.PsObject.Properties.Name } | Sort-Object -Unique

# Standardize the data structure by ensuring all rows have the same columns
foreach ($Row in $AllData) {
    foreach ($Column in $AllColumns) {
        if (-not $Row.PSObject.Properties[$Column]) {
            $Row | Add-Member -MemberType NoteProperty -Name $Column -Value $null -Force
        }
    }
}

# Reorder and rename columns for output
$ReorderedData = $AllData | Select-Object `
    @{Name="Program Title"; Expression={ $_.Title }}, `
    @{Name="Program Number"; Expression={ $_."Assistance Listings Number" }}, `
    @{Name="Date Published"; Expression={ $_."Date Published" }}, `
    @{Name="Department/Ind. Agency"; Expression={ $_."Department/Ind. Agency" }}, `
    @{Name="Funded"; Expression={ $_.Funded }}, `
    @{Name="Last Date Modified"; Expression={ $_."Last Date Modified" }}, `
    @{Name="POC Information"; Expression={ $_."POC Information" }}, `
    @{Name="Related Federal Assistance"; Expression={ $_."Related Federal Assistance" }}, `
    @{Name="Sub-Tier"; Expression={ $_."Sub-Tier" }}, `
    @{Name="Types of Assistance"; Expression={ $_."Types of Assistance" }}

# Export the cleaned, merged data with proper encoding (UTF-8)
try {
    $ReorderedData | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8
    Write-Host "Data from all CSV files in $InputFolder has been merged, standardized, and saved to $OutputFile with UTF-8 encoding."
} catch {
    Write-Error "Failed to export the merged data to CSV. Error: $_"
}
