# Investigacion: Custom WhatsApp AI Harness — Insights de OpenClaw y Estado del Arte

> **Fecha:** 2026-04-09
> **Autor:** Gilberts Ahumada (asistido por Claude)
> **Objetivo:** Documentar insights del harness de OpenClaw y tecnicas avanzadas de personalizacion AI para construir un asistente WhatsApp que realmente aprenda del usuario con el tiempo.
> **Proyecto destino:** WhatsApp AI Assistant (AI SDK + Custom Harness)

---

## Tabla de Contenidos

1. [Que es OpenClaw](#1-que-es-openclaw)
2. [Arquitectura del Harness de OpenClaw](#2-arquitectura-del-harness-de-openclaw)
3. [Workspace: Sistema de Configuracion por Archivos](#3-workspace-sistema-de-configuracion-por-archivos)
4. [Sistema de Memoria de OpenClaw](#4-sistema-de-memoria-de-openclaw)
5. [Patrones del Harness para tu WhatsApp Assistant](#5-patrones-del-harness-para-tu-whatsapp-assistant)
6. [Las 5 Capas de Personalizacion Profunda](#6-las-5-capas-de-personalizacion-profunda)
7. [Frameworks de Memoria (Estado del Arte 2025-2026)](#7-frameworks-de-memoria-estado-del-arte-2025-2026)
8. [Modelos Dedicados y Especializados](#8-modelos-dedicados-y-especializados)
9. [Mas Alla del Harness — Otras Implementaciones](#9-mas-alla-del-harness--otras-implementaciones)
10. [Arquitectura Recomendada](#10-arquitectura-recomendada)
11. [Roadmap de Implementacion](#11-roadmap-de-implementacion)
12. [Referencias y Fuentes](#12-referencias-y-fuentes)

---

## 1. Que es OpenClaw

OpenClaw (anteriormente Clawdbot, luego Moltbot) es un **agente AI autonomo open-source** creado por Peter Steinberger. Lanzado en noviembre 2025, alcanzo 150K+ GitHub stars rapidamente. NVIDIA CEO Jensen Huang lo llamo "el sistema operativo para AI personal."

### Que hace

- Conecta LLMs (Claude, GPT-4o, Gemini, DeepSeek, Ollama) a plataformas de mensajeria
- Soporta 15+ canales: WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Google Chat, Teams, Matrix, etc.
- Convierte un LLM en un agente accionable: gestiona inbox, calendario, mensajes, automatiza navegador, ejecuta comandos shell, lee/escribe archivos
- Es model-agnostic y self-hosted

### Concepto de "Harness"

El **"agentic harness"** es la capa de infraestructura que NO es el LLM, sino todo lo que lo gobierna:

```
+----------------------------------------------------------+
|                    AGENTIC HARNESS                        |
|                                                          |
|  +----------+  +--------+  +-----------+  +-----------+  |
|  | Identidad|  | Memoria|  | Ejecucion |  | Guardrails|  |
|  | & Reglas |  | & State|  | de Tools  |  | & Safety  |  |
|  +----------+  +--------+  +-----------+  +-----------+  |
|                                                          |
|  +----------+  +--------+  +-----------+  +-----------+  |
|  | Triggers |  | Contexto| | Permisos  |  | Loops     |  |
|  | & Cron   |  | Window |  | & Auth    |  | Iterativos|  |
|  +----------+  +--------+  +-----------+  +-----------+  |
|                                                          |
|                    +-------+                              |
|                    |  LLM  |                              |
|                    +-------+                              |
+----------------------------------------------------------+
```

Un agente = modelo + memoria + instrucciones + triggers + herramientas + outputs + loop.
El harness provee todos los "plus".

### Arquitectura de 3 capas

```
+-----------------------------------------------------------+
| CHANNEL LAYER (Input/Output)                               |
| WhatsApp | Telegram | Slack | Discord | Signal | WebChat   |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
| BRAIN LAYER (Razonamiento)                                 |
| Agent Runtime: contexto + modelo + tool calls + state      |
| SOUL.md + AGENTS.md + USER.md -> system prompt            |
+-----------------------------+-----------------------------+
                              |
                              v
+-----------------------------------------------------------+
| BODY LAYER (Accion)                                        |
| Tools | Browser | Files | Memory | Cron | Messaging        |
+-----------------------------------------------------------+
```

---

## 2. Arquitectura del Harness de OpenClaw

### Stack tecnologico

- **Lenguaje:** TypeScript (ESM)
- **Runtime:** Node.js >=22.12.0
- **Package Manager:** pnpm 10.23.0
- **AI Runtime:** `@mariozechner/pi-*` (pi-agent-core, pi-ai, pi-coding-agent)
- **Messaging:** Grammy (Telegram), discord.js, Baileys (WhatsApp), Bolt (Slack)
- **Config Validation:** Zod 4.3.6
- **Browser:** Playwright-core 1.58.2
- **DB:** SQLite + sqlite-vec (vector embeddings)
- **Build:** tsdown, Rolldown, Vite

### Estructura del monorepo

```
openclaw/
+-- src/                    # Core (68+ subdirectorios)
|   +-- agents/             # Agent runtime, system prompt, tools
|   +-- gateway/            # WebSocket control plane
|   +-- memory/             # Memory system (69 archivos)
|   +-- channels/           # Channel adapters
|   +-- plugins/            # Hook/plugin system
|   +-- config/             # Config loading, validation
|   +-- auto-reply/         # Reply orchestration
|   +-- routing/            # Message -> agent routing
|   +-- cron/               # Scheduled tasks
+-- extensions/             # 30+ channel & feature plugins
+-- skills/                 # 54+ bundled skills
+-- apps/                   # Native apps (macOS, iOS, Android)
+-- ui/                     # Web UI (WebChat, Control UI)
+-- docs/                   # Documentation
```

### Gateway Server (Control Plane)

```
WebSocket ws://127.0.0.1:18789
|
+-- Channel lifecycle management
+-- Session state persistence
+-- Agent orchestration (spawn, route, manage runs)
+-- Tool execution
+-- Real-time event streaming
```

**Metodos del gateway:**

- `chat.send`, `chat.abort` -- chat directo
- `send` -- message routing
- `agent` -- agent execution
- `channels.status`, `channels.list` -- channel management
- `sessions.list`, `sessions.patch` -- session operations
- `skills.status`, `skills.update` -- skill management
- `cron.list`, `cron.add` -- scheduled tasks
- `health`, `status` -- system health

### Pipeline de ejecucion del agente

```
1. Message arrives (CLI/Gateway/Channel)
       |
       v
2. Route Resolution
   resolve-route.ts: channel + accountId + peer -> agentId + sessionKey
       |
       v
3. Agent Harness Setup
   agent-scope.ts: load config, workspace, sessions
       |
       v
4. System Prompt Building
   system-prompt.ts: compose sections dynamically
   +-- Skills section
   +-- Memory recall section
   +-- User identity section
   +-- Time/timezone section
   +-- Channel capabilities
   +-- Workspace notes + heartbeat
       |
       v
5. Model Resolution
   model.ts: resolve provider/model, auth profiles, context window
       |
       v
6. Tool Preparation
   pi-tools.ts: core tools + skill tools + client tools
   Filtered by agent config
       |
       v
7. Execution (Pi Embedded Runner)
   attempt.ts: streamSimple() -> tool calls -> results
   Failover: auth rotation, model fallback, rate limit backoff
       |
       v
8. Session Persistence
   Write lock -> transcript accumulation -> usage tracking
   Compaction if context exceeds limits
       |
       v
9. Channel Outbound
   Per-channel adapters: markdown->native format, chunking, retry
       |
       v
10. Hooks Fire
    post-message, post-tool-call, etc.
```

### Hook/Plugin System

Archivo: `src/plugins/hooks.ts`

| Hook               | Momento                   | Tipo                   |
| ------------------ | ------------------------- | ---------------------- |
| `beforeAgentStart` | Antes de ejecutar agente  | Modifying (sequential) |
| `beforeToolCall`   | Antes de ejecutar tool    | Modifying (sequential) |
| `afterToolCall`    | Despues de tool           | Void (parallel)        |
| `messageSending`   | Antes de enviar respuesta | Modifying (sequential) |
| `messageReceived`  | Al recibir mensaje        | Void (parallel)        |
| `sessionStart`     | Nueva sesion              | Void (parallel)        |
| `sessionEnd`       | Fin de sesion             | Void (parallel)        |
| `llmInput`         | Pre-LLM call              | Modifying (sequential) |
| `llmOutput`        | Post-LLM call             | Void (parallel)        |
| `beforeCompaction` | Pre-compactacion          | Modifying (sequential) |
| `afterCompaction`  | Post-compactacion         | Void (parallel)        |

**Regla:** Void hooks = paralelo (fire-and-forget). Modifying hooks = secuencial con merge.

---

## 3. Workspace: Sistema de Configuracion por Archivos

### Jerarquia de configuracion

El workspace es el directorio hogar del agente. Cada archivo markdown tiene una responsabilidad unica:

```
IDENTITY.md  (QUIEN es el agente)
    |
    v
SOUL.md      (COMO se comporta -- principios, tono, limites)
    |
    v
USER.md      (QUIEN es el usuario -- preferencias, timezone, metas)
    |
    v
HEARTBEAT.md (CUANDO actua -- triggers temporales)
    |
    v
AGENTS.md    (QUE hace -- campanas, flujos, reglas)
    |
    v
TOOLS.md     (CON QUE ejecuta -- comandos, APIs, referencias tecnicas)
    |
    v
data/        (DONDE almacena -- logs, metricas, drafts)
    |
    v
skills/      (CAPACIDADES extras -- CLI tools, scripts)
```

### Detalle de cada archivo

| Archivo          | Proposito                                                            | Tamano tipico |
| ---------------- | -------------------------------------------------------------------- | ------------- |
| `IDENTITY.md`    | Nombre, rol, vibe, emoji, awareness de competencia                   | ~400 bytes    |
| `SOUL.md`        | Principios core, valores, tono, limites, posicionamiento competitivo | ~8 KB         |
| `USER.md`        | Preferencias del usuario, timezone, metas, content mix targets       | ~1.5 KB       |
| `HEARTBEAT.md`   | Tareas automatizadas con triggers temporales, workflow de aprobacion | ~1.8 KB       |
| `AGENTS.md`      | Master playbook: campanas, reglas, API budgets, reglas de idioma     | ~17 KB        |
| `TOOLS.md`       | Referencia tecnica: comandos, chain IDs, conceptos del dominio       | ~4.6 KB       |
| `data/README.md` | Arquitectura de data logging, folder structure, retention            | ~4.4 KB       |
| `BOOTSTRAP.md`   | Ritual de primer inicio (se borra despues)                           | variable      |
| `MEMORY.md`      | Memoria curada de largo plazo                                        | variable      |
| `BOOT.md`        | Checklist de startup en gateway restart                              | variable      |

### Workspace actual (trust8004 Community Manager)

```
workspace/
+-- IDENTITY.md                    # @trust8004 Twitter persona
+-- USER.md                        # Gilberts: Spanish, Chile timezone
+-- HEARTBEAT.md                   # 9AM, 10AM, 1PM, 5PM triggers
+-- SOUL.md                        # Data-driven, no hype, crypto-native
+-- AGENTS.md                      # 3 campanas: Data Drop, Engagement, Ecosystem
+-- TOOLS.md                       # twclaw CLI, fetch-metrics, chain IDs
+-- data/
|   +-- README.md                  # Data logging spec
|   +-- daily/YYYY-MM-DD/          # Daily logs (14-day retention)
|   +-- weekly/YYYY-WNN/           # Weekly logs (8-week retention)
+-- scripts/
|   +-- fetch-metrics.mjs          # Playwright -> trust8004 API metrics
|   +-- fetch-changelog.mjs        # Playwright -> trust8004 changelog
|   +-- twitter-refresh-token.mjs  # OAuth 2.0 token refresh
+-- skills/
    +-- twitter-openclaw/
        +-- SKILL.md               # twclaw CLI documentation
        +-- package.json
        +-- bin/twclaw.js          # Twitter/X CLI tool
```

### Reglas operacionales clave

**Approval Gates:**

- TODOS los tweets requieren aprobacion de Gilberts
- TODAS las interacciones (likes, retweets) requieren aprobacion
- Drafts enviados via Telegram, discusiones en espanol

**Reglas de idioma (estrictas):**

- Twitter/X: siempre en ingles
- Telegram con Gilberts: siempre en espanol
- Grupo Telegram: siempre en ingles
- Engagement: idioma nativo del tweet original

**Anti-patrones (prohibidos):**

- No em dashes en tweets (delatan AI)
- No Unicode fancy ni smart quotes
- No frases genericas ("Here's why that matters")
- No especulacion de precios
- No engagement con competencia (@8004_scan)
- No almacenar texto completo de tweets (solo URL/handle/resumen)

**API Budgets:**

- 1 busqueda/dia max
- 9 interacciones/dia max (likes + retweets)
- Sin engagement en fines de semana
- Nunca llamar mentions/home/user-tweets automaticamente

**Data Retention:**

- Daily folders: 14 dias
- Weekly folders: 8 semanas
- Audit files: 30 dias
- Cleanup: lunes por la manana

### Insight para tu harness: Configuracion modular

```typescript
// Estructura sugerida para tu WhatsApp harness
interface WorkspaceConfig {
  identity: string; // Quien es el asistente
  soul: string; // Como se comporta (tono, limites)
  user: string; // Perfil del usuario
  instructions: string; // Que hace (flujos, reglas)
  tools: string; // Referencia tecnica
}

// Composicion dinamica del system prompt
function buildSystemPrompt(workspace: WorkspaceConfig): string {
  return [
    workspace.identity,
    workspace.soul,
    `## Usuario\n${workspace.user}`,
    workspace.instructions,
    workspace.tools,
    `## Contexto temporal\n- Fecha: ${new Date().toISOString()}\n- Timezone: ${tz}`,
  ].join("\n\n---\n\n");
}
```

**Ventaja:** Puedes modificar comportamiento sin tocar codigo. Cada cliente puede tener su propio workspace.

---

## 4. Sistema de Memoria de OpenClaw

### Arquitectura two-tier

```
+-------------------------------------------------------------------+
|                     MEMORY SYSTEM                                  |
|                                                                    |
|  TIER 1: File-Based (siempre en contexto = "RAM")                |
|  +------------------------------------------------------------+   |
|  | MEMORY.md + memory/*.md                                     |   |
|  | Inyectados directamente en system prompt                    |   |
|  | Editados manualmente por usuario/agente                     |   |
|  +------------------------------------------------------------+   |
|                                                                    |
|  TIER 2: Semantic Search (bajo demanda = "Disco")                |
|  +------------------------------------------------------------+   |
|  | SQLite + sqlite-vec (vector) + FTS5 (keyword)               |   |
|  | Hybrid search: 70% vector + 30% BM25                        |   |
|  | Chunking: ~400 tokens, 80 tokens overlap                    |   |
|  | minScore: 0.35, maxResults: 6                               |   |
|  | Tools: memory_search(query), memory_get(path, from, lines) |   |
|  +------------------------------------------------------------+   |
|                                                                    |
|  EMBEDDING PROVIDERS:                                              |
|  OpenAI text-embedding-3-small (default)                          |
|  Gemini gemini-embedding-001                                       |
|  Voyage voyage-4-large                                             |
|  Local hf:embeddinggemma-300m (via node-llama-cpp)                |
|  Auto: local first, then remote                                   |
+-------------------------------------------------------------------+
```

### Storage (SQLite)

**Location:** `~/.openclaw/state/memory/{agentId}.sqlite`

**Tables:**

- `chunks` -- text chunks con line numbers, hashes, embeddings (JSON), model, source
- `chunks_vec` -- vector index (L2 distance via sqlite-vec)
- `chunks_fts` -- full-text search (FTS5 con BM25 ranking)
- `files` -- metadata: path, source, hash, mtime, size
- `embedding_cache` -- cache por hash + provider + model
- `meta` -- metadata como vector dimensions

### Search Pipeline

```
Query arrives
    |
    v
1. Warm session if configured (on-demand sync)
    |
    v
2. Hybrid search (parallel)
   +-- Vector search: cosine similarity en embeddings normalizados (L2)
   +-- Keyword search: FTS5 BM25 ranking
    |
    v
3. Merge results
   Score = (0.7 * vector_score) + (0.3 * text_score)
    |
    v
4. Filter: minScore >= 0.35
    |
    v
5. Return top 6 results
```

### Synchronization

- Triggered by: session start, search (if dirty), file watcher, interval timer
- Detecta cambios via hash comparison
- Deletes stale chunks de archivos modificados/eliminados
- Indexes nuevos/modificados markdown files y session files

### Embedding Management

- Batch processing respetando limites de tokens (8000 default)
- Usa batch APIs nativas de cada provider
- Retry con exponential backoff para rate limits
- Cache de embeddings por hash (evita re-calcular mismo texto)
- L2 normalization post-generacion
- Pruning LRU cuando cache excede maxEntries

### Memory Sources

```typescript
type MemorySource = "memory" | "sessions";
// "memory"   -> MEMORY.md y memory/*.md (user-controlled)
// "sessions" -> Transcripts de conversaciones (experimental)
```

### Integracion en Agent Execution

**Fase 1: Bootstrap (pre-request)**

```
bootstrap-files.ts
    |
    v
Lee MEMORY.md + memory/*.md
    |
    v
Inyecta en system prompt como "Project Context"
```

**Fase 2: Runtime (on-demand)**

```
Agent recibe pregunta sobre trabajo previo
    |
    v
Llama memory_search(query)
    |
    v
Recibe chunks relevantes con scores
    |
    v
Llama memory_get(path, from, lines) para snippet exacto
    |
    v
Responde con cita: Source: path#L{start}-L{end}
```

### System prompt guidance (de system-prompt.ts)

```
## Memory Recall
Before answering anything about prior work, decisions, dates,
people, preferences, or todos:
run memory_search on MEMORY.md + memory/*.md;
then use memory_get to pull only needed lines.
```

### Config disponible

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "provider": "openai|local|gemini|voyage|auto",
        "model": "text-embedding-3-small",
        "sources": ["memory", "sessions"],
        "chunking": { "tokens": 400, "overlap": 80 },
        "sync": {
          "onSessionStart": true,
          "onSearch": true,
          "watch": true,
          "watchDebounceMs": 1000,
          "intervalMinutes": 5
        },
        "query": {
          "maxResults": 6,
          "minScore": 0.35,
          "hybrid": { "vectorWeight": 0.7, "textWeight": 0.3 }
        },
        "cache": { "enabled": true, "maxEntries": 10000 },
        "store": {
          "driver": "sqlite",
          "vector": { "enabled": true }
        }
      }
    }
  }
}
```

### Limitaciones del sistema de memoria de OpenClaw

1. **No hay aprendizaje implicito** -- el agente debe decidir explicitamente que guardar
2. **No hay modelado de usuario automatico** -- no extrae patrones de comportamiento
3. **No hay olvido inteligente** -- depende de borrar archivos manualmente
4. **No hay personalizacion de modelo** -- mismo modelo base para todos
5. **No hay feedback loop** -- no rastrea que respuestas funcionaron mejor
6. **No hay memory scoring** -- todas las memorias tienen el mismo peso

---

## 5. Patrones del Harness para tu WhatsApp Assistant

### 5.1 Prompt Composer con Secciones Condicionales

```typescript
interface PromptSection {
  id: string;
  content: string;
  condition?: (ctx: ConversationContext) => boolean;
  priority: number; // menor = primero
}

function buildPrompt(sections: PromptSection[], ctx: ConversationContext): string {
  return sections
    .filter((s) => !s.condition || s.condition(ctx))
    .sort((a, b) => a.priority - b.priority)
    .map((s) => s.content)
    .join("\n\n");
}

// Ejemplo: herramientas solo si el usuario tiene permisos
const toolsSection: PromptSection = {
  id: "tools",
  content: toolsMarkdown,
  condition: (ctx) => ctx.user.role === "admin",
  priority: 50,
};
```

### 5.2 Channel Capabilities para WhatsApp

````typescript
const whatsappCapabilities = {
  markdown: {
    bold: true, // *bold*
    italic: true, // _italic_
    strikethrough: true, // ~strikethrough~
    monospace: true, // ```code```
    headers: false, // NO soporta #
    links: false, // NO soporta [text](url)
    tables: false, // NO soporta tablas
    lists: "manual", // Usar "- " o "* " manualmente
  },
  media: {
    images: true,
    audio: true,
    documents: true,
    maxMessageLength: 4096,
  },
  features: {
    reactions: true,
    messageEditing: false,
    buttons: true, // Quick reply buttons (limitados)
    lists: true, // List messages
  },
};

// Inyectar en system prompt:
const channelInstructions = `
## Formato de respuesta (WhatsApp)
- Usa *negrita* para enfasis, NO **doble asterisco**
- Usa _cursiva_ para notas secundarias
- NO uses headers (#), tablas, ni links markdown
- Maximo 4096 caracteres por mensaje; divide si necesitas mas
- Para listas usa "- " o "1. " manualmente
- URLs se envian tal cual (WhatsApp las convierte en clickeables)
`;
````

### 5.3 Message Batching

```typescript
// WhatsApp: usuarios envian mensajes fragmentados
// "Oye" -> "necesito que" -> "me ayudes con algo"
// Sin batching = 3 respuestas. Con batching = 1 respuesta.

const userQueues = new Map<string, AsyncQueue>();

async function handleIncomingMessage(userId: string, message: Message) {
  if (!userQueues.has(userId)) {
    userQueues.set(userId, new AsyncQueue());
  }

  const queue = userQueues.get(userId)!;

  await queue.enqueue(async () => {
    // Esperar 2-3 segundos por si llegan mas mensajes
    await delay(2500);
    const pendingMessages = await getPendingMessages(userId);
    const combinedInput = pendingMessages.map((m) => m.text).join("\n");

    const response = await processWithAgent(userId, combinedInput);
    await sendWhatsAppResponse(userId, response);
  });
}
```

### 5.4 Context Compaction

```typescript
const MAX_CONTEXT_TOKENS = 150_000;
const COMPACTION_THRESHOLD = 0.8;

async function manageContext(messages: Message[], tokenCount: number): Promise<Message[]> {
  if (tokenCount > MAX_CONTEXT_TOKENS * COMPACTION_THRESHOLD) {
    const oldMessages = messages.slice(0, -10);
    const recentMessages = messages.slice(-10);

    const summary = await generateText({
      model: anthropic("claude-haiku-4-5-20251001"),
      prompt: `Resume esta conversacion en puntos clave:\n${formatMessages(oldMessages)}`,
    });

    return [
      { role: "system", content: `## Resumen de conversacion anterior\n${summary.text}` },
      ...recentMessages,
    ];
  }
  return messages;
}
```

### 5.5 Approval Gates (Human-in-the-Loop)

```typescript
interface ApprovalGate {
  action: string;
  requiresApproval: boolean;
  approver: "user" | "admin";
  timeout: number;
  fallback: "cancel" | "queue";
}

async function executeWithApproval(
  action: AgentAction,
  gate: ApprovalGate,
  whatsappClient: WhatsAppClient,
): Promise<ActionResult> {
  if (!gate.requiresApproval) return execute(action);

  await whatsappClient.sendMessage(userId, {
    text: `*Accion pendiente*\n\n${action.preview}\n\nResponde *SI* para aprobar o *NO* para cancelar.`,
  });

  const response = await waitForUserResponse(userId, gate.timeout);
  if (response === "SI") return execute(action);
  return { status: "cancelled", reason: "user_rejected" };
}
```

### 5.6 Heartbeat (Agente Proactivo)

```typescript
interface ScheduledTask {
  id: string;
  userId: string;
  cron: string;
  prompt: string;
  channel: "whatsapp";
  requiresApproval: boolean;
}

// Ejemplos:
const tasks: ScheduledTask[] = [
  {
    id: "morning-briefing",
    userId: "user_123",
    cron: "0 8 * * 1-5", // 8 AM L-V
    prompt: "Envia resumen de agenda, tareas pendientes y recordatorios.",
    channel: "whatsapp",
    requiresApproval: false,
  },
  {
    id: "weekly-report",
    userId: "user_123",
    cron: "0 18 * * 5", // Viernes 6 PM
    prompt: "Genera resumen semanal con metricas y prioridades.",
    channel: "whatsapp",
    requiresApproval: true,
  },
];
```

### 5.7 Skills Modulares

```typescript
interface Skill {
  id: string;
  name: string;
  description: string;
  instructions: string; // Markdown para inyectar en prompt
  tools: ToolDefinition[];
  enabled: (ctx: UserContext) => boolean;
}

// Skill de ejemplo
const calendarSkill: Skill = {
  id: "calendar",
  name: "Google Calendar",
  description: "Gestiona eventos del calendario",
  instructions: `## Calendario
Puedes crear, editar y consultar eventos.
- Confirma fecha, hora y timezone antes de crear
- Si dice "manana" usa su timezone configurada`,
  tools: [createEventTool, listEventsTool],
  enabled: (ctx) => ctx.user.plan === "premium" && ctx.user.calendarConnected,
};

// Composicion dinamica
function getActiveSkills(ctx: UserContext): Skill[] {
  return allSkills.filter((s) => s.enabled(ctx));
}
```

### 5.8 Middleware Pipeline (inspirado en hooks de OpenClaw)

```typescript
type HookEvent =
  | "message:received"
  | "message:sending"
  | "agent:before"
  | "agent:after"
  | "tool:before"
  | "tool:after";

interface Hook {
  event: HookEvent;
  priority: number;
  handler: (ctx: HookContext) => Promise<HookContext | void>;
}

// Hooks practicos:
const hooks: Hook[] = [
  // Rate limiting
  { event: "message:received", priority: 90, handler: rateLimitHook },
  // Logging
  { event: "message:received", priority: 100, handler: loggingHook },
  // Budget check
  { event: "agent:before", priority: 80, handler: budgetCheckHook },
  // Token tracking
  { event: "agent:after", priority: 50, handler: usageTrackingHook },
  // WhatsApp formatting
  { event: "message:sending", priority: 10, handler: whatsappFormatHook },
];
```

### 5.9 Budget Management por Usuario

```typescript
interface UserBudget {
  userId: string;
  plan: "free" | "pro" | "enterprise";
  limits: {
    messagesPerDay: number; // free: 20, pro: 200, enterprise: unlimited
    tokensPerDay: number; // free: 50K, pro: 500K, enterprise: 5M
    toolCallsPerDay: number; // free: 5, pro: 50, enterprise: 500
    proactiveTasksPerDay: number; // free: 0, pro: 5, enterprise: unlimited
  };
  usage: {
    messagesUsed: number;
    tokensUsed: number;
    toolCallsUsed: number;
    lastReset: Date;
  };
}
```

### 5.10 Failover Multi-Modelo

```typescript
import { generateText } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import { openai } from "@ai-sdk/openai";

const modelChain = [
  anthropic("claude-sonnet-4-20250514"),
  openai("gpt-4o"),
  anthropic("claude-haiku-4-5-20251001"),
];

async function generateWithFailover(params: GenerateParams): Promise<string> {
  for (const model of modelChain) {
    try {
      const result = await generateText({ model, ...params });
      return result.text;
    } catch (error) {
      if (isRateLimit(error)) {
        await delay(exponentialBackoff());
        continue;
      }
      if (isBillingError(error)) {
        await notifyAdmin(error);
        continue;
      }
      throw error;
    }
  }
  throw new Error("All models exhausted");
}
```

---

## 6. Las 5 Capas de Personalizacion Profunda

La diferencia entre un chatbot y un asistente personal: un chatbot responde preguntas; un asistente te conoce.

```
+---------------------------------------------------------------+
| Capa 5: Modelo Dedicado                                        |
|   Adaptar pesos del modelo al usuario                          |
|   (LoRA, destilacion, P2P)                                    |
+---------------------------------------------------------------+
| Capa 4: Aprendizaje Activo                                     |
|   El AI pregunta estrategicamente                              |
|   (GATE, elicitation, A/B responses)                          |
+---------------------------------------------------------------+
| Capa 3: User Modeling Dinamico                                 |
|   Extrae patrones automaticamente                              |
|   (reflection pass, implicit signals, feedback loop)           |
+---------------------------------------------------------------+
| Capa 2: Memoria Estructurada                                   |
|   Recuerda hechos y contexto entre sesiones                    |
|   (Mem0, Zep, Letta)                                          |
+---------------------------------------------------------------+
| Capa 1: Prompt Personalizado                                   |
|   Info del usuario en system prompt                            |
|   (USER.md pattern)                                            |
+---------------------------------------------------------------+

     Profundidad de personalizacion --->
     Inversion requerida           --->
```

### Capa 1: Prompt Personalizado

Lo basico. Inyectar info del usuario en system prompt.

```typescript
interface UserProfile {
  id: string;
  name: string;
  language: string;
  timezone: string;
  preferences: {
    verbosity: "concise" | "detailed";
    formality: "casual" | "professional" | "formal";
    topics: string[];
  };
  context: string; // markdown libre
}
```

**Limitacion:** Estatico. Alguien tiene que actualizar manualmente.

### Capa 2: Memoria Estructurada

El agente guarda y recupera informacion entre conversaciones.

**Tipos de memoria a almacenar:**

| Tipo         | Ejemplo                         | Uso                         |
| ------------ | ------------------------------- | --------------------------- |
| Hechos       | "Mi empresa se llama Acme Corp" | Contexto siempre disponible |
| Preferencias | "Prefiere resumenes cortos"     | Ajustar formato             |
| Decisiones   | "Decidimos usar PostgreSQL"     | Mantener coherencia         |
| Relaciones   | "Juan es su socio"              | Resolver referencias        |
| Temporal     | "Lanzamiento el 15 mayo"        | Recordatorios proactivos    |
| Emocional    | "Estresado con deadline"        | Ajustar tono                |

Ver seccion 7 para frameworks recomendados.

### Capa 3: User Modeling Dinamico

**Esto es lo que OpenClaw NO hace y es la oportunidad.**

Basado en PRIME (EMNLP 2025): el modelado humano tiene dos sistemas de memoria:

- **Episodica:** eventos especificos ("la semana pasada hablamos de X")
- **Semantica:** conocimiento general ("prefiere respuestas tecnicas")

La semantica es MAS ROBUSTA para personalizacion.

#### Reflection Pass (post-conversacion)

```typescript
async function reflectOnConversation(userId: string, conversation: Message[]): Promise<void> {
  const reflectionPrompt = `
Analiza esta conversacion y extrae SOLO informacion nueva sobre el usuario.

Categorias:
1. PREFERENCIAS DE COMUNICACION: largo, formalidad, emojis, idioma
2. PATRONES DE COMPORTAMIENTO: horarios, tipos de preguntas, reacciones
3. CONOCIMIENTO Y EXPERTISE: nivel tecnico, dominio de trabajo
4. CONTEXTO DE VIDA: proyectos, personas, preocupaciones
5. PREFERENCIAS IMPLICITAS: reformulaciones (= no entendio), 
   pidio mas detalle (= quiere profundidad), 
   corto la conversacion (= quiere brevedad)

MEMORIA EXISTENTE:
${existingMemory}

CONVERSACION:
${formatConversation(conversation)}

Responde en JSON:
{
  "new_facts": [{"category": "...", "fact": "...", "confidence": 0.0-1.0}],
  "updated_facts": [{"id": "...", "update": "...", "reason": "..."}],
  "invalidated_facts": [{"id": "...", "reason": "..."}]
}`;

  const reflection = await generateText({
    model: anthropic("claude-haiku-4-5-20251001"), // modelo barato
    prompt: reflectionPrompt,
  });

  await updateUserModel(userId, JSON.parse(reflection.text));
}
```

#### Senales implicitas en WhatsApp

| Senal                           | Indica                      | Como captar                               |
| ------------------------------- | --------------------------- | ----------------------------------------- |
| Reformula pregunta              | No entendio respuesta       | Detectar preguntas similares consecutivas |
| "ok"/"gracias" rapido           | Satisfecho, quiere brevedad | Analizar largo de respuestas              |
| Envia audio                     | Comunicacion informal       | Trackear media types                      |
| Escribe a 11 PM                 | Nocturno, relajado          | Timestamp analysis                        |
| "Explicame como si fuera X"     | Nivel bajo en ese tema      | Ajustar depth por tema                    |
| Muchos mensajes cortos          | Stream-of-consciousness     | Activar batching                          |
| No responde a mensaje proactivo | No fue util                 | Reducir frecuencia                        |

### Capa 4: Aprendizaje Activo

Basado en GATE (ICLR 2025): LLMs que hacen preguntas abiertas obtienen preferencias MAS INFORMATIVAS que prompts del usuario.

#### 3 fases de elicitation

```
Fase 1: Onboarding (conversaciones 1-3)
  Preguntas directas pero naturales:
  "Como prefieres que te responda? Directo o con contexto?"
  "En que trabajas? Asi doy respuestas mas relevantes"

Fase 2: Micro-elicitation (conversaciones 4-20)
  Preguntas sutiles en respuestas:
  "Te envio resumen corto. Prefieres mas detalle la proxima?"
  Ofrecer 2 estilos y ver cual elige

Fase 3: Refinamiento (ongoing)
  Solo con incertidumbre alta:
  "La ultima vez usaste X. Sigo con ese enfoque?"
  Deteccion de drift si preferencias cambiaron
```

```typescript
interface ElicitationStrategy {
  trigger: (ctx: ConversationContext, userModel: UserModel) => boolean;
  question: (ctx: ConversationContext, userModel: UserModel) => string;
  priority: number;
  cooldown: number; // ms entre preguntas
}
```

**Regla:** NUNCA mas de 1 pregunta de elicitation por conversacion.

### Capa 5: Modelo Dedicado

Ver seccion 8 para detalles completos.

---

## 7. Frameworks de Memoria (Estado del Arte 2025-2026)

El espacio de memoria AI en 2026 se siente como el de vector databases en 2022: muchas soluciones compitiendo, benchmark wars, y consolidacion acercandose.

### Comparativa Principal

| Framework          | Fortaleza                                  | Debilidad                        | Best For              |
| ------------------ | ------------------------------------------ | -------------------------------- | --------------------- |
| **Mem0**           | Facil integracion, 3 scopes, hybrid store  | Menos control sobre que recuerda | MVP rapido            |
| **Zep (Graphiti)** | Razonamiento temporal, knowledge graph     | Mas complejo                     | Relaciones temporales |
| **Letta**          | Agente maneja su memoria (OS-style)        | Opinionado                       | Control maximo        |
| **Hindsight**      | 4 redes (world/bank/opinion/observation)   | Relativamente nuevo              | Precision maxima      |
| **Memvid**         | No DB, MP4 storage, ultra-rapido           | Enfoque no convencional          | Alto throughput       |
| **LangMem**        | Integra con LangGraph, prompt optimization | Ecosistema LangChain             | Si ya usas LangGraph  |

### Mem0 (Recomendado para tu MVP)

- 26% mas preciso que OpenAI Memory (benchmark LOCOMO)
- 91% menos tokens que full-context
- 90% respuestas mas rapidas
- SDK en TypeScript y Python
- Cloud (app.mem0.ai) + self-hosted
- 3 scopes: user, session, agent

```typescript
import { MemoryClient } from "mem0ai";
import { generateText } from "ai";

const memory = new MemoryClient({ apiKey: process.env.MEM0_API_KEY });

async function handleMessage(userId: string, message: string) {
  // 1. Recuperar memorias relevantes
  const memories = await memory.search(message, { user_id: userId });

  // 2. Generar respuesta con contexto
  const result = await generateText({
    model: anthropic("claude-sonnet-4-20250514"),
    system: buildPrompt(userId, memories),
    messages: conversationHistory,
  });

  // 3. Guardar nuevas memorias
  await memory.add(
    [
      { role: "user", content: message },
      { role: "assistant", content: result.text },
    ],
    { user_id: userId },
  );

  return result.text;
}
```

### Zep (Graphiti) -- Para relaciones temporales

- Knowledge graph temporalmente-aware
- 18.5% accuracy improvement, 90% latency reduction
- 15 puntos mas en LongMemEval para temporal reasoning
- Entiende transiciones: "Alice era budget owner hasta febrero, luego Bob"
- Integrado con Amazon Neptune

### Letta (ex-MemGPT) -- Para control maximo

- Paradigma "LLM-as-Operating-System"
- **Core Memory:** siempre en contexto (como RAM), editable via API
- **Recall Memory:** historial completo en disco, buscable
- **Archival Memory:** DB externa, el agente gestiona explicitamente
- Agentes son participantes ACTIVOS en su propia memoria
- REST API + SDKs Python/TypeScript

### Hindsight -- Para maxima precision

- 4 redes logicas: World (hechos), Bank (experiencias), Opinion (juicios), Observation (entidades)
- 91.4% accuracy en LongMemEval
- Multi-session: de 21.1% a 79.7%
- Temporal reasoning: de 31.6% a 79.7%

### Taxonomia de Memoria AI

Basada en Endel Tulving (1972), adaptada para AI:

```
MEMORIA
+-- Por tipo:
|   +-- Episodica: eventos especificos pasados
|   +-- Semantica: hechos, preferencias, conocimiento
|   +-- Procedural: comportamientos aprendidos, workflows
|
+-- Por storage:
|   +-- Token-level: texto explicito en context window
|   +-- Parametric: conocimiento en pesos del modelo
|   +-- Latent: hidden states y embeddings
|
+-- Por scope (Mem0):
    +-- User: persistente, cross-session
    +-- Session: dentro de una conversacion
    +-- Agent: del propio agente (sus preferencias/reglas)
```

---

## 8. Modelos Dedicados y Especializados

### 8A. Drift: Personalizacion en Decode-Time (CERO entrenamiento)

**ICLR 2025**

- Descompone preferencias en combinaciones ponderadas de atributos
- Guia generacion en espacio de logits durante inferencia
- NO modifica el modelo
- Necesita solo 50-100 ejemplos de preferencias
- Performance comparable a RLHF
- Zero costo de entrenamiento por usuario
- **Limitacion:** requiere acceso a logits -> solo modelos open-source

### 8B. LoRA/QLoRA Adapters por Segmento

NO un adapter por usuario, sino por SEGMENTO:

```
Segmento "Ejecutivo"     -> LoRA: conciso, corporativo, bullets
Segmento "Desarrollador" -> LoRA: codigo, tecnico, detallado
Segmento "Estudiante"    -> LoRA: paso-a-paso, analogias, pedagogico
```

**Costos (2026):**

- QLoRA fine-tune 7B model: ~$10-50 por adapter (RunPod/Modal)
- Cada adapter: ~5-50 MB
- Inference: misma latencia que base
- Hot-swap en runtime

**Flujo:**

```
Datos de usuarios
    |
    v
Clustering por patrones
    |
    v
Segmentos definidos
    |
    v
Fine-tune LoRA por segmento
    |
    v
Deploy adapters
    |
    v
Router: usuario -> segmento -> adapter -> inference
```

### 8C. Profile-to-PEFT (P2P) -- Adapter instantaneo por usuario

**arXiv 2510.16282**

- Hypernetwork toma perfil codificado del usuario
- Genera directamente parametros LoRA completos
- 33x mas rapido que LoRA individual (0.57s vs 20.44s)
- Escala a cantidad arbitraria de usuarios
- Costo marginal ~cero post-entrenamiento del hypernetwork
- **Estado:** investigacion reciente, no production-ready aun

### 8D. Destilacion Personalizada

```
Claude Opus (teacher)
    |
    | genera datos de alta calidad en tu dominio
    |
    v
Modelo destilado 7B (student)
    -> 50-70% menos costo de inference
    -> Latencia mucho menor
    -> Personalizado para tu caso de uso
```

**Cuando vale la pena:**

- > 1000 usuarios activos
- 80% conversaciones son temas predecibles
- Costo de Claude/GPT es significativo
- Quieres latencia <3s para WhatsApp

### 8E. Fine-Tuning via APIs de Providers

| Provider  | Modelo       | Costo Training        | Costo Inference    |
| --------- | ------------ | --------------------- | ------------------ |
| OpenAI    | GPT-4.1      | $25/M tokens          | $2/$8 per M        |
| OpenAI    | GPT-4o-mini  | $3/M tokens           | $0.30/$1.20 per M  |
| OpenAI    | o4-mini (RL) | $100/hour             | varies             |
| Anthropic | --           | No ofrece fine-tuning | via prompt caching |

### Approach de cada provider para personalizacion

**Anthropic (Claude):**

- Memory feature (sept 2025, ahora en free tier)
- Extrae hechos derivados, no transcripciones
- Categorias: Role & Work, Projects, Personal, Communication prefs
- Prompt caching: 90% ahorro en cache reads, 85% reduccion latencia
- NO ofrece fine-tuning API

**OpenAI (ChatGPT):**

- "Saved memories" + "Chat history"
- Projects con persistent files
- Custom GPTs (pero SIN memoria, cada conversacion es nueva)
- Fine-tuning API completo

**Google (Gemini):**

- Gems (personas especializadas)
- Memory automatica (agosto 2025)
- "Saved Info" como long-term memory
- Temporary chats (auto-delete 72h)

---

## 9. Mas Alla del Harness -- Otras Implementaciones

### 9A. Memory Confidence Scoring

```typescript
interface Memory {
  content: string;
  confidence: number; // 0.0 - 1.0
  source:
    | "explicit" // usuario dijo directamente
    | "inferred" // sistema infirio
    | "observed"; // patron de comportamiento
  lastVerified: Date;
  usageCount: number;
  contradictions: number;
}

// Decay: confianza baja con el tiempo si no se reconfirma
function decayConfidence(memory: Memory): number {
  const daysSinceVerified = daysBetween(memory.lastVerified, new Date());
  const decay = memory.source === "explicit" ? 0.001 : 0.01;
  return Math.max(0.1, memory.confidence - daysSinceVerified * decay);
}
```

### 9B. Personalidad Evolutiva del Asistente

```
Semana 1:  Formal, cuidadoso, muchas preguntas
Semana 4:  Mas casual, sabe contexto, anticipa necesidades
Mes 3:    Casi un colega, usa jerga del usuario, humor contextual
```

Implementar modificando dinamicamente la "soul" del agente basandose en depth de relacion (conversaciones totales, dias de interaccion, temas cubiertos).

### 9C. Anticipacion Proactiva (Predictive Actions)

```typescript
// Detectar patrones temporales
const patterns = await detectTemporalPatterns(userId);

// Si usuario consulta metricas todos los lunes a las 9 AM...
// ...enviar briefing el lunes a las 8:50 AM
if (pattern.confidence > 0.8 && pattern.occurrences > 3) {
  scheduleProactiveMessage(userId, {
    time: pattern.expectedNext - 10 * 60 * 1000,
    prompt: `Preparar briefing de ${pattern.topic}`,
  });
}
```

### 9D. Implicit Feedback Loop

| Senal positiva          | Senal negativa                |
| ----------------------- | ----------------------------- |
| Continua conversacion   | Deja de responder             |
| "Perfecto", "gracias"   | Reformula pregunta            |
| Forward a alguien       | "no" o corrige                |
| Vuelve al tema otro dia | Cambia de tema abruptamente   |
| Responde rapido         | Largo silencio post-respuesta |

```typescript
function estimateSatisfaction(response: AssistantMessage, userReaction: UserBehavior): number {
  let score = 0.5;
  if (userReaction.continuedConversation) score += 0.1;
  if (userReaction.saidThanks) score += 0.2;
  if (userReaction.reformulated) score -= 0.3;
  if (userReaction.responseTimeMs < 5000) score += 0.1;
  if (userReaction.responseTimeMs > 300000) score -= 0.1;
  if (userReaction.forwardedMessage) score += 0.3;
  return Math.max(0, Math.min(1, score));
}
```

### 9E. Knowledge Graph Personal

```
[Usuario] --trabaja_en--> [Acme Corp]
[Acme Corp] --industria--> [Fintech]
[Acme Corp] --usa--> [PostgreSQL]
[Usuario] --conoce--> [Juan (socio)]
[Juan] --trabaja_en--> [Acme Corp]
[Usuario] --proyecto--> [App de pagos]
[App de pagos] --deadline--> [15 Mayo 2026]
[App de pagos] --stack--> [Next.js, PostgreSQL]
```

Zep con Graphiti es la mejor opcion: temporally-aware, sabe que "Alice era PM hasta febrero, ahora es Bob."

### 9F. Observabilidad

```typescript
interface InteractionLog {
  id: string;
  userId: string;
  timestamp: Date;
  input: { message: string; messageType: string };
  agent: {
    model: string;
    tokensInput: number;
    tokensOutput: number;
    latencyMs: number;
    toolCalls: { name: string; durationMs: number }[];
    cost: number;
  };
  output: { message: string; messageCount: number };
  metadata: {
    sessionId: string;
    skillsUsed: string[];
    memoryRetrieved: boolean;
    compacted: boolean;
    satisfactionScore: number;
  };
}
```

**Metricas clave para WhatsApp:**

- Latencia de respuesta (usuarios esperan <10s)
- Costo por conversacion / por usuario
- Tasa de uso de skills
- Retencion (conversaciones/semana)
- Tasa de compactacion

---

## 10. Arquitectura Recomendada

```
+----------------------------------------------------------------+
|                  WhatsApp Business API                           |
|                  (Webhook Inbound)                               |
+----------------------------+-----------------------------------+
                             |
                             v
                +---------------------------+
                |   MIDDLEWARE PIPELINE      |
                |                           |
                |  +-- Rate Limiter         |
                |  +-- Auth & Session       |
                |  +-- Language Detector    |
                |  +-- Message Batcher     |
                |  +-- Budget Checker      |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   SESSION MANAGER         |
                |                           |
                |  +-- Load user context    |
                |  +-- Memory retrieval     |
                |       (Mem0 / Zep)        |
                |  +-- History management   |
                |  +-- Compaction check     |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   PROMPT COMPOSER         |
                |                           |
                |  +-- Identity section     |
                |  +-- Soul/tone section    |
                |  +-- User profile section |
                |  +-- Active skills        |
                |  +-- Memory context       |
                |  +-- Channel capabilities |
                |  +-- Instructions         |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   AI SDK AGENT            |
                |                           |
                |  +-- generateText/stream  |
                |  +-- Tool execution       |
                |  +-- Model failover       |
                |  +-- Token tracking       |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   OUTPUT PIPELINE         |
                |                           |
                |  +-- WhatsApp formatting  |
                |  +-- Message splitting    |
                |  +-- Approval gates       |
                |  +-- Satisfaction scoring |
                |  +-- Logging/metrics      |
                +-------------+-------------+
                              |
                              v
                +---------------------------+
                |   WhatsApp Business API   |
                |   (Send Response)         |
                +---------------------------+

+---------------------------+     +---------------------------+
|   BACKGROUND WORKERS      |     |   LEARNING ENGINE         |
|                           |     |                           |
|  +-- Cron / Heartbeat     |     |  +-- Reflection pass     |
|  +-- Proactive messages   |     |  +-- Signal detection    |
|  +-- Pattern detection    |     |  +-- User model update   |
|  +-- Reminder scheduling  |     |  +-- Confidence decay    |
+---------------------------+     +---------------------------+
```

### Comparativa OpenClaw vs Tu Producto

| Dimension          | OpenClaw                           | Tu Producto (Recomendado)                 |
| ------------------ | ---------------------------------- | ----------------------------------------- |
| **Config**         | Markdown files en workspace        | Markdown files + DB por usuario           |
| **Prompt**         | Composicion dinamica por secciones | Secciones condicionales + AI SDK          |
| **Memoria**        | File-based + SQLite vector         | Mem0 (3-tier: user/session/agent)         |
| **User Modeling**  | Manual (USER.md)                   | Automatico (reflection + signals)         |
| **Aprendizaje**    | No tiene                           | Feedback loop implicito + active learning |
| **Contexto**       | Compactacion + history limits      | Compactacion + sliding window             |
| **Aprobacion**     | Telegram como canal                | WhatsApp inline (quick replies)           |
| **Proactividad**   | Heartbeat cron jobs                | Pattern detection + predictive            |
| **Skills**         | 54+ bundled + workspace custom     | Modular por plan de suscripcion           |
| **Hooks**          | Plugin lifecycle hooks             | Middleware pipeline                       |
| **Multi-canal**    | 15+ canales                        | WhatsApp primary + web dashboard          |
| **Failover**       | Multi-model + multi-auth           | AI SDK provider failover                  |
| **Observabilidad** | OpenTelemetry + file logging       | Structured logging + analytics            |
| **Budget**         | Per-campaign API limits            | Per-user token/message limits             |
| **Modelo**         | Mismo para todos                   | Segmented LoRA + destilacion              |
| **Personalidad**   | Estatica (SOUL.md)                 | Evolutiva por relacion                    |
| **Knowledge**      | Flat markdown                      | Knowledge graph temporal                  |

---

## 11. Roadmap de Implementacion

### Fase 1: Fundacion (Semanas 1-2)

- [ ] Prompt composer modular (markdown files)
- [ ] Channel capabilities para WhatsApp
- [ ] Message batching (2-3 seg delay)
- [ ] Context compaction (Haiku para resumir)
- [ ] Budget tracking por usuario
- [ ] Failover multi-modelo (AI SDK)
- [ ] Logging estructurado

### Fase 2: Memoria (Semanas 3-4)

- [ ] Integrar Mem0 para memoria persistente
- [ ] Tipos: hechos, preferencias, decisiones, relaciones, temporal
- [ ] Reflection pass post-conversacion (Haiku)
- [ ] Memory search antes de responder
- [ ] Memory confidence scoring

### Fase 3: Aprendizaje (Semanas 5-8)

- [ ] User modeling dinamico (senales implicitas)
- [ ] Satisfaction scoring implicito
- [ ] Active learning (preguntas estrategicas)
- [ ] Onboarding inteligente (3 primeras conversaciones)
- [ ] Personalidad evolutiva del asistente

### Fase 4: Proactividad (Semanas 9-12)

- [ ] Heartbeat/cron para mensajes proactivos
- [ ] Deteccion de patrones temporales
- [ ] Anticipacion predictiva
- [ ] Approval gates para acciones importantes
- [ ] Skills modulares por plan

### Fase 5: Modelo Dedicado (Mes 4+)

- [ ] Destilacion: Claude Opus -> modelo 7B especializado
- [ ] LoRA adapters por segmento de usuario
- [ ] Knowledge graph personal (Zep/Graphiti)
- [ ] Evaluacion con PersonalLLM benchmark
- [ ] Profile-to-PEFT cuando madure

---

## 12. Referencias y Fuentes

### OpenClaw

- OpenClaw Official: https://openclaw.ai/
- GitHub: https://github.com/openclaw/openclaw
- Wikipedia: https://en.wikipedia.org/wiki/OpenClaw
- Agent Workspace Docs: https://docs.openclaw.ai/concepts/agent-workspace
- Configuration: https://docs.openclaw.ai/gateway/configuration
- SOUL.md Guide: https://clawdocs.org/guides/soul-md/

### Investigacion Academica

- PRIME (EMNLP 2025): Cognitive dual-memory for LLM personalization
- Drift (ICLR 2025): Efficient implicit personalization at decode-time
- GATE (ICLR 2025): Generative Active Task Elicitation
- PersonalLLM (ICLR 2025): Benchmark for evaluating personalization
- PeaPOD: Personalized Prompt Distillation (arXiv 2407.05033)
- PersonaMem: Dynamic profile memory benchmark (arXiv 2504.14225)
- Profile-to-PEFT (arXiv 2510.16282): Hypernetwork for instant LoRA
- LD-Agent (NAACL 2025): Long-short term memory personas

### Frameworks de Memoria

- Mem0: https://docs.mem0.ai/introduction | GitHub: https://github.com/mem0ai/mem0
- Zep (Graphiti): https://www.getzep.com/ | arXiv 2501.13956
- Letta: https://docs.letta.com/concepts/letta/ | GitHub: https://github.com/letta-ai/letta
- Hindsight: https://github.com/vectorize-io/hindsight
- Memvid: https://memvid.com
- LangMem: via LangGraph ecosystem

### Fine-Tuning y Modelos

- LoRA/QLoRA guide: https://www.index.dev/blog/top-ai-fine-tuning-tools-lora-vs-qlora-vs-full
- OpenAI fine-tuning pricing: https://platform.openai.com/docs/pricing/
- Anthropic prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Model distillation explained: https://www.quantamagazine.org/how-distillation-makes-ai-models-smaller-and-cheaper-20250718/

### Providers - Personalizacion

- Claude Memory: https://support.claude.com/en/articles/10185728
- ChatGPT Memory: https://openai.com/index/memory-and-new-controls-for-chatgpt/
- Gemini Memory: https://gemini.google/overview/gems/

---

> **Nota:** Este documento es una referencia viva. Actualizar conforme se implementen las fases y surjan nuevos frameworks/tecnicas.
