# PowerShell Testing Commands for NexusAI API

## Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/health"
```

---

## Upload File

### Step 1: Create test file
```powershell
"Wikipedia is a free online encyclopedia. Students can access millions of articles." | Out-File -FilePath "test_wikipedia.txt" -Encoding UTF8
```

### Step 2: Upload file

**For PowerShell 7+ (has `-Form` parameter):**
```powershell
$file = Get-Item "test_wikipedia.txt"
$form = @{
    file = $file
}
Invoke-RestMethod -Uri "http://localhost:8000/admin/upload-file" `
    -Method Post `
    -Headers @{"X-API-Key" = "sk_education_wikipedia_tes123"} `
    -Form $form
```

**For PowerShell 5.1 (Windows default):**
```powershell
# Create multipart form data manually
Add-Type -AssemblyName System.Net.Http

$client = New-Object System.Net.Http.HttpClient
$client.DefaultRequestHeaders.Add("X-API-Key", "sk_education_wikipedia_tes123")

$content = New-Object System.Net.Http.MultipartFormDataContent
$fileStream = [System.IO.File]::OpenRead("test_wikipedia.txt")
$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
$fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("text/plain")
$content.Add($fileContent, "file", "test_wikipedia.txt")

$response = $client.PostAsync("http://localhost:8000/admin/upload-file", $content).Result
$result = $response.Content.ReadAsStringAsync().Result
$fileStream.Close()
$client.Dispose()

Write-Output $result
```

---

## Test Chat

```powershell
$body = @{
    query = "What is Wikipedia?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "X-API-Key" = "sk_education_wikipedia_tes123"
    } `
    -Body $body
```

---

## Add URL

```powershell
$body = @{
    url = "https://example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/admin/add-url" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "X-API-Key" = "sk_education_mit_def456"
    } `
    -Body $body
```

---

## Get Admin Logs

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/admin/logs?lines=20" `
    -Headers @{"X-API-Key" = "sk_admin_master_xyz999"}
```

---

## Test Invalid API Key

```powershell
$body = @{
    query = "test"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "X-API-Key" = "invalid-key"
    } `
    -Body $body
```

---

## Quick Test Workflow (PowerShell 5.1 Compatible)

```powershell
# 1. Health check
Write-Host "=== Testing Health ===" -ForegroundColor Cyan
Invoke-RestMethod -Uri "http://localhost:8000/api/health"

# 2. Create test file
Write-Host "`n=== Creating test file ===" -ForegroundColor Cyan
"Wikipedia is a free online encyclopedia" | Out-File -FilePath "test.txt" -Encoding UTF8

# 3. Upload file (PowerShell 5.1 method)
Write-Host "`n=== Uploading file ===" -ForegroundColor Cyan
Add-Type -AssemblyName System.Net.Http
$client = New-Object System.Net.Http.HttpClient
$client.DefaultRequestHeaders.Add("X-API-Key", "sk_education_wikipedia_tes123")
$content = New-Object System.Net.Http.MultipartFormDataContent
$fileStream = [System.IO.File]::OpenRead("test.txt")
$fileContent = New-Object System.Net.Http.StreamContent($fileStream)
$content.Add($fileContent, "file", "test.txt")
$response = $client.PostAsync("http://localhost:8000/admin/upload-file", $content).Result
$result = $response.Content.ReadAsStringAsync().Result
$fileStream.Close()
$client.Dispose()
Write-Output $result

# 4. Wait for vector store
Write-Host "`n=== Waiting 30 seconds for vector store ===" -ForegroundColor Cyan
Start-Sleep -Seconds 30

# 5. Test chat
Write-Host "`n=== Testing chat ===" -ForegroundColor Cyan
$body = @{ query = "What is Wikipedia?" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
    -Method Post `
    -Headers @{
        "Content-Type" = "application/json"
        "X-API-Key" = "sk_education_wikipedia_tes123"
    } `
    -Body $body
```

---

## Verify Files Created

```powershell
# Check original file
Get-Item "data\policies\education\wikipedia\test_wikipedia.txt"

# Check extracted text
Get-Item "data\raw_data\education\wikipedia\pdf_test_wikipedia.txt"

# Check vector store (wait 30s first)
Get-Item "data\vector_stores\education\wikipedia\vector.index"
Get-Item "data\vector_stores\education\wikipedia\metadata.json"
```

---

## Alternative: Use Real curl (if installed)

If you have Git Bash or WSL:

```bash
curl http://localhost:8000/api/health
```

Or install curl for Windows:
```powershell
winget install curl
```

---

**Note:** In PowerShell, backtick `` ` `` is the line continuation character (not `\` like in bash).



