# Relatórios de teste — Smart Report Auditor

Este pacote contém bases fictícias para testar o app Smart Report Auditor.

## Arquivos

1. 01_vendas_ecommerce.csv
   - Testa vendas, canais, categorias e valores.
   - Problemas intencionais: categoria vazia, valor negativo, data ausente, data em formato diferente, possível outlier e variação textual.

2. 02_chamados_suporte.csv
   - Testa chamados de atendimento/suporte.
   - Problemas intencionais: duplicidade, tempo de resposta zerado, campo vazio, status com variação textual e possíveis outliers.

3. 03_campanhas_marketing.csv
   - Testa campanhas de marketing.
   - Problemas intencionais: investimento negativo, leads zerados, campanha vazia, data ausente e variação textual.

4. 04_estoque_varejo.csv
   - Testa movimentações de estoque.
   - Problemas intencionais: quantidades negativas, duplicidade, categoria vazia, quantidade zerada e data ausente.

5. 05_assinaturas_saas.csv
   - Testa receita recorrente/assinaturas.
   - Problemas intencionais: receita negativa, plano vazio, data ausente e variação textual.

6. 06_rh_treinamentos_lgpd_teste.csv
   - Testa a camada de alerta de LGPD.
   - Contém colunas como nome_colaborador e email propositalmente para validar se o app sinaliza possível dado pessoal.
   - Os dados são fictícios.

## Como usar

1. Abra o app Smart Report Auditor.
2. Marque a confirmação de privacidade/LGPD.
3. Faça upload de um dos arquivos CSV.
4. Observe:
   - score de qualidade;
   - alertas de auditoria;
   - diagnóstico executivo;
   - gráficos automáticos;
   - alerta de possível dado pessoal, quando aplicável.

## Observação

Todas as bases são fictícias e foram criadas apenas para teste técnico e demonstração de portfólio.
