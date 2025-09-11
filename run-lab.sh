#!/bin/bash
# run-lab.sh
# Abre la shell de Oracle Graph sin cargar jsh automático

cd "$(dirname "$0")"

chmod +x ./oracle-graph-client-22.3.0/bin/opg4j

./oracle-graph-client-22.3.0/bin/opg4j \
  --base_url http://aquiles002.sii.cl:7007 \
  --username beuser
