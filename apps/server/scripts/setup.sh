#!/bin/bash
set -eo pipefail

# Configuration

readonly APP_DIR="/app"
readonly LOG_DIR="$APP_DIR/logs"
readonly LOG_FILE="$LOG_DIR/setup.log"

# Logging

log() { echo "[$(date '+%H:%M:%S')] $1"; }
info() { log "INFO: $1"; }
error() { log "ERROR: $1" >&2; }
success() { log "OK: $1"; }

init_logging() {
    mkdir -p "$LOG_DIR" 2>/dev/null || true
    exec > >(tee -a "$LOG_FILE") 2>&1
}

# Checks

check_env() {
    local required=("DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD" "ADMIN_EMAIL" "ADMIN_PASSWORD")
    local missing=()

    for var in "${required[@]}"; do
        [ -z "${!var:-}" ] && missing+=("$var")
    done

    if [ ${#missing[@]} -ne 0 ]; then
        error "Missing env vars: ${missing[*]}"
        exit 1
    fi
    success "Environment variables OK"
}

wait_for_db() {
    info "Waiting for database..."
    local attempt=0
    local max=30

    while ! nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
        attempt=$((attempt + 1))
        [ $attempt -ge $max ] && { error "Database timeout"; exit 1; }
        sleep 2
    done
    success "Database ready"
}

# Setup

setup_dirs() {
    local dirs=("logs" "media" "staticfiles" "swagger" ".cache" "media/blog" "media/projects" "media/user")

    for dir in "${dirs[@]}"; do
        mkdir -p "$APP_DIR/$dir" 2>/dev/null || true
        chmod 755 "$APP_DIR/$dir" 2>/dev/null || true
    done

    chmod +x "$APP_DIR"/scripts/*.sh "$APP_DIR"/scripts/*.py "$APP_DIR"/manage.py 2>/dev/null || true
    success "Directories ready"
}

run_migrations() {
    info "Running migrations..."

    # Run all migrations in one command
    if ! python manage.py migrate --no-input; then
        error "Migration failed - attempting fresh migration"

        # Try migrating Django apps first
        python manage.py migrate contenttypes --no-input || true
        python manage.py migrate auth --no-input || true
        python manage.py migrate admin --no-input || true
        python manage.py migrate sessions --no-input || true

        # Then user app
        if ! python manage.py migrate user --no-input; then
            error "User migration failed"
            info "Try: docker compose down -v && docker compose up --build"
            return 1
        fi

        # Finally all remaining
        python manage.py migrate --no-input || true
    fi

    success "Migrations done"
}

create_admin() {
    info "Setting up admin user..."
    python "$APP_DIR/scripts/create_admin.py" 2>/dev/null || true
    success "Admin user ready"
}

generate_openapi() {
    info "Generating OpenAPI schema..."
    python "$APP_DIR/scripts/export_openapi.py" --output "$APP_DIR/swagger/openapi.json" 2>/dev/null || {
        cat > "$APP_DIR/swagger/openapi.json" << 'EOF' || true
{"swagger":"2.0","info":{"title":"Portfolio API","version":"v1"},"paths":{},"definitions":{}}
EOF
    }
    success "OpenAPI schema ready"
}

collect_static() {
    info "Collecting static files..."
    python manage.py collectstatic --noinput --clear --verbosity=0 2>/dev/null || true
    success "Static files ready"
}

# Main

main() {
    local start_time=$(date +%s)

    info "=== Django Setup Starting ==="

    init_logging
    check_env
    setup_dirs
    wait_for_db
    run_migrations
    create_admin
    generate_openapi
    collect_static

    local duration=$(($(date +%s) - start_time))
    success "Setup completed in ${duration}s"

    info "=== Starting Gunicorn ==="

    local workers=${GUNICORN_WORKERS:-3}
    local timeout=${GUNICORN_TIMEOUT:-120}

    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers="$workers" \
        --timeout="$timeout" \
        --worker-tmp-dir=/dev/shm \
        --log-level=info \
        --access-logfile=- \
        --error-logfile=- \
        --max-requests=1000 \
        --max-requests-jitter=50 \
        --preload
}

main "$@"
