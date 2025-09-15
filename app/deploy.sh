#!/bin/bash
# =============================================
# Script de Deploy Automático - Trabalho DevOps Uninter
# Curso: Análise e Desenvolvimento de Sistemas
# Instituição: Uninter
# =============================================

echo "🚀 Iniciando deploy automático da aplicação DevOps..."

# 1. Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale o Docker antes de continuar."
    exit 1
fi

# 2. Constrói a imagem Docker com base no Dockerfile da pasta atual
echo "🐳 Construindo imagem Docker..."
docker build -t devops-app .

# 3. Verifica se a construção foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "❌ Falha na construção da imagem Docker."
    exit 1
fi

# 4. Roda o container, mapeando a porta 5000
echo "▶️ Executando container na porta 5000..."
docker run -d -p 5000:5000 --name devops-container devops-app

# 5. Verifica se o container está rodando
echo "🔍 Verificando status do container..."
docker ps --filter "name=devops-container" --format "table {{.Names}}\t{{.Status}}"

# 6. Informa como acessar a aplicação
echo -e "\n✅ Deploy concluído com sucesso!"
echo "👉 Acesse a aplicação em: http://localhost:5000"
echo "💡 Dica: Se estiver usando WSL ou máquina virtual, use o IP da máquina."

# 7. Mostra logs em tempo real (opcional)
echo -e "\n📄 Mostrando logs do container (pressione Ctrl+C para sair):"
docker logs -f devops-container