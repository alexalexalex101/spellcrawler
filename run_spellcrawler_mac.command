#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# === Kill anything on port 5000 first ===
echo "Killing any process using port 5000..."
lsof -ti :5000 | xargs kill -9 2>/dev/null

# === Open Terminal window #1 -> allow_server.py ===
osascript <<EOF
tell application "Terminal"
    do script "cd \"$SCRIPT_DIR\"; echo 'Starting allow_server.py...'; python3 allow_server.py"
end tell
EOF

sleep 1

# === Open Terminal window #2 -> Docker build + run ===
osascript <<EOF
tell application "Terminal"
    do script "cd \"$SCRIPT_DIR\"; \
        echo 'Building Docker image...'; \
        docker build -t spellcrawler-img .; \
        echo 'Running crawler...'; \
        docker run --rm \
            -v \"$SCRIPT_DIR/docs:/app/docs\" \
            -v \"$SCRIPT_DIR/custom_words.txt:/app/custom_words.txt\" \
            -v \"$SCRIPT_DIR/output:/app/output\" \
            spellcrawler-img; \
        echo 'Opening report...'; \
        open \"$SCRIPT_DIR/output/spell_report.html\""
end tell
EOF

echo "=== SpellCrawler launched in two terminals ==="
