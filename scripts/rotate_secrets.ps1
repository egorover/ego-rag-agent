# Script for rotating secrets safely
# Используйте этот скрипт для безопасной ротации API ключей

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$EnvFile = "$Root/.env"

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔄 ROTATION OF SECRETS - Руководство" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Этот скрипт НЕ АВТОМАТИЗИРУЕТ ротацию, а предоставляет инструкции." -ForegroundColor Yellow
Write-Host "Автоматическая ротация невозможна без доступа к консолям провайдеров." -ForegroundColor Yellow
Write-Host ""

# Check if .env exists
if (-not (Test-Path $EnvFile)) {
    Write-Host "⚠️  Файл .env не найден. Создайте его из .env.example" -ForegroundColor Yellow
    Write-Host "   Copy-Item .env.example .env" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📋 ШАГ 1: Сгенерировать новые ключи в консолях провайдеров" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. TELEGRAM BOT TOKEN" -ForegroundColor White
Write-Host "   - Откройте @BotFather в Telegram" -ForegroundColor Gray
Write-Host "   - Используйте /newbot или /mybots -> выберите бота -> Revoke Token" -ForegroundColor Gray
Write-Host "   - Скопируйте новый токен" -ForegroundColor Gray
Write-Host "   - URL: https://t.me/BotFather" -ForegroundColor Gray
Write-Host ""

Write-Host "2. PROXYAPI API KEY" -ForegroundColor White
Write-Host "   - ⚠️ Ключ можно увидеть ТОЛЬКО ОДИН РАЗ при создании!" -ForegroundColor Red
Write-Host "   - Зайдите на https://console.proxyapi.ru/keys" -ForegroundColor Gray
Write-Host "   - Создайте новый ключ или удалите старый и создайте заново" -ForegroundColor Gray
Write-Host "   - СКОПИРУЙТЕ КЛЮЧ СРАЗУ — восстановить невозможно!" -ForegroundColor Yellow
Write-Host "   - URL: https://console.proxyapi.ru/keys" -ForegroundColor Gray
Write-Host ""

Write-Host "3. GIGACHAT AUTHORIZATION KEY" -ForegroundColor White
Write-Host "   - Зайдите в консоль GigaChat" -ForegroundColor Gray
Write-Host "   - Найдите раздел API ключи / Credentials" -ForegroundColor Gray
Write-Host "   - Создайте новый ключ или отзовите старый" -ForegroundColor Gray
Write-Host "   - Ключ должен быть в формате: Basic <base64-encoded>" -ForegroundColor Gray
Write-Host "   - URL: https://gigachat.devices.sberbank.ru/" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📝 ШАГ 2: Обновить файл .env" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $EnvFile) {
    Write-Host "Файл .env найден. Обновите следующие строки:" -ForegroundColor White
    Write-Host ""
    Write-Host "TELEGRAM_BOT_TOKEN=НОВЫЙ_TELEGRAM_ТОКЕН" -ForegroundColor Gray
    Write-Host "PROXYAPI_API_KEY=НОВЫЙ_PROXYAPI_КЛЮЧ" -ForegroundColor Gray
    Write-Host "GIGACHAT_AUTHORIZATION_KEY=НОВЫЙ_GIGACHAT_КЛЮЧ" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Или выполните команду для редактирования:" -ForegroundColor Yellow
    Write-Host "   notepad .env" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "Создайте файл .env:" -ForegroundColor White
    Write-Host "   Copy-Item .env.example .env" -ForegroundColor Gray
    Write-Host "   notepad .env" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🧪 ШАГ 3: Проверить работоспособность" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "1. Запустите валидацию конфигурации:" -ForegroundColor White
Write-Host "   python -c `"from config import Settings; s = Settings.from_env(); print('✅ Config OK')`"" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Запустите сканирование безопасности:" -ForegroundColor White
Write-Host "   .\scripts\security_scan.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Перезапустите бота:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🗑️  ШАГ 4: Отзвать старые ключи (ОПЦИОНАЛЬНО)" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "После проверки работоспособности новых ключей:" -ForegroundColor White
Write-Host "  - Отзовите старые ключи в консолях провайдеров" -ForegroundColor Gray
Write-Host "  - Это предотвратит использование украденных/устаревших ключей" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📅 РЕКОМЕНДУЕМАЯ ЧАСТОТА РОТАЦИИ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "  • Telegram Bot Token: каждые 180 дней или при компрометации" -ForegroundColor White
Write-Host "  • ProxyAPI API Key: каждые 90 дней" -ForegroundColor White
Write-Host "  • GigaChat Key: каждые 90 дней" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Немедленно ротируйте ключи при:" -ForegroundColor Yellow
Write-Host "  • Утере доступа к системе" -ForegroundColor Gray
Write-Host "  • Подозрении на утечку" -ForegroundColor Gray
Write-Host "  • Смене сотрудников с доступом" -ForegroundColor Gray
Write-Host "  • Инцидентах безопасности" -ForegroundColor Gray
Write-Host ""

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "📚 ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Полная документация по безопасности:" -ForegroundColor White
Write-Host "  SECURITY.md" -ForegroundColor Gray
Write-Host "  SECURITY_REPORT.md" -ForegroundColor Gray
Write-Host ""
