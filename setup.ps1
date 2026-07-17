# Claude Code + Skills 一键部署 (Windows)
# 用法: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Claude Code + 32 Skills 一键部署" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# === Step 1: Check Node.js ===
Write-Host "[1/4] 检查 Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "  Node.js 未安装，正在通过 winget 安装..." -ForegroundColor Gray
    winget install OpenJS.NodeJS --accept-package-agreements --accept-source-agreements
    Write-Host "  ⚠ 安装完成后请重新打开终端，再次运行本脚本" -ForegroundColor Red
    Write-Host "  或者手动刷新 PATH: `$env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [Environment]::GetEnvironmentVariable('Path','User')" -ForegroundColor Gray
    exit 0
}

# Refresh PATH to ensure npm is available
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$nodeVersion = node --version
Write-Host "  ✅ Node.js $nodeVersion" -ForegroundColor Green

# === Step 2: Install Claude Code ===
Write-Host "[2/4] 安装 Claude Code..." -ForegroundColor Yellow
$cc = Get-Command claude -ErrorAction SilentlyContinue
if ($cc) {
    Write-Host "  Claude Code 已安装: claude --version" -ForegroundColor Green
    claude --version
} else {
    Write-Host "  正在安装 @anthropic-ai/claude-code ..." -ForegroundColor Gray
    npm install -g @anthropic-ai/claude-code
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Claude Code 安装完成" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 安装失败，请检查网络连接后重试" -ForegroundColor Red
        exit 1
    }
}

# === Step 3: Install Skills ===
Write-Host "[3/4] 安装 32 Skills..." -ForegroundColor Yellow
$skillsDir = "$env:USERPROFILE\.claude\skills"
if (Test-Path $skillsDir) {
    Write-Host "  Skills 目录已存在，正在更新..." -ForegroundColor Gray
    cd $skillsDir
    git pull 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠ git pull 失败（可能不是 git 仓库），使用已有文件" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ Skills 已更新" -ForegroundColor Green
    }
} else {
    Write-Host "  正在从 GitHub 拉取..." -ForegroundColor Gray
    git clone https://github.com/Mingel-github/claude-skills.git $skillsDir
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ 32 Skills 安装完成" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 克隆失败，请检查 Git 和网络" -ForegroundColor Red
        exit 1
    }
}

# === Step 4: Verify ===
Write-Host "[4/4] 验证..." -ForegroundColor Yellow
$skillsCount = (Get-ChildItem -Directory $skillsDir).Count
Write-Host "  ✅ $skillsCount 个 Skill 已就绪" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  部署完成！" -ForegroundColor Green
Write-Host ""
Write-Host "  启动 Claude Code:  claude" -ForegroundColor White
Write-Host "  管理 Skills:      /skills" -ForegroundColor White
Write-Host "  查看说明:         $skillsDir\README.md" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
