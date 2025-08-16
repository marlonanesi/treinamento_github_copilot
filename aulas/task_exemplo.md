# Tarefa Copilot: Reajuste Salarial com Faixas por Cargo + Auditoria

Objetivo:
Implementar um endpoint para reajuste salarial de funcionários com validação de faixas por cargo e registro de auditoria do reajuste (histórico), respeitando a arquitetura em camadas do ms-cadastro-funcionario.

Resumo da Feature:
- Novo endpoint: PATCH /funcionarios/{id}/salario
- Modos de reajuste: percentual ou absoluto
- Validação de faixa salarial por cargo
- Auditoria: registrar histórico de reajustes (quem, quando, antes/depois, motivo)
- Log estruturado da operação

Regras de Negócio:
- Salário nunca pode ser negativo.
- Reajuste percentual permitido entre -50% e +100%.
- Faixas por cargo (exemplo; parametrizar/centralizar):
  - DESENVOLVEDOR_JUNIOR: 3000.00–6000.00
  - DESENVOLVEDOR_PLENO: 6000.00–12000.00
  - DESENVOLVEDOR_SENIOR: 12000.00–20000.00
  - Cargos personalizados: 2000.00–50000.00 (default)
- Se funcionário ainda não tem salário (None), só aceitar modo absoluto.
- Atualizar updated_at a cada reajuste.
- Registrar histórico em salario_historico (lista append-only).

Contrato HTTP:
- Rota: PATCH /funcionarios/{funcionario_id}/salario
- Headers: X-User-Id (opcional; default "system")
- Body (um dos modos):
  - { "modo": "percentual", "valor": 10.0, "motivo": "Ajuste anual" }
  - { "modo": "absoluto", "valor": 7500.00, "motivo": "Promoção" }
- Response: SuccessResponseSchema[FuncionarioResponseSchema] com salário atualizado (salario_historico pode ser omitido na resposta pública para não vazar detalhes; deixar no documento apenas).
- Status: 200, 400 (dados), 404 (não encontrado), 422 (violação de regra), 409 (conflito, se aplicável).

Auditoria (persistência):
- Campo novo na entidade/documento: salario_historico: List[dict]
- Item do histórico:
  {
    "anterior": <Decimal|float>,
    "novo": <Decimal|float>,
    "modo": "percentual" | "absoluto",
    "valor_aplicado": <float>,        // percentual ou absoluto
    "percentual": <float|null>,        // preencher quando modo=percentual
    "motivo": <str>,
    "solicitado_por": <str>,
    "data": <datetime UTC ISO>
  }

Observabilidade:
- Log estruturado no caso de uso com event=salary_adjustment, funcionario_id, modo, valor, anterior, novo.

Diretrizes de Implementação (arquivos-alvo):

- app/domain/entities/funcionario.py
  - Adicionar atributo opcional salario_historico: List[Dict[str, Any]] = field(default_factory=list)
  - Adicionar método:
    def reajustar_salario(self, *, modo: Literal["percentual","absoluto"], valor: Decimal | float, motivo: str, solicitado_por: str = "system") -> None
    - Validar entradas, aplicar regra de faixa por cargo (criar helper para obter faixa por cargo).
    - Calcular novo salário:
      - percentual: novo = atual * (1 + valor/100)
      - absoluto: novo = valor
    - Validar min/max, não-negativo, e regras especiais (None → somente absoluto).
    - Atualizar self.salario e self.updated_at.
    - Append no self.salario_historico com payload definido.
  - Opcional: mover ranges para value_objects.Cargo ou constante no módulo.

- app/domain/entities/value_objects.py
  - Adicionar método utilitário no Cargo/TiposCargo:
    TiposCargo.get_salary_range(value: str) -> tuple[Decimal, Decimal]
    - Implementar lógica dos ranges acima; para personalizados retornar default.

- app/application/use_cases/ajustar_salario.py (novo arquivo)
  - Criar use case:
    class AjustarSalarioUseCase(UseCase[AjustarSalarioRequest, FuncionarioResponse])
    - Steps: buscar por id → chamar entidade.reajustar_salario(...) → repository.atualizar(entidade) → mapear para response.
    - Mapear exceptions de domínio para application/HTTP.

- app/presentation/schemas/funcionario_schemas.py
  - Adicionar schema de entrada:
    class AjusteSalarioSchema(BaseSchema):
      modo: Literal["percentual","absoluto"]
      valor: condecimal(gt=0) | confloat(gt=0)  // permitir percentual negativo? Use validator custom para -50% a +100%
      motivo: constr(min_length=3, max_length=140)
    - Validator: quando modo="percentual", permitir -50.0 ≤ valor ≤ 100.0; quando absoluto, valor > 0.
  - Não expor salario_historico no response público (mantém interface atual).

- app/presentation/api/v1/funcionarios.py
  - Adicionar rota PATCH /{funcionario_id}/salario
  - Ler header X-User-Id (optional).
  - Chamar use case, retornar SuccessResponseSchema.
  - Mapear erros para 400/404/422/409 conforme regras.

- app/infrastructure/database/models.py
  - Incluir salario_historico no from_entity/to_entity e no documento.
  - Garantir conversão Decimal ↔ float e datetime ↔ ISODate.
  - to_update_document: incluir salario e, quando presente, push no salario_historico (pode salvar como substituição completa se estratégia atual não usa $push; manter simples: salvar a lista inteira atualizada).

- app/infrastructure/repositories/funcionario_repository_impl.py
  - Reutilizar atualizar(funcionario) para persistir salário e histórico.
  - Garantir que o update salve salario_historico (evitar sobrescrever nulo).

- app/presentation/api/__init__.py | app/main.py
  - Garantir inclusão do novo endpoint no router (se modularizado).

Erros/Exceptions:
- DadosInvalidosException(campo="salario", regra="SALARY_OUT_OF_RANGE" | "PERCENTUAL_RANGE" | "NEGATIVE_SALARY" | "MODO_INVALIDO")
- FuncionarioNaoEncontradoException em fetch
- ValidationException do schema de entrada

Testes (Definition of Done):
- Unidade (domain/entities/funcionario.py)
  - Feliz: absoluto de 7000.00 quando atual=6000.00 (cargo PLENO) → OK, histórico append.
  - Feliz: +10% quando atual=10000.00 (cargo SENIOR) → 11000.00, histórico append.
  - Triste: percentual +150% → rejeitar (422 domain: PERCENTUAL_RANGE).
  - Triste: absoluto abaixo do mínimo do cargo → rejeitar (422 SALARY_OUT_OF_RANGE).
  - Triste: percentual com salário atual None → rejeitar (422).
  - Triste: resultado negativo → rejeitar.
- Unidade (value_objects.Cargo/TiposCargo)
  - get_salary_range retorna min/max corretos para cargos pré-definidos e default para personalizados.
- Unidade (application/use_cases/ajustar_salario.py)
  - Feliz: executa fluxo, chama repository.atualizar com entidade alterada.
  - Triste: id inexistente → mapear 404.
  - Triste: violação de regra → mapear 422.
- Infra (infrastructure/database/models.py)
  - Roundtrip com salario_historico preserva dados.
  - to_update_document inclui salario e salario_historico conforme esperado.
- Infra (repositories/funcionario_repository_impl.py)
  - Atualização persiste o novo salário e histórico.
- API (presentation/api/v1/funcionarios.py)
  - PATCH com modo absoluto retorna 200 e salário atualizado.
  - PATCH com modo percentual fora do range retorna 422.
  - PATCH com id inválido retorna 400/404 conforme validação existente.
  - Header X-User-Id populado em solicitado_por; sem header → "system".

Cobertura e Validações (targets):
- Cobertura mínima:
  - Domain/value_objects: ≥95%
  - Use case: ≥90%
  - Infra models/repository: ≥85%
  - API: ≥85%
- Lint/format: flake8, black, isort sem violações.
- Tipagem (opcional): mypy sem erros nas camadas domain e application.
- OpenAPI atualizado: novo endpoint aparece no Swagger.
- Logs contendo event=salary_adjustment.

Critérios de Aceite (Done):
- Todos os testes passam com as coberturas mínimas.
- Novo endpoint disponível e documentado.
- Regras de faixa por cargo aplicadas.
- Histórico de salário persistido e consultável no documento (sem expor no response público).
- Nenhum breaking change nos endpoints existentes.

Dicas de Implementação:
- Centralizar ranges por cargo em um único lugar (value_objects ou config).
- Usar Decimal nas operações para evitar imprecisão; converter para float apenas na fronteira de persistência.
- Normalizar motivo (strip, tamanho) no schema.
- Manter consistência de exceptions com o mapeamento atual da API.

Comandos:
- Testes: pytest tests/ -v --cov=app --cov-report=term-missing
- Lint: flake8 app/ && black --check app/ && isort --check-only app/
- Run: uvicorn main:app --reload
