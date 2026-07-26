# --- Stage 1: Build ---
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Cache dependencies separately from source for faster rebuilds
COPY go.mod go.sum* ./
RUN go mod download

COPY . .

# Static binary: no libc dependency at runtime, CGO disabled
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /app/bin/ingestion-api ./cmd/main.go

# --- Stage 2: Runtime ---
FROM alpine:3.19 AS runtime

# TLS root certs, in case the service ever calls out over HTTPS
RUN apk add --no-cache ca-certificates && \
    addgroup -S app && adduser -S app -G app

WORKDIR /app
COPY --from=builder /app/bin/ingestion-api .

USER app
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:8080/healthz || exit 1

ENTRYPOINT ["./ingestion-api"]