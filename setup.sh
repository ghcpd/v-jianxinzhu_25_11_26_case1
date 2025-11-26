#!/usr/bin/env bash
set -euo pipefail

echo "Setting up Python virtual environment and installing dependencies..."
PYTHON=${PYTHON:-python3}
VENV_DIR=".venv"

if [ ! -x "${PYTHON}" ]; then
  echo "Python executable not found: ${PYTHON}" >&2
  exit 2
fi

if [ -d "${VENV_DIR}" ]; then
  echo "Using existing venv at ${VENV_DIR}"
else
  echo "Creating venv in ${VENV_DIR}"
  ${PYTHON} -m venv "${VENV_DIR}"
fi

echo "Installing requirements..."
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -r requirements.txt
echo "Setup complete. Activate with: source ${VENV_DIR}/bin/activate"
