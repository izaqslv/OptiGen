📘 🧠 GUIA PRÁTICO — GIT (OPTIGEN)
👉 Você pode salvar isso como:
README_DEPLOY.md

🚀 🔹 1. FLUXO NORMAL (USO DO DIA A DIA)
# Verifica status do repositório
git status

# Adiciona todas as alterações
git add .

# Cria commit (descreva o que foi feito)
git commit -m "feat: melhorias no sistema de autenticação"

# Envia para o GitHub
git push origin main

🚀 🔹 2. QUANDO O REPOSITÓRIO JÁ EXISTE (PRIMEIRA VEZ)
# Inicializa git (se ainda não tiver)
git init

# Define branch principal
git branch -M main

# Conecta ao repositório remoto
git remote add origin https://github.com/SEU_USUARIO/optigen-backend.git

# Envia código
git push -u origin main

🚀 🔹 3. FORÇAR ATUALIZAÇÃO (SOBRESCREVER TUDO NO GITHUB)
👉 ⚠️ CUIDADO: isso apaga o histórico remoto
Use quando:
✔ quer limpar versões antigas
✔ remover lixo
✔ recomeçar com versão limpa

🔥 COMANDO
# Adiciona tudo
git add .

# Commit da versão limpa
git commit -m "reset: clean version production ready"

# FORÇA envio (sobrescreve GitHub)
git push origin main --force

🧠 O QUE ISSO FAZ
👉 Substitui completamente o repositório remoto:
ANTES:
v1 → v2 → v3 → bagunça
DEPOIS:
v_clean 🚀

🚀 🔹 4. VERIFICAR CONEXÃO COM GITHUB
git remote -v
Saída esperada:
origin  https://github.com/... (fetch)
origin  https://github.com/... (push)

🚀 🔹 5. CORRIGIR REPOSITÓRIO REMOTO
git remote remove origin

git remote add origin https://github.com/SEU_USUARIO/optigen-backend.git

🚀 🔹 6. IGNORAR ARQUIVOS (MUITO IMPORTANTE)
Crie .gitignore:
# Ambiente virtual
venv/

# IDE
.idea/

# Banco local
optigen.db

# Cache
__pycache__/
*.pyc

# Variáveis sensíveis
.env

🚀 🔹 7. GERAR REQUIREMENTS ATUALIZADO
pip freeze > requirements.txt

🚀 🔹 8. BOAS PRÁTICAS DE COMMIT
feat: nova funcionalidade
fix: correção de bug
refactor: melhoria de código
docs: documentação
Exemplo:
git commit -m "fix: swagger auth token"

🚀 🔹 9. DEPLOY AUTOMÁTICO
👉 Backend (Render):
✔ git push → deploy automático
👉 Frontend (Streamlit):
✔ git push → atualiza automaticamente

🚀 🔹 10. CHECK FINAL (APÓS DEPLOY)
Testar:
https://optigen.onrender.com/docs
✔ login
✔ register
✔ endpoints 🔒

🧠 RESUMO EXECUTIVO
👉 Dia a dia:
git add .
git commit -m "msg"
git push
👉 Reset total:
git push --force
