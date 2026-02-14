# OpenClaw - Despliegue en Dokploy

## Requisitos previos

- Servidor con Dokploy instalado
- Token de OpenAI API (`OPENAI_API_KEY`)
- Bot de Telegram creado via `@BotFather` (`TELEGRAM_BOT_TOKEN`)

## 1. Crear el bot de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envia `/newbot`
3. Sigue las instrucciones (nombre y username del bot)
4. Copia el token que te devuelve (formato: `123456:ABCDEF...`)

## 2. Crear el proyecto en Dokploy

1. En Dokploy, ve a **Projects** > **Create Project**
2. Dale un nombre (ej: `openclaw`)
3. Dentro del proyecto, clic en **+ Create Service** > **Compose**
4. Pega el contenido del `docker-compose.yml` (ver seccion abajo)

## 3. docker-compose.yml

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
    init: true
    expose:
      - "18789"
    networks:
      - dokploy-network
    command:
      ["node", "dist/index.js", "gateway", "--bind", "lan", "--port", "18789"]

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

## 4. Variables de entorno

En Dokploy, seccion **Environment**, agrega estas variables:

| Variable | Descripcion | Ejemplo |
|---|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | Token interno para autenticar gateway y CLI | Un string seguro generado por ti |
| `OPENAI_API_KEY` | API key de OpenAI | `sk-proj-...` |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | `123456:ABCDEF...` |

## 5. Desplegar

1. Guarda la configuracion del compose en Dokploy
2. Agrega las variables de entorno
3. Haz clic en **Deploy**
4. Verifica en los logs que el gateway inicie correctamente

## 6. Aprobar pairing de Telegram

Cuando le escribas al bot por primera vez, te dara un codigo de pairing.

Para aprobarlo, entra a la terminal del contenedor `openclaw-gateway` desde Dokploy y ejecuta:

```bash
node dist/index.js pairing approve telegram <CODIGO>
```

O desde tu servidor via SSH:

```bash
docker exec <nombre-contenedor-gateway> node dist/index.js pairing approve telegram <CODIGO>
```

## 7. Verificar

- Escribe al bot en Telegram y confirma que responde
- Revisa los logs del contenedor `openclaw-gateway` en Dokploy si hay errores

## Notas

- La red `dokploy-network` es creada automaticamente por Dokploy (por eso se marca como `external: true`)
- Los named volumes (`openclaw_config`, `openclaw_workspace`) persisten datos entre reinicios
- Se usa `expose` en vez de `ports` porque Dokploy maneja el reverse proxy internamente
- `init: true` asegura un manejo limpio de procesos dentro del contenedor

## Canales adicionales

OpenClaw soporta 22+ canales. Para agregar mas, define las variables de entorno correspondientes:

| Canal | Variable de entorno |
|---|---|
| Telegram | `TELEGRAM_BOT_TOKEN` |
| Discord | `DISCORD_BOT_TOKEN` |
| Slack | `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` |

Para configuracion avanzada de canales, edita `openclaw.json` dentro del volumen `openclaw_config`.
