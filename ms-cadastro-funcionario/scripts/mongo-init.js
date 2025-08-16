// Script de inicialização do MongoDB para MS Funcionários
// Este script é executado automaticamente quando o container MongoDB inicia

print('Iniciando configuração do banco de dados...');

// Conectar ao banco de dados da aplicação
db = db.getSiblingDB('funcionarios_db');

// Pular criação de usuários quando --noauth está habilitado
print('⚠️  Executando sem autenticação (--noauth)');
print('💡 Pulando criação de usuários...');

// Criar coleção de funcionários se não existir
if (!db.funcionarios.findOne()) {
    db.createCollection('funcionarios');
    print('✅ Coleção funcionarios criada');
}

// Criar índices essenciais
print('📊 Criando índices...');

// Índice único para email
db.funcionarios.createIndex(
    { "email": 1 }, 
    { 
        unique: true, 
        name: "idx_email_unique",
        background: true
    }
);
print('  ✅ Índice único para email criado');

// Índice para CPF (único também)
db.funcionarios.createIndex(
    { "cpf": 1 }, 
    { 
        unique: true, 
        name: "idx_cpf_unique",
        background: true,
        sparse: true  // Permite documentos sem CPF
    }
);
print('  ✅ Índice único para CPF criado');

// Índice para departamento (consultas frequentes)
db.funcionarios.createIndex(
    { "departamento": 1 }, 
    { 
        name: "idx_departamento",
        background: true
    }
);
print('  ✅ Índice para departamento criado');

// Índice para cargo (consultas frequentes)
db.funcionarios.createIndex(
    { "cargo": 1 }, 
    { 
        name: "idx_cargo",
        background: true
    }
);
print('  ✅ Índice para cargo criado');

// Índice composto para filtros por departamento e cargo
db.funcionarios.createIndex(
    { "departamento": 1, "cargo": 1 }, 
    { 
        name: "idx_departamento_cargo",
        background: true
    }
);
print('  ✅ Índice composto departamento+cargo criado');

// Índice para status (ativo/inativo)
db.funcionarios.createIndex(
    { "status": 1 }, 
    { 
        name: "idx_status",
        background: true
    }
);
print('  ✅ Índice para status criado');

// Índice para data de criação (auditoria e ordenação)
db.funcionarios.createIndex(
    { "created_at": 1 }, 
    { 
        name: "idx_created_at",
        background: true
    }
);
print('  ✅ Índice para created_at criado');

// Índice para data de admissão (consultas por período)
db.funcionarios.createIndex(
    { "data_admissao": 1 }, 
    { 
        name: "idx_data_admissao", 
        background: true
    }
);
print('  ✅ Índice para data_admissao criado');

// Índice para salário (filtros por faixa salarial)
db.funcionarios.createIndex(
    { "salario": 1 }, 
    { 
        name: "idx_salario",
        background: true
    }
);
print('  ✅ Índice para salário criado');

// Índice de texto para busca textual (nome, sobrenome, email)
db.funcionarios.createIndex(
    {
        "nome": "text",
        "sobrenome": "text", 
        "email": "text"
    },
    {
        name: "idx_text_search",
        background: true,
        weights: {
            "nome": 10,
            "sobrenome": 5,
            "email": 1
        }
    }
);
print('  ✅ Índice de busca textual criado');

// Inserir documento de exemplo (opcional, para desenvolvimento)
if (db.funcionarios.countDocuments() === 0) {
    print('📝 Inserindo funcionário de exemplo...');
    
    const exemploFuncionario = {
        nome_completo: 'João Silva Santos',
        email: 'joao.silva@empresa.com.br',
        telefone: '(11) 99999-9999',
        data_admissao: new Date('2020-01-15'),
        cargo: 'Desenvolvedor Pleno',
        departamento: 'Tecnologia',
        salario: 8500.00,
        ativo: false,
        created_at: new Date(),
        updated_at: new Date()
    };
    
    try {
        db.funcionarios.insertOne(exemploFuncionario);
        print('  ✅ Funcionário de exemplo criado');
    } catch (error) {
        print('  ⚠️  Erro ao criar funcionário exemplo (pode já existir):', error.message);
    }
}

// Verificar estatísticas finais
const stats = {
    totalFuncionarios: db.funcionarios.countDocuments(),
    totalIndices: db.funcionarios.getIndexes().length,
    tamanhoColecao: db.funcionarios.stats().size || 0
};

print('');
print('📊 Estatísticas finais:');
print('   • Total de funcionários:', stats.totalFuncionarios);
print('   • Total de índices:', stats.totalIndices);
print('   • Tamanho da coleção:', stats.tamanhoColecao, 'bytes');
print('');
print('🎉 Configuração do banco concluída com sucesso!');
print('🔧 Banco pronto para receber conexões da aplicação.');
print('');
