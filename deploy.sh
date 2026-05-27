#!/bin/bash
# Deploy script for APP_Invest
# Usage: ./deploy.sh [build|run|restart|logs|stop|status]
#
# Runs Docker commands on the OCI server via SSH
# (Docker is not available in the local environment)

set -e

SSH_HOST="ubuntu@167.126.22.28"
REMOTE_DIR="/home/opc/projetos/meu-projeto-x"
APP_NAME="app-investidor"

case "${1:-status}" in
  build)
    echo ">> Building Docker image on OCI..."
    ssh "$SSH_HOST" "cd $REMOTE_DIR && sudo docker build -t ${APP_NAME}:latest ."
    echo ">> Build complete."
    ;;
  run)
    echo ">> Starting container on OCI..."
    ssh "$SSH_HOST" "cd $REMOTE_DIR && sudo docker run -d \
      --name ${APP_NAME} \
      --restart always \
      -p 80:8080 \
      -v ${REMOTE_DIR}/data:/app/data \
      ${APP_NAME}:latest"
    echo ">> Container started."
    ;;
  restart)
    echo ">> Restarting container..."
    ssh "$SSH_HOST" "sudo docker restart ${APP_NAME}"
    ;;
  logs)
    ssh "$SSH_HOST" "sudo docker logs ${APP_NAME}"
    ;;
  stop)
    echo ">> Stopping container..."
    ssh "$SSH_HOST" "sudo docker stop ${APP_NAME} && sudo docker rm ${APP_NAME}"
    echo ">> Container stopped and removed."
    ;;
  status)
    echo ">> Container status:"
    ssh "$SSH_HOST" "sudo docker ps --filter name=${APP_NAME} --format 'table {{.ID}}\t{{.Status}}\t{{.Ports}}'"
    echo ""
    echo ">> HTTP check:"
    curl -s -o /dev/null -w "HTTP %{http_code}\n" http://167.126.22.28:80/ || echo "unreachable"
    ;;
  *)
    echo "Usage: $0 [build|run|restart|logs|stop|status]"
    exit 1
    ;;
esac
