#!/bin/bash
# ClaudeTrader — Iniciar interface Streamlit
cd "$(dirname "$0")"
streamlit run app.py --server.port 8501 --server.headless false
