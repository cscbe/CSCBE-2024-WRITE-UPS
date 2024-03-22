if ! [ -f models/mistral-7b-instruct-v0.2.Q4_K_S.gguf ]; then
  echo "Downloading LLM";
  curl -L -O --output-dir models/ https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_S.gguf
fi

sudo docker compose up --build --remove-orphans

