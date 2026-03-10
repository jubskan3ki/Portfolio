#!/bin/bash
set -e

APP_DIR="/app"

echo "Setting up permissions..."

# Create directories
dirs=("logs" "media" "staticfiles" "swagger" "media/blog" "media/projects" "media/user")
for dir in "${dirs[@]}"; do
    mkdir -p "$APP_DIR/$dir"
    chmod 755 "$APP_DIR/$dir"
done

# Make scripts executable
chmod +x "$APP_DIR"/scripts/*.sh "$APP_DIR"/scripts/*.py "$APP_DIR"/manage.py 2>/dev/null || true

# Create log files
touch "$APP_DIR/logs/django_errors.log" "$APP_DIR/logs/setup.log" 2>/dev/null || true
chmod 644 "$APP_DIR"/logs/*.log 2>/dev/null || true

echo "Permissions configured successfully"
