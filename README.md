# 🔐 TFM — Evaluación de LLMs en protocolos criptográficos

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![Status](https://img.shields.io/badge/status-Completed-success)]()

Este repositorio contiene el código, los datos y los experimentos asociados al **Trabajo de Fin de Máster en Ciberseguridad**:
  
**“Evaluación e implementación de LLMs en el análisis de protocolos criptográficos”**

El objetivo del trabajo es analizar hasta qué punto los *Large Language Models* (LLMs), tanto comerciales (GPT-4) como abiertos (Mistral 7B), pueden asistir en la auditoría de protocolos criptográficos como TLS, SSH o IPsec.  

---

## 🗂️ Estructura del repositorio

```text
TFM_LLM_Cybersecurity/
├── prompts/             # Prompts y entradas por caso (casoN_prompt.txt, casoN_input.txt/.conf)
├── responses/           # Salidas de los modelos (GPT-4 y Mistral 7B)
│   ├── gpt4/
│   └── mistral/
├── metrics/             # Tablas LaTeX por caso y metrics_master.csv (resumen)
├── scripts/             # Scripts de automatización (ejecución y métricas)
│   ├── gpt4_run_and_metrics.py
│   ├── ollama_run_and_metrics.sh
│   └── run_all_metrics.py
├── README.md            # Este archivo
└── TFM/                 # Manuscrito en LaTeX y bibliografía
```
## ⚙️ Requisitos

- Python **3.9+**
- Paquetes:  
  ```bash
  pip install openai tiktoken pandas
OpenAI API (para GPT-4):
export OPENAI_API_KEY="tu_clave_aqui"
Opcional: OPENAI_MODEL (por defecto gpt-4o).

Ollama (para Mistral 7B):
ollama pull mistral

🚀 Cómo ejecutar
Ejemplo con GPT-4 (API OpenAI):
python scripts/gpt4_run_and_metrics.py prompts/caso1_input.txt

Ejemplo con Mistral 7B (local vía Ollama):
bash scripts/ollama_run_and_metrics.sh prompts/caso1_input.txt

Ejecución completa de todos los casos:
python scripts/run_all_metrics.py

📊 Resultados
Todas las salidas se guardan en responses/modelo/casoN_modelo_out.txt.

Las métricas por caso se generan en metrics/casoN_metrics_table.tex.

El resumen agregado está en metrics/metrics_master.csv.

Ejemplo de métricas capturadas:

⏱️ Time-to-first-token (TTFT)

🚀 Tasa de tokens/s

🔢 Tokens de entrada/salida

💰 Coste estimado (solo GPT-4 vía API)

📜 Cita académica
Si utilizas este repositorio, por favor cita:

```text
@misc{alro2025tfm,
  author       = {Lucas Álvarez Rodríguez},
  title        = {Evaluación e implementación de LLMs en el análisis de protocolos criptográficos},
  year         = {2025},
  institution  = {Universidad de Alcalá},
  note         = {Trabajo de Fin de Máster en Ciberseguridad},
  url          = {https://github.com/LucasAlRo/TFM_LLM_Cybersecurity}
}
```
📧 Contacto
👤 Lucas Álvarez Rodríguez
📩 GitHub | LinkedIn

✨ Este repositorio busca contribuir a la investigación sobre el papel de los LLMs en seguridad informática, promoviendo transparencia, reproducibilidad y soberanía tecnológica.
