# --- Stage 1: Build ---
FROM oven/bun:1-alpine AS builder

WORKDIR /app

COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun run build   # Vite outputs static files to dist/

# --- Stage 2: Runtime ---
FROM oven/bun:1-alpine AS runtime

WORKDIR /app
COPY --from=builder /app/dist ./dist

RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 5173

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD bun -e "fetch('http://localhost:5173/').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

CMD ["bunx", "serve", "-s", "dist", "-l", "5173"]