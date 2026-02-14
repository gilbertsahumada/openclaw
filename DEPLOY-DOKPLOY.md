# OpenClaw - Despliegue en Dokploy

## Requisitos previos

- Servidor con Dokploy instalado
- Token de OpenAI API (`OPENAI_API_KEY`)
- (Opcional) Bot de Telegram creado via `@BotFather` (`TELEGRAM_BOT_TOKEN`)

## 1. Crear el bot de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envia `/newbot`
3. Sigue las instrucciones (nombre y username del bot)
4. Copia el token que te devuelve (formato: `123456:ABCDEF...`)

## 2. Crear el proyecto en Dokploy

1. En Dokploy, ve a **Projects** > **Create Project**
2. Dale un nombre (ej: `openclaw`)
3. Dentro del proyecto, clic en **+ Create Service** > **Compose** (NO Application)
4. Conecta tu repositorio de GitHub o pega el contenido del `docker-compose.yml`
5. Si conectas el repo, en **Watch Path** pon `/`

> **Importante**: No uses "Application" con Dockerfile. Este setup usa imagenes pre-construidas
> de `ghcr.io`, no necesita buildear nada. Debe ser tipo **Compose**.

## 3. Estructura del proyecto

```
openclaw/
├── docker-compose.yml          # Configuracion de servicios
├── config/
│   └── openclaw.json           # Configuracion de canales (Telegram, etc.)
├── DEPLOY-DOKPLOY.md           # Esta guia
```

## 4. docker-compose.yml

```yaml
services:
  openclaw-gateway:
    image: ghcr.io/openclaw/openclaw:latest
    restart: unless-stopped
    environment:
      HOME: /home/node
      TERM: xterm-256color
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
    volumes:
      - openclaw_config:/home/node/.openclaw
      - openclaw_workspace:/home/node/.openclaw/workspace
      - ./config/openclaw.json:/home/node/.openclaw/openclaw.json:ro
    init: true
    expose:
      - "18789"
    networks:
      - dokploy-network
    command:
      ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789", "--allow-unconfigured"]

  openclaw-cli:
    image: ghcr.io/openclaw/openclaw:latest
    environment:
      HOME: /home/node
      TERM: xterm-256color
      OPENCLAW_GATEWAY_TOKEN: ${OPENCLAW_GATEWAY_TOKEN}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      BROWSER: echo
    volumes:
      - openclaw_config:/home/node/.openclaw
      - openclaw_workspace:/home/node/.openclaw/workspace
    stdin_open: true
    tty: true
    init: true
    networks:
      - dokploy-network
    entrypoint: ["node", "dist/index.js"]

volumes:
  openclaw_config:
  openclaw_workspace:

networks:
  dokploy-network:
    external: true
```

### Notas sobre el compose

- `--allow-unconfigured`: Necesario para que el gateway arranque sin haber ejecutado `openclaw setup`
- `expose` en vez de `ports`: Dokploy maneja el reverse proxy, no necesitamos exponer puertos al host
- `init: true`: Manejo limpio de senales y procesos zombie dentro del contenedor
- `dokploy-network` (external): Red creada automaticamente por Dokploy
- Named volumes (`openclaw_config`, `openclaw_workspace`): Persisten datos entre reinicios
- `./config/openclaw.json` montado como `:ro` (read-only): Configuracion de canales desde el repo
- El servicio `openclaw-cli` es opcional - se usa para interaccion manual. Se sale automaticamente al no tener terminal interactiva conectada, eso es normal

## 5. Configuracion de canales

El archivo `config/openclaw.json` define que canales estan activos:

```json
{
  "channels": {
    "telegram": {
      "enabled": true
    }
  }
}
```

Para agregar mas canales, edita este archivo:

```json
{
  "channels": {
    "telegram": {
      "enabled": true
    },
    "discord": {
      "enabled": true
    }
  }
}
```

Los tokens de cada canal se pasan como variables de entorno (ver seccion siguiente).

## 6. Variables de entorno

En Dokploy, seccion **Environment**, agrega estas variables:

| Variable | Requerida | Descripcion | Ejemplo |
|---|---|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | Si | Token interno para autenticar gateway y CLI | Generalo con `openssl rand -hex 32` |
| `OPENAI_API_KEY` | Si | API key de OpenAI | `sk-proj-...` |
| `TELEGRAM_BOT_TOKEN` | No | Token del bot de Telegram | `123456:ABCDEF...` |
| `DISCORD_BOT_TOKEN` | No | Token del bot de Discord | `MTIz...` |
| `SLACK_BOT_TOKEN` | No | Token del bot de Slack | `xoxb-...` |
| `SLACK_APP_TOKEN` | No | Token de app de Slack (Socket Mode) | `xapp-...` |

### Generar OPENCLAW_GATEWAY_TOKEN

```bash
openssl rand -hex 32
```

Copia el resultado y pegalo como valor de la variable en Dokploy.

## 7. Desplegar

1. Configura las variables de entorno en Dokploy
2. Haz clic en **Deploy**
3. Verifica en los logs que el gateway inicie correctamente
4. El contenedor `openclaw-cli` aparecera como "exited" - eso es **normal** (es interactivo)
5. El contenedor `openclaw-gateway` debe aparecer como "running"

## 8. Verificar que funciona

Entra a la **terminal** del contenedor `openclaw-gateway` desde Dokploy y ejecuta:

```bash
cd /app && node dist/index.js channels list
```

> **Nota**: El binario de openclaw esta en `/app/dist/index.js`. El comando `openclaw`
> no esta en el PATH dentro del contenedor, siempre usa `node dist/index.js` desde `/app`.

Deberias ver los canales configurados listados.

## 9. Aprobar pairing de Telegram

Cuando le escribas al bot por primera vez, te dara un codigo de pairing.

Para aprobarlo, entra a la terminal del contenedor `openclaw-gateway` desde Dokploy:

```bash
cd /app && node dist/index.js pairing approve telegram <CODIGO>
```

O desde tu servidor via SSH:

```bash
docker exec <nombre-contenedor-gateway> sh -c "cd /app && node dist/index.js pairing approve telegram <CODIGO>"
```

## 10. Troubleshooting

### El gateway se reinicia constantemente
- **"Missing config"**: Verifica que `--allow-unconfigured` este en el command del gateway y que `config/openclaw.json` este montado correctamente
- **Error de red al desplegar** (`connection reset by peer`): Reintenta el deploy, suele ser un error temporal de red al bajar la imagen de ghcr.io

### El CLI aparece como "exited"
- Es **normal**. El CLI necesita terminal interactiva y no puede correr como daemon. Usalo solo desde la terminal de Dokploy cuando necesites ejecutar comandos

### Canales vacios en `channels list`
- Verifica que `config/openclaw.json` tenga el canal habilitado (`"enabled": true`)
- Verifica que la variable de entorno del token este configurada en Dokploy

### No encuentro el comando `openclaw`
- Dentro del contenedor, el binario no esta en el PATH
- Siempre usa: `cd /app && node dist/index.js <comando>`

## Canales soportados

OpenClaw soporta 22+ canales. Los mas comunes:

| Canal | Variable de entorno | Dificultad |
|---|---|---|
| Telegram | `TELEGRAM_BOT_TOKEN` | Facil |
| Discord | `DISCORD_BOT_TOKEN` | Facil |
| Slack | `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` | Media |
| WhatsApp | Login con QR | Media |
| Google Chat | Service Account JSON | Media |
| Signal | signal-cli | Dificil |

Para documentacion detallada de cada canal, revisa `docs/channels/` en el repositorio.
