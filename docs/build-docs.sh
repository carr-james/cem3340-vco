#!/bin/bash

# Docker-based local Antora documentation preview script
# Matches the production build environment exactly
# Run from repository root: docs/build-docs-docker.sh

set -e

# Get to repository root if running from docs directory
if [ -f "local-site.yml" ]; then
    cd ..
fi

echo "=================================="
echo "Building Component Documentation Preview (Docker)"
echo "=================================="

# Check if we're in the repository root
if [ ! -f "docs/local-site.yml" ]; then
    echo "ERROR: docs/local-site.yml not found. Run this script from the repository root."
    exit 1
fi

echo "Pulling Docker container..."
docker pull ghcr.io/carr-james/eurorack-docker:latest

echo ""
echo "Building site in Docker container..."
docker run --rm \
    -v "$(pwd):/work" \
    -w /work \
    -e LOCAL_USER_ID="$(id -u)" \
    -e LOCAL_GROUP_ID="$(id -g)" \
    ghcr.io/carr-james/eurorack-docker:latest \
    bash -c "
        set -e

        echo 'Installing Antora dependencies...'
        cd docs
        if [ ! -d node_modules ]; then
            npm install --no-package-lock
        else
            echo 'Antora dependencies already installed.'
        fi

        echo 'Building Antora site...'
        if npx antora local-site.yml; then
            echo 'Antora build completed successfully'
        else
            echo 'ERROR: Antora build failed'
            exit 1
        fi
        cd ..

        echo 'Fixing file ownership...'
        chown -R \$LOCAL_USER_ID:\$LOCAL_GROUP_ID /work/docs/build /work/docs/node_modules /work/hardware/**/kibot-output 2>/dev/null || true
    "

# Check if build succeeded
if [ -d "docs/build/site" ]; then
    echo ""
    echo "=================================="
    echo "✓ Build successful!"
    echo "=================================="
    echo ""
    echo "To view the documentation:"
    echo "  cd docs/build/site && python3 -m http.server 8000"
    echo "  Then open: http://localhost:8000/cem3340-vco/stable/"
    echo ""
    echo "NOTE: This is a local preview of this component only."
    echo "For the full unified site, see: https://carr-james.github.io/eurorack-docs"
    echo ""
else
    echo ""
    echo "=================================="
    echo "✗ Build failed!"
    echo "=================================="
    exit 1
fi
