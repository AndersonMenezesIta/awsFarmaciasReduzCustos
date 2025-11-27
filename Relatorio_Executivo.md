**Relatório de implementação de serviços AWS**

**Data:** 27/11/2025  
**Empresa:** Abstergo Industries (Farmácia Fictícia)  
**Responsável:** Sergio Santos – Especialista em Cloud & Data Science  
Versão: 1.1

---

**Visão executiva**

- Contexto financeiro: A Abstergo opera 12 farmácias e 1 CD em BH, com TI on-premises custando R$ 85.000/ano (servidores, energia, manutenção, licenças).
- Objetivo: Migrar cargas críticas para AWS (EC2, RDS, S3) para reduzir custos, aumentar segurança e escalabilidade.
- Resultado esperado (12 meses): Economia líquida estimada de R$ 119.000/ano, redução de 40% no OPEX de TI, SLA >= 99,9%, preparo para expansão (+5 lojas em 2026).
- Governança e controle: Orçamentos mensais, tags financeiras, alertas de custo e relatórios para diretoria.

---

**Descrição do projeto**

A migração foi planejada em três etapas com entregas mensuráveis e foco em impacto financeiro imediato.

**Etapa 1:** Amazon EC2 (Elastic Compute Cloud)

- Foco: Substituir 4 servidores físicos por instâncias EC2 para ERP/PDV/estoque.
- Caso de uso:  
  - Produção: 2 instâncias t3.medium (vCPU 2, RAM 4 GB) com Auto Scaling.  
  - Homologação: 1 instância t3.micro, desligada fora do horário (economia).  
- Benefícios:  
  - CAPEX evitado: R$ 48.000 (4 servidores x R$ 12.000/ano) e manutenção.  
  - Pagamento por uso: Desligamento noturno gera economia ~35% em horas.  
  - Elasticidade: Escala em campanhas de vacinação e datas sazonais.

**Etapa 2:** Amazon RDS (Relational Database Service)

- Foco: Banco gerenciado para vendas, clientes, estoque e auditoria.
- Caso de uso:  
  - PostgreSQL RDS: db.t3.medium, Multi-AZ em produção; backups automáticos 7 dias.  
- Benefícios:  
  - Licenciamento substituído: SQL local R$ 25.000/ano.  
  - Operação simplificada: Patches, backups e failover gerenciados.  
  - LGPD: Criptografia em repouso e em trânsito; acesso por função.

**Etapa 3:** Amazon S3 (Simple Storage Service)

- Foco: Repositório de documentos e relatórios com ciclo de vida custando menos.
- Caso de uso:  
  - Buckets: s3://abstergo-docs-prod (receitas, NF), s3://abstergo-logs (auditoria).  
  - Classes de armazenamento: Standard, Standard-IA, Glacier para arquivamento.  
- Benefícios:  
  - Aluguel evitado: 2 salas (R$ 3.500/mês) substituídas por digitalização.  
  - Durabilidade 11x9: Reduz risco de perda e custo de recuperação.  
  - Auditoria ágil: Acesso por perfis, sem duplicação de documentos.

---

**Arquitetura de referência**

**Rede e segurança**

- VPC Abstergo: 10.0.0.0/16 com sub-redes privadas (EC2/RDS) e públicas (ALB/NAT).
- Security Groups:  
  - App: Tráfego somente do ALB e IPs internos.  
  - DB: Apenas portas do app e bastion com MFA.  
- IAM: Perfis mínimos necessários; contas críticas com MFA; chaves rotacionadas.

**Disponibilidade e continuidade**

- RDS Multi-AZ: Failover automático.  
- Backups:  
  - EC2: AMIs semanais e snapshots diários.  
  - RDS: Retenção 7 dias, testes de restore mensais.  
  - S3: Versionamento e bloqueio de exclusão (legal hold em documentos críticos).
- Monitoramento: CloudWatch + alarmes (CPU, memória, I/O, custos), métricas por centro de custo.

---

**Plano financeiro**

**Custos AWS e economia**

| Item                         | Situação atual (anual) | AWS (anual) | Economia líquida |
|-----------------------------|-------------------------|-------------|------------------|
| Servidores locais (4x)      | R$ 48.000               | —           | R$ 48.000        |
| Energia/refrigeração        | R$ 30.000               | —           | R$ 30.000        |
| Licença SQL                 | R$ 25.000               | —           | R$ 25.000        |
| Backups físicos             | R$ 8.000                | —           | R$ 8.000         |
| Aluguel salas de arquivo    | R$ 42.000               | —           | R$ 42.000        |
| EC2                         | —                       | R$ 21.600   | -R$ 21.600       |
| RDS                         | —                       | R$ 28.800   | -R$ 28.800       |
| S3 (5 TB + requisições)     | —                       | R$ 7.200    | -R$ 7.200        |
| Internet/operacional extra  | —                       | R$ 0        | R$ 0             |
| Totais                  | R$ 153.000          | R$ 57.600 | R$ 95.400    |

- **Observações financeiras:**  
  - Margem de segurança: +10% para variações de uso → custo AWS anual estimado R$ 63.360.  
  - Economia conservadora: R$ 153.000 - R$ 63.360 = R$ 89.640/ano.  
  - ROI (12 meses): > 140% considerando custos de migração e treinamento (~R$ 37.000).

**Governança de custos**

- **Budgets mensais:** Limite R$ 5.500 com alertas em 70%/90%/100%.  
- **Tags financeiras:** cost_center, environment, owner, project.  
- **Relatórios:** Dashboards mensais por serviço e unidade (filial).

---

**Requisitos para operação**

- **Hardware local:**  
  - **Estações:** PCs padrão para PDV e administração; sem servidores.  
  - Conectividade: Link principal + 4G de contingência no CD e matriz.
- **Software e acessos:**  
  - **Console AWS:** Acesso via navegador atualizado.  
  - **Cliente SQL:** Para RDS (pgAdmin).  
  - **VPN/Bastion:** Acesso administrativo restrito.
- **Segurança operacional:**  
  - **MFA obrigatório:** Gestores e TI.  
  - **Senhas robustas:** Políticas de rotação trimestral.  
  - **Criptografia:** Ativa em S3 e RDS.

---

**Capacitação e treinamento**

- **Público:** Finanças, Operações, TI.
- **Trilha e carga horária:**  
  - **AWS Cloud Practitioner:** 12h (conceitos, custos e segurança).  
  - **Workshop EC2/RDS/S3:** 10h (mão na massa, boas práticas).  
  - **Governança de custos:** 4h (tags, budgets, relatórios).  
- **Entregáveis do treinamento:**  
  - **Playbooks operacionais:** Rotinas de backup/restore, desligamento de instâncias, leitura de relatórios.  
  - **Guia LGPD:** Perfis de acesso, auditoria, retenção de dados.

---

**Cronograma de implementação**

**1. Semana 1 – Planejamento**
   - Levantamento: Sistemas, volumes, SLAs, sazonalidade, requisitos LGPD.
   - Arquitetura: VPC, sub-redes, IAM, SGs, classes de S3, RDS Multi-AZ.
**2. Semanas 2–3 – Pilotos**
   - EC2: ERP/PDV em t3.medium; testes de carga e desligamento programado.  
   - RDS: Migração base teste; performance, backups e criptografia.  
   - S3: Buckets, versionamento, ciclo de vida; integração com digitalização.
**3. Semanas 4–5 – Produção**
   - Go-live: EC2/RDS/S3 com ALB, NAT, monitoramento e orçamentos.  
   - Treinamento: Playbooks entregues; finanças com dashboard de custos.
**4. Semana 6 – Revisão e otimização**
   - Rightsizing: Ajustes de instância/armazenamento.  
   - Relatório financeiro: Primeira consolidação mensal e plano de melhorias.
**5. Semana 8 – Governança ampliada**
   - Saving Plans/Reserved: Avaliar para cargas previsíveis.  
   - Automação: Escalonamento noturno e políticas de ciclo de vida refinadas.

---

**Riscos e mitigação**

- Custo acima do previsto:  
  - Mitigação: Budgets, desligamento automático, rightsizing, tags obrigatórias.
- Segurança/LGPD:  
  - Mitigação: IAM com menor privilégio, MFA, criptografia, trilhas de auditoria, revisão de acessos mensal.
- Disponibilidade:  
  - Mitigação: RDS Multi-AZ, snapshots, testes de recuperação trimestrais, ALB para redundância.
- Adoção interna:  
  - Mitigação: Treinamento prático, comunicação de benefícios, suporte inicial de TI.
- Dependência de internet:  
  - Mitigação: Links redundantes e plano de contingência (modo offline limitado para PDV).

---

**Conclusão:**

A migração para AWS com EC2, RDS e S3 oferece à Abstergo uma redução direta e sustentável de custos, maior segurança, disponibilidade e agilidade operacional. Com governança de custos e treinamento, a empresa obtém previsibilidade orçamentária e base tecnológica para crescer com controle e compliance. Na fase seguinte, recomenda-se avaliar AWS Lambda (automatizações) e Amazon QuickSight (BI financeiro) para ampliar o valor entregue ao negócio.

---

**Anexos**

- Planilha de custos comparativos: On-premises vs AWS (CSV/XLSX).  
- Mapa de tags financeiras: cost_center, environment, owner, project.  
- Políticas S3: Versionamento, ciclo de vida (Standard → IA → Glacier).  
- Checklist de segurança: IAM, MFA, encryption, backups, auditoria.  
- Playbooks operacionais: Backup/restore, desligamento, leitura de custos.  

---

**Assinatura do responsável pelo projeto:**

Sergio Santos – Especialista em Cloud & Data Science  
Contato: sergio@abstergo.example.br (fictício)

---
