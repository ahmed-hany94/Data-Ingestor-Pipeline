# --- Stage 1: Build ---
FROM oven/bun:1-alpine AS builder

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build   # requires output: 'standalone' in next.config.ts

# --- Stage 2: Runtime ---
FROM oven/bun:1-alpine AS runtime

WORKDIR /app
ENV NODE_ENV=production

# Standalone output bundles only what's needed to run — no full node_modules copy
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD bun -e "fetch('http://localhost:3000/api/healthz').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["bun", "server.js"]