#!/bin/bash
# audit-permissions.sh - Verifica permisos críticos del proyecto brewery-app
# Aprendizaje: Linux permissions applied to project security

set -e

PROJECT_ROOT="${1:-$(pwd)}"
echo "🔍 Auditing permissions for: $PROJECT_ROOT"
echo "📅 $(date)"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_perm() {
    local path=$1
    local expected=$2
    local description=$3

    if [ ! -e "$path" ]; then
        echo -e "${YELLOW}⚠️  SKIP${NC}: $path no existe"
        return
    fi

    local actual=$(stat -c "%a" "$path" 2>/dev/null || stat -f "%Lp" "$path")

    if [ "$actual" = "$expected" ]; then
        echo -e "${GREEN}✅ OK${NC}: $description ($path: $actual)"
    else
        echo -e "${RED}❌ FAIL${NC}: $description"
        echo "   Esperado: $expected, Actual: $actual"
        echo "   Fix: chmod $expected $path"
    fi
}

echo "📁 Verificando estructura del proyecto..."
check_perm "$PROJECT_ROOT/.git" "700" "Carpeta .git (debe ser privada)"
check_perm "$PROJECT_ROOT/backend" "755" "Carpeta backend (pública, no writable por others)"
check_perm "$PROJECT_ROOT/docs" "755" "Carpeta docs (pública)"

echo ""
echo "🔐 Verificando archivos sensibles..."
if [ -f "$PROJECT_ROOT/.env" ]; then
    check_perm "$PROJECT_ROOT/.env" "600" "Archivo .env (secrets)"
else
    echo -e "${YELLOW}ℹ️  INFO${NC}: No hay .env aún (crearlo cuando haya secrets)"
fi

echo ""
echo "📜 Verificando scripts ejecutables..."
for script in "$PROJECT_ROOT/scripts/"*.sh; do
    if [ -f "$script" ]; then
        check_perm "$script" "755" "Script ejecutable: $(basename $script)"
    fi
done

echo ""
echo "✅ Auditoría completada"
