#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "   Simplexo Data & Mining - VM Provisioning & Setup       "
echo "=========================================================="

# 1. Update system packages
echo "[1/6] Updating APT repositories..."
sudo apt-get update -y
sudo apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    build-essential \
    libpq-dev \
    python3 \
    python3-pip \
    python3-venv \
    htop \
    iotop \
    unzip

# 2. Setup 8GB Swap File (if not already set)
if [ ! -f /swapfile ]; then
    echo "[2/6] Configuring 8GB Swap file for stability..."
    sudo fallocate -l 8G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=8192
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "Swap configured successfully."
else
    echo "[2/6] Swap already exists. Skipping."
fi

# 3. Install Docker and Docker Compose Plugin
if ! command -v docker &> /dev/null; then
    echo "[3/6] Installing Docker..."
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker "$USER" || true
    echo "Docker installed successfully."
else
    echo "[3/6] Docker already installed."
fi

# 4. Create Persistent Data Directories
echo "[4/6] Creating storage directories..."
sudo mkdir -p /data/rfb_raw /data/postgres /data/redis
sudo chown -R "$USER":"$USER" /data /opt/simplexo_data 2>/dev/null || true

# 5. Build and Start Stack via Docker Compose
echo "[5/6] Starting Simplexo Data Stack (Postgres, Redis, Gateway, Worker)..."
cd "$(dirname "$0")"
sudo docker compose up -d --build

# 6. Verify Health
echo "[6/6] Verifying container status..."
sleep 5
sudo docker compose ps

echo "=========================================================="
echo "   Simplexo Data Stack is UP and RUNNING!                "
echo "   - REST Gateway:  http://$(curl -s ifconfig.me):8000/docs"
echo "   - Health Check:  http://$(curl -s ifconfig.me):8000/health"
echo "=========================================================="
