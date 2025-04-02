#!/bin/sh


echo "----------- Run migrations -----------"
alembic upgrade head

echo "----------- Run api -----------"
uvicorn endpoints.proxy_client:app --host 0.0.0.0 --port 8000 --reload --use-colors