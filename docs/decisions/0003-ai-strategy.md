# ADR-0003: Estrategia de Inferencia de IA y Tooling

| Metadata | Value |
|----------|-------|
| **Estado** | Aceptado |
| **Fecha** | 2026-04-08 |
| **Autor** | jota |
| **Impacto** | Dev workflow, MLOps pipeline |

---

## Contexto

El proyecto `brewery-app` requiere asistencia de IA para desarrollo ágil (generación de código, validación Pydantic, diseño de arquitectura). Simultáneamente, se mantiene un servidor local (`jotasrv`) para infraestructura DevOps/MLOps.

Se evalúa la viabilidad técnica de ejecutar LLMs localmente vs. usar proveedores cloud, considerando:
- Velocidad de iteración en desarrollo interactivo
- Privacidad de datos del proyecto
- Coste económico y de mantenimiento
- Alineación con objetivos de aprendizaje MLOps/LLMOps

---

## Opciones Evaluadas

### Opción 1: Inferencia 100% Local (Ollama + Radeon 680M)

Hardware: ACEMAGIC, Ryzen 7 6800H, Radeon 680M (iGPU), 32GB RAM DDR5

Pruebas realizadas:
- `ollama pull qwen3:8b` (~4.5GB VRAM requerida)

| Métrica | Resultado |
|---------|-----------|
| Tasa de generación | 2-4 tokens/segundo |
| Latencia por respuesta | 30-50 segundos |
| Uso de memoria | 4.5GB VRAM + swap intensivo |
| Experiencia de desarrollo | ❌ Feedback loop roto |

Conclusión: La iGPU comparte ancho de banda de memoria con el sistema (~50 GB/s vs ~360 GB/s en GPU dedicada). El cuello de botella en transferencia de datos hace inviable la inferencia interactiva de modelos ≥7B.

---

### Opción 2: Inferencia Cloud (Groq / OpenRouter / OpenAI)

Pruebas realizadas:
- Groq: Llama 3.3 70B (LPU, ~500 tok/s) - Login inestable
- OpenRouter: Qwen 2.5 7B free tier (~80 tok/s) - Funcional
- OpenCode CLI + Free models: Integración estable

| Métrica | Resultado |
|---------|-----------|
| Tasa de generación | 50-150 tokens/segundo |
| Latencia por respuesta | 1-3 segundos |
| Modelos disponibles | 7B-70B (según provider) |
| Coste | $0 (tier gratuito) |
| Experiencia de desarrollo | ✅ Feedback loop fluido |

Conclusión: Viable para desarrollo interactivo.

---

### Opción 3: Modelo Híbrido (Recomendada)

Combinar lo mejor de ambas aproximaciones según el caso de uso.

| Caso de Uso | Infraestructura | Modelo |
|-------------|----------------|--------|
| Desarrollo interactivo (código, refactor, docs) | Cloud (Opencode) | `free tiers` |
| Automatizaciones nocturnas / batch | Local (Ollama) | `phi3:mini`, `llama3.2:3b` |
| Pruebas MLOps/LLMOps (deploy, monitoring) | Local (Ollama) | Cualquier modelo experimental |
| Producción con datos sensibles | Local + GPU dedicada* | Modelo cuantizado |

*GPU dedicada futura: RTX 3060 12GB o superior para inferencia local viable.

---

## Decisión

✅ **Se adopta el Modelo Híbrido Cloud-First para Desarrollo**

### Configuración Actual (Desarrollo)

Tooling: OpenCode CLI / VS Code extension

Variables de entorno (~/.bashrc):

- export OPENAI_API_KEY="sk-or-v1-..."
- export OPENAI_BASE_URL="https://openrouter.ai/api/v1"


Config mínima (~/.config/opencode/opencode.json):
```json
{
  "$schema": "https://opencode.ai/config.json"
}
```

### Configuración Futura (Local / MLOps)

- Tooling: Ollama + llama.cpp optimizado
- Hardware: jotasrv (Radeon 680M) + posible GPU dedicada
- Modelos objetivo: <3B para interacción, 7B+ cuantizados para batch

### Consecuencias
Positivas

    ✅ Velocidad de desarrollo recuperada (<3s por respuesta)
    ✅ Acceso a modelos capaces (7B+) sin inversión inicial en GPU
    ✅ El servidor local se dedica a infraestructura crítica (PostgreSQL, MinIO, Vault)
    ✅ Flexibilidad para migrar a local cuando sea técnicamente viable

Negativas / Mitigaciones

| Riesgo | Caso de uso |
|:---|:---|
| Dependencia de internet para desarrollo | Infraestructura core (DB, storage) sigue siendo local |
| Privacidad de prompts en cloud | No enviar secretos/credenciales; usar Vault para datos sensibles |
| Cambios en tier gratuito de providers | Mantener config modular; fácil switch entre OpenRouter/Groq/otros |

### Notas de Implementación
---
Para desarrollo diario

   1. Usar OpenCode CLI o extensión VS Code

   2. Seleccionar modelo free tier

   3. No incluir secrets en prompts; usar Vault para credenciales

---

Para experimentación local

1. Instalar Ollama (si no está)
curl -fsSL https://ollama.com/install.sh | sh

2. Descargar modelo pequeño para pruebas
ollama pull phi3:mini

3. Probar velocidad
time ollama run phi3:mini "Hola"
---

Para producción futura

1. Evaluar GPU dedicada (RTX 3060 12GB )

2. Usar quantización Q4_K_M o Q3_K_S para reducir VRAM

3. Implementar caching de respuestas para reducir inferencias repetidas
---


