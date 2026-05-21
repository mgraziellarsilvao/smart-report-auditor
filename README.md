# Smart Report Auditor

Ferramenta em Python e Streamlit para auditoria automática de relatórios operacionais.

O projeto permite que o usuário faça upload de um arquivo CSV ou Excel e receba uma leitura inicial sobre qualidade da base, alertas críticos, gráficos automáticos e diagnóstico executivo.

## Objetivo

O objetivo é reduzir retrabalho em rotinas administrativas, operacionais e analíticas, identificando problemas antes que a base seja usada em dashboards, apresentações executivas ou processos de tomada de decisão.

Este projeto foi desenhado para demonstrar uma abordagem de especialista em dados e processos: não apenas visualizar informações, mas validar a confiabilidade da base antes da análise.

## Problema de negócio

Em áreas administrativas e operacionais, relatórios costumam circular em Excel ou CSV com problemas como:

- campos vazios;
- duplicidades;
- datas fora de padrão;
- categorias escritas de formas diferentes;
- valores negativos ou zerados;
- colunas obrigatórias ausentes;
- inconsistências que só aparecem depois que o dashboard já foi atualizado.

Esses problemas geram retrabalho, perda de confiança nos indicadores e dificuldade para tomar decisões rápidas.

## Solução proposta

O Smart Report Auditor automatiza uma primeira camada de validação da base.

A ferramenta avalia:

- estrutura da base;
- colunas recomendadas;
- campos vazios;
- duplicidades;
- valores numéricos suspeitos;
- possíveis outliers;
- inconsistências textuais;
- score de qualidade;
- diagnóstico executivo.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- OpenPyXL
- GitHub
- Streamlit Cloud

## Estrutura do projeto

```text
smart-report-auditor/
├── app.py
├── auditor.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── exemplo_relatorio_operacional.csv
└── docs/
    ├── gamma_prompt.md
    ├── lovable_prompt.md
    ├── linkedin_post.md
    └── roadmap.md
```

## Como executar localmente

1. Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/smart-report-auditor.git
cd smart-report-auditor
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
```

3. Ative o ambiente virtual:

No Windows:

```bash
.venv\Scripts\Activate.ps1
```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Execute o app:

```bash
streamlit run app.py
```

## Como testar

Use o arquivo de exemplo disponível em:

```text
data/exemplo_relatorio_operacional.csv
```

Esse arquivo contém problemas intencionais para testar a auditoria, como duplicidades, campo vazio, valor negativo, valor zerado, variação textual e data fora de padrão.

## Valor de negócio

A proposta do projeto é apoiar rotinas de dados, processos e operações com uma camada simples de validação preventiva.

Antes de criar um dashboard ou enviar uma análise para tomada de decisão, a base precisa ser confiável.

Este projeto contribui para:

- reduzir retrabalho;
- antecipar erros;
- melhorar qualidade da informação;
- aumentar confiabilidade dos indicadores;
- apoiar governança de dados operacionais;
- transformar validações manuais em um fluxo reutilizável.

## Possíveis evoluções

- Permitir regras customizadas por tipo de relatório;
- Exportar relatório de auditoria em Excel;
- Criar alertas por criticidade;
- Comparar duas versões de relatório;
- Integrar com Power BI;
- Integrar com SharePoint;
- Gerar diagnóstico com IA via API;
- Criar histórico de auditorias por arquivo.

## Posicionamento profissional

Este projeto faz parte de uma trilha de portfólio voltada a dados operacionais, processos administrativos, automação analítica e melhoria contínua.

A premissa central é:

> Antes de confiar no indicador, precisamos confiar na base.

## Privacidade, LGPD e uso responsável

Este projeto foi desenvolvido para fins educacionais e de portfólio. Não envie arquivos com dados pessoais, sensíveis, confidenciais ou estratégicos.

Para testes, utilize bases:

- fictícias;
- públicas;
- anonimizadas;
- sem identificação direta ou indireta de pessoas.

A aplicação possui uma camada preventiva que verifica nomes de colunas que podem indicar dados pessoais ou sensíveis, como CPF, e-mail, telefone, endereço, matrícula, colaborador, saúde, biometria ou sindicato.

Essa verificação é apenas um alerta inicial. Ela não substitui avaliação jurídica, revisão de segurança da informação, política interna de privacidade ou validação formal de compliance.

Em um ambiente corporativo, qualquer uso com dados reais deve observar:

- a Lei Geral de Proteção de Dados Pessoais;
- as políticas internas de segurança e privacidade;
- a classificação da informação;
- a necessidade e finalidade do tratamento;
- os controles de acesso;
- a retenção e descarte dos arquivos analisados;
- a aprovação das áreas responsáveis, como Jurídico, Compliance, Segurança da Informação e Governança de Dados.

## Como adaptar para um ambiente interno da empresa

Em uma versão corporativa, o Smart Report Auditor poderia funcionar como uma camada de validação antes de relatórios serem usados em dashboards, apresentações executivas ou rotinas de atualização.

### Exemplo de fluxo interno

```text
Usuário envia relatório
↓
Sistema valida estrutura e qualidade da base
↓
Regras de governança classificam alertas
↓
Base aprovada segue para Power BI, SharePoint ou data lake
↓
Base com erro retorna para correção
↓
Auditoria gera histórico e evidência de validação
```

### Sistemas que poderiam ser integrados

A adaptação corporativa poderia integrar:

- SharePoint ou OneDrive corporativo para entrada e armazenamento controlado dos arquivos;
- Power BI para consumo dos dados validados;
- Power Automate para acionar fluxos de aprovação, alertas ou notificações;
- Microsoft Teams ou Outlook para envio de alertas aos responsáveis;
- Azure SQL, Dataverse ou Data Lake para registrar histórico de auditorias;
- Azure Active Directory / Entra ID para autenticação e controle de acesso;
- SAP, ERP ou sistemas operacionais como origem dos dados;
- ferramentas de governança, catálogo de dados ou data quality, caso existam na organização.

### Como funcionariam as regras de compliance e governança

Em uma implantação interna, as regras deveriam ser formalizadas de acordo com o tipo de relatório e a criticidade do processo.

Exemplos de regras:

- bloquear upload de arquivos com colunas sensíveis não autorizadas;
- exigir anonimização para bases com dados pessoais;
- registrar usuário, data, nome do arquivo e resultado da auditoria;
- classificar alertas por criticidade;
- impedir avanço de bases classificadas como críticas;
- permitir aprovação manual por responsável do processo;
- manter trilha de auditoria;
- aplicar controle de acesso por perfil;
- definir política de retenção e descarte dos arquivos;
- documentar as regras de qualidade aceitas por área;
- revisar periodicamente as regras com Governança de Dados, Compliance e Segurança da Informação.

### Exemplo de papéis envolvidos

- Área de negócio: define regras do processo e valida critérios de qualidade.
- BI / Dados: estrutura a lógica de validação e integração com dashboards.
- TI: garante infraestrutura, segurança, autenticação e disponibilidade.
- Compliance / Jurídico: avalia aderência regulatória e privacidade.
- Segurança da Informação: define controles de acesso, retenção e proteção dos dados.
- Dono do dado: aprova regras, exceções e uso da informação.

### Evolução possível

Em uma versão empresarial, a ferramenta poderia deixar de ser apenas um app de upload e evoluir para uma solução de governança operacional, com:

- validações automáticas por pasta monitorada;
- histórico de auditorias;
- dashboards de qualidade da base;
- alertas automáticos;
- logs por usuário;
- integração com esteiras de atualização do Power BI;
- regras específicas por departamento;
- indicadores de qualidade dos dados por área;
- camada de aprovação antes da publicação de relatórios.
