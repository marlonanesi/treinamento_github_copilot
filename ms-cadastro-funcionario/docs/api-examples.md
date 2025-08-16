# Exemplos de API

Este documento fornece exemplos práticos de uso da API do microserviço de cadastro de funcionários.

## 🔗 Base URL
```
http://localhost:8000/api/v1
```

## 🧪 Testando a API

### Usando curl

**Health Check**:
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

### Usando HTTPie
```bash
# Instalar HTTPie
pip install httpie

# Health check
http GET localhost:8000/api/v1/health
```

### Usando Postman
1. Importe a collection: `docs/postman-collection.json`
2. Configure environment: `localhost:8000`
3. Execute os requests

## 👥 Funcionários - Exemplos Completos

### 1. Criar Funcionário

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "Ana Silva Santos",
    "email": "ana.santos@company.com",
    "cargo": "Desenvolvedora Senior",
    "data_admissao": "2024-01-15",
    "telefone": "(11) 99999-9999",
    "departamento": "Tecnologia",
    "salario": 8500.00,
    "data_nascimento": "1985-03-20",
    "ativo": true
  }'
```

**Response (201 Created)**:
```json
{
  "success": true,
  "message": "Funcionário criado com sucesso",
  "data": {
    "id": "60d5ecb74b24c3b3d8f8e1a2",
    "nome_completo": "Ana Silva Santos",
    "email": "ana.santos@company.com",
    "cargo": "Desenvolvedora Senior",
    "data_admissao": "2024-01-15",
    "telefone": "(11) 99999-9999",
    "departamento": "Tecnologia",
    "salario": 8500.00,
    "data_nascimento": "1985-03-20",
    "ativo": true,
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T10:30:00Z"
  },
  "timestamp": "2024-01-10T10:30:00Z"
}
```

### 2. Listar Funcionários

**Request Simples**:
```bash
curl -X GET "http://localhost:8000/api/v1/funcionarios"
```

**Request com Filtros**:
```bash
curl -X GET "http://localhost:8000/api/v1/funcionarios?departamento=Tecnologia&page=1&size=5"
```

**Request com Múltiplos Filtros**:
```bash
curl -X GET "http://localhost:8000/api/v1/funcionarios?cargo=Desenvolvedor&departamento=Tecnologia&ativo=true&page=1&size=10"
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Funcionários encontrados",
  "data": {
    "items": [
      {
        "id": "60d5ecb74b24c3b3d8f8e1a2",
        "nome_completo": "Ana Silva Santos",
        "email": "ana.santos@company.com",
        "cargo": "Desenvolvedora Senior",
        "departamento": "Tecnologia",
        "salario": 8500.00,
        "ativo": true,
        "created_at": "2024-01-10T10:30:00Z"
      },
      {
        "id": "60d5ecb74b24c3b3d8f8e1a3",
        "nome_completo": "João Costa Lima",
        "email": "joao.lima@company.com",
        "cargo": "Desenvolvedor Junior",
        "departamento": "Tecnologia",
        "salario": 4500.00,
        "ativo": true,
        "created_at": "2024-01-09T14:20:00Z"
      }
    ],
    "total": 2,
    "page": 1,
    "size": 10,
    "pages": 1
  },
  "timestamp": "2024-01-10T10:35:00Z"
}
```

### 3. Buscar Funcionário por ID

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2"
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Funcionário encontrado",
  "data": {
    "id": "60d5ecb74b24c3b3d8f8e1a2",
    "nome_completo": "Ana Silva Santos",
    "email": "ana.santos@company.com",
    "cargo": "Desenvolvedora Senior",
    "data_admissao": "2024-01-15",
    "telefone": "(11) 99999-9999",
    "departamento": "Tecnologia",
    "salario": 8500.00,
    "data_nascimento": "1985-03-20",
    "ativo": true,
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T10:30:00Z"
  },
  "timestamp": "2024-01-10T10:40:00Z"
}
```

### 4. Atualizar Funcionário

**Request (Atualização Parcial)**:
```bash
curl -X PUT "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2" \
  -H "Content-Type: application/json" \
  -d '{
    "cargo": "Tech Lead",
    "salario": 12000.00,
    "departamento": "Arquitetura"
  }'
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Funcionário atualizado com sucesso",
  "data": {
    "id": "60d5ecb74b24c3b3d8f8e1a2",
    "nome_completo": "Ana Silva Santos",
    "email": "ana.santos@company.com",
    "cargo": "Tech Lead",
    "data_admissao": "2024-01-15",
    "telefone": "(11) 99999-9999",
    "departamento": "Arquitetura",
    "salario": 12000.00,
    "data_nascimento": "1985-03-20",
    "ativo": true,
    "created_at": "2024-01-10T10:30:00Z",
    "updated_at": "2024-01-10T11:00:00Z"
  },
  "timestamp": "2024-01-10T11:00:00Z"
}
```

### 5. Excluir Funcionário

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2"
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Funcionário excluído com sucesso",
  "data": null,
  "timestamp": "2024-01-10T11:15:00Z"
}
```

## 🚨 Exemplos de Erro

### Funcionário Não Encontrado

**Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e999"
```

**Response (404 Not Found)**:
```json
{
  "success": false,
  "message": "Funcionário não encontrado",
  "error": {
    "type": "FuncionarioNaoEncontradoException",
    "details": "Nenhum funcionário encontrado com o ID: 60d5ecb74b24c3b3d8f8e999"
  },
  "timestamp": "2024-01-10T11:20:00Z"
}
```

### Email Duplicado

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "Outro Funcionário",
    "email": "ana.santos@company.com",
    "cargo": "Analista",
    "data_admissao": "2024-02-01"
  }'
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Dados inválidos",
  "error": {
    "type": "EmailJaExisteException",
    "details": "Já existe um funcionário cadastrado com o email: ana.santos@company.com"
  },
  "timestamp": "2024-01-10T11:25:00Z"
}
```

### Validação de Dados

**Request (Dados inválidos)**:
```bash
curl -X POST "http://localhost:8000/api/v1/funcionarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "",
    "email": "email-invalido",
    "cargo": "Dev",
    "data_admissao": "2024-13-45",
    "telefone": "123",
    "salario": -1000
  }'
```

**Response (422 Unprocessable Entity)**:
```json
{
  "success": false,
  "message": "Dados inválidos",
  "error": {
    "type": "ValidationError",
    "details": [
      {
        "field": "nome_completo",
        "message": "Nome não pode ser vazio",
        "input": ""
      },
      {
        "field": "email",
        "message": "Formato de email inválido",
        "input": "email-invalido"
      },
      {
        "field": "data_admissao",
        "message": "Data inválida",
        "input": "2024-13-45"
      },
      {
        "field": "telefone",
        "message": "Telefone deve estar no formato (XX) XXXXX-XXXX",
        "input": "123"
      },
      {
        "field": "salario",
        "message": "Salário deve ser positivo",
        "input": -1000
      }
    ]
  },
  "timestamp": "2024-01-10T11:30:00Z"
}
```

### Funcionário Ativo (Não pode excluir)

**Request**:
```bash
curl -X DELETE "http://localhost:8000/api/v1/funcionarios/60d5ecb74b24c3b3d8f8e1a2"
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Operação não permitida",
  "error": {
    "type": "FuncionarioAtivoException",
    "details": "Não é possível excluir funcionário ativo em projetos. Desative o funcionário primeiro."
  },
  "timestamp": "2024-01-10T11:35:00Z"
}
```

## 🔍 Casos de Uso Avançados

### Busca com Múltiplos Critérios

```bash
# Buscar desenvolvedores do departamento de Tecnologia, ordenados por salário
curl -X GET "http://localhost:8000/api/v1/funcionarios" \
  -G \
  -d "cargo=Desenvolvedor" \
  -d "departamento=Tecnologia" \
  -d "ativo=true" \
  -d "page=1" \
  -d "size=20"
```

### Paginação Eficiente

```bash
# Primeira página
curl -X GET "http://localhost:8000/api/v1/funcionarios?page=1&size=5"

# Próxima página
curl -X GET "http://localhost:8000/api/v1/funcionarios?page=2&size=5"

# Última página (baseada no total retornado)
curl -X GET "http://localhost:8000/api/v1/funcionarios?page=10&size=5"
```

### Filtros Combinados

```bash
# Buscar funcionários específicos por departamento e status
curl -X GET "http://localhost:8000/api/v1/funcionarios" \
  -G \
  -d "departamento=RH" \
  -d "ativo=false"

# Buscar por cargo específico
curl -X GET "http://localhost:8000/api/v1/funcionarios?cargo=Analista%20Senior"
```

## 📊 Status Codes

| Código | Significado | Quando ocorre |
|--------|-------------|---------------|
| `200` | OK | Operação bem-sucedida |
| `201` | Created | Funcionário criado |
| `400` | Bad Request | Dados inválidos ou regra de negócio violada |
| `404` | Not Found | Funcionário não encontrado |
| `422` | Unprocessable Entity | Erro de validação |
| `500` | Internal Server Error | Erro interno do servidor |

## 🛠️ Scripts Úteis

### Script de Teste Completo

```bash
#!/bin/bash
# test-api.sh

BASE_URL="http://localhost:8000/api/v1"

echo "=== Testando API ==="

# 1. Health Check
echo "1. Health Check..."
curl -s "$BASE_URL/health" | jq '.'

# 2. Criar funcionário
echo -e "\n2. Criando funcionário..."
FUNCIONARIO_ID=$(curl -s -X POST "$BASE_URL/funcionarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_completo": "Teste API User",
    "email": "teste.api@company.com",
    "cargo": "Testador",
    "data_admissao": "2024-01-15",
    "departamento": "QA"
  }' | jq -r '.data.id')

echo "Funcionário criado com ID: $FUNCIONARIO_ID"

# 3. Buscar funcionário
echo -e "\n3. Buscando funcionário..."
curl -s "$BASE_URL/funcionarios/$FUNCIONARIO_ID" | jq '.'

# 4. Listar funcionários
echo -e "\n4. Listando funcionários..."
curl -s "$BASE_URL/funcionarios?size=3" | jq '.'

# 5. Atualizar funcionário
echo -e "\n5. Atualizando funcionário..."
curl -s -X PUT "$BASE_URL/funcionarios/$FUNCIONARIO_ID" \
  -H "Content-Type: application/json" \
  -d '{"cargo": "Senior Testador"}' | jq '.'

# 6. Excluir funcionário
echo -e "\n6. Excluindo funcionário..."
curl -s -X DELETE "$BASE_URL/funcionarios/$FUNCIONARIO_ID" | jq '.'

echo -e "\n=== Teste concluído ==="
```

**Executar script**:
```bash
chmod +x test-api.sh
./test-api.sh
```

### Script de Performance

```bash
#!/bin/bash
# performance-test.sh

BASE_URL="http://localhost:8000/api/v1"

echo "=== Teste de Performance ==="

# Testar múltiplas requisições paralelas
for i in {1..10}; do
  curl -s "$BASE_URL/health" > /dev/null &
done
wait

echo "10 requisições paralelas concluídas"

# Medir tempo de resposta
time curl -s "$BASE_URL/funcionarios" > /dev/null

echo "=== Performance teste concluído ==="
```

## 📋 Collection Postman

**Exemplo de collection** (`postman-collection.json`):
```json
{
  "info": {
    "name": "MS Cadastro Funcionários",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api/v1"
    }
  ],
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "{{base_url}}/health",
          "host": ["{{base_url}}"],
          "path": ["health"]
        }
      }
    },
    {
      "name": "Criar Funcionário",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"nome_completo\": \"Teste Postman\",\n    \"email\": \"teste@company.com\",\n    \"cargo\": \"Testador\",\n    \"data_admissao\": \"2024-01-15\",\n    \"departamento\": \"QA\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/funcionarios",
          "host": ["{{base_url}}"],
          "path": ["funcionarios"]
        }
      }
    }
  ]
}
```

## 🔧 Troubleshooting de API

### Problemas Comuns

**1. CORS Error no Browser**:
```javascript
// Se testando via browser/JavaScript
fetch('http://localhost:8000/api/v1/health', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
```

**2. Certificado SSL em Desenvolvimento**:
```bash
# Ignorar SSL (apenas desenvolvimento)
curl -k https://localhost:8000/api/v1/health
```

**3. Timeout em Requests**:
```bash
# Aumentar timeout
curl --connect-timeout 10 --max-time 30 http://localhost:8000/api/v1/funcionarios
```

---

**💡 Dica**: Use o Swagger UI em `http://localhost:8000/docs` para testar interativamente todos os endpoints!
