#!/bin/bash

export $(grep -v '^#' .env | xargs)
echo "Сборка образов версии ${VERSION}..."

docker buildx create --use --name amd64-builder 2>/dev/null || docker buildx use amd64-builder

docker buildx build --platform linux/amd64 -t ${REGISTRY}/${SERVICE_NAME}:${VERSION} --push .

echo "Версия ${VERSION} загружена в GitLab Registry"
