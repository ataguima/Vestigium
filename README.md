# Vestigium - README

Vestigium é uma workstation visual de OSINT people-first, focada em investigar pessoas reais a partir de fragmentos limitados de informação (username, e-mail, nome, IDs), organizando vestígios digitais em um grafo probabilístico, com decisão humana no loop.

Este projeto é vibecoded, criado com foco em fluidez criativa, iteração rápida e alinhamento com a visão investigativa do produto.

O Vestigium não tenta “adivinhar a verdade”.
Ele organiza hipóteses, explicita incertezas e ajuda o investigador a pensar melhor.

## Rodando no Windows (rápido)

Se você já tem Python e Node instalados, o jeito mais fácil é usar o script abaixo:

```bat
scripts\\run_windows.bat
```

Isso abre dois terminais: um para o backend (FastAPI) e outro para o frontend (Vite).

### Passo a passo (manual)

**1) Backend**

```bash
python -m uvicorn services.api.app:app --reload --host 0.0.0.0 --port 8000
```

Teste rápido:

```bash
curl http://localhost:8000/health
```

**2) Frontend**

```bash
cd apps/desktop
npm install
npm run dev
```

Depois, abra o endereço que aparecer no terminal do Vite (geralmente `http://localhost:5173`).

## 1. Problema que o Vestigium resolve

Ferramentas OSINT tradicionais falham em três pontos críticos:

- Tratam pessoas como infraestrutura
  (domínios, IPs, serviços), não como identidades humanas ambíguas.
- Assumem determinismo
  (“achou = é a mesma pessoa”), ignorando que OSINT é incerto por natureza.
- Geram ruído cognitivo
  listas enormes de links, sem hierarquia, sem explicação, sem orientação.

O Vestigium nasce para resolver exatamente isso.

## 2. Princípios fundamentais

### 2.1 People-first

O objeto central do Vestigium não é um site, nem um domínio, nem um serviço.
É uma Pessoa.

Tudo no sistema existe para responder perguntas como:

- “Esses dois perfis pertencem à mesma pessoa?”
- “Quais evidências sustentam essa hipótese?”
- “O que ainda falta investigar?”

### 2.2 Evidência antes de conclusão

Nada entra no grafo sem evidência.
Nada sai sem decisão.

Cada ligação no grafo carrega:

- fonte
- contexto
- grau de confiança
- justificativa

### 2.3 Incerteza explícita (não escondida)

O Vestigium não força respostas binárias.

Toda correlação aceita três estados:

- Sim (confirmado)
- Não (descartado)
- Não sei (mantido como hipótese fraca)

A incerteza é uma feature, não um erro.

### 2.4 Humano no loop

O Vestigium não substitui o investigador.
Ele organiza o raciocínio do investigador.

O sistema:

- sugere
- prioriza
- alerta

Mas quem decide é o humano.

## 3. O que é o Vestigium (em termos práticos)

### 3.1 Uma workstation visual (estilo Maltego)

- Interface gráfica baseada em grafo
- Nós representam entidades
- Arestas representam relações
- Zoom, pan, drag, foco, histórico

Mas com uma diferença fundamental:
👉 o Vestigium pensa em pessoas, não em infraestrutura.

### 3.2 Um motor de investigação guiada

Dado um input simples, como:

```
@username
```

O Vestigium:

- Coleta vestígios públicos (via plugins)
- Organiza os achados no grafo
- Levanta hipóteses
- Pergunta ao usuário:
  “Isso parece ser a mesma pessoa?”
- Ajusta o grafo conforme as decisões
- Sugere próximos passos lógicos

### 3.3 Um organizador de casos OSINT

Cada investigação é um caso:

- entradas
- decisões
- hipóteses descartadas
- hipóteses confirmadas
- histórico completo

Nada se perde. Nada é implícito.

## 4. Entidades centrais do Vestigium

Essas entidades não são opcionais. Elas definem o DNA do sistema.

### 4.1 Person

Representa uma pessoa hipotética ou confirmada.

- Pode começar “vaga”
- Vai se fortalecendo com evidências
- Pode se fragmentar (caso hipóteses se contradigam)

### 4.2 Identifier

Fragmentos identificadores:

- username
- e-mail
- telefone
- nome
- handle

Um Identifier não prova identidade, apenas sugere.

### 4.3 Profile

Perfis públicos:

- redes sociais
- plataformas
- fóruns
- serviços

Sempre ligados a um Identifier ou Person, nunca soltos.

### 4.4 Evidence

A menor unidade de verdade do sistema.

Uma evidência contém:

- origem
- contexto
- dado bruto
- confiabilidade

### 4.5 Hypothesis

Uma suposição explícita, por exemplo:

“O perfil X e o perfil Y pertencem à mesma pessoa”

Hipóteses:

- podem ser aceitas
- rejeitadas
- mantidas em estado fraco

### 4.6 Decision

Registro humano:

- Sim
- Não
- Não sei

Decisões alteram o grafo, mas nunca apagam o histórico.

## 5. Arquitetura do sistema

### 5.1 Core (agnóstico)

- Modelos de dados
- Engine de decisão
- Scoring
- Plugins

Não depende de UI nem de país.

### 5.2 API local (FastAPI)

- Interface entre UI e Core
- Executa plugins
- Normaliza resultados
- Expõe decisões

A UI nunca coleta dados diretamente.

### 5.3 UI Desktop

- Electron + React
- React Flow para o grafo
- Painel lateral de evidências
- Histórico navegável

Pensada para investigações longas.

## 6. Sistema de plugins

O Vestigium não é um monolito.

### 6.1 Plugins de coleta

Exemplos:

- Social Analyzer
- Sherlock
- Ferramentas customizadas

Cada plugin:

- declara o que coleta
- declara limites
- declara tipo de evidência

### 6.2 Plugins contextuais (ex: Brasil)

O Vestigium entende que OSINT é local.

Exemplo:

- Um nome “João da Silva” ativa heurísticas brasileiras
- Sugestões mudam conforme o contexto cultural
- Fontes locais só aparecem quando fazem sentido

O core é global.
O contexto é modular.

## 7. O que o Vestigium não é

- ❌ Não é scraper agressivo
- ❌ Não quebra login
- ❌ Não acessa dados privados
- ❌ Não promete “descobrir tudo”
- ❌ Não toma decisões finais sozinho

Isso é proposital. Isso é força, não limitação.

## 8. Público-alvo

- Investigadores OSINT
- Estudantes de segurança
- Jornalistas
- Pesquisadores
- Pessoas que precisam pensar, não só coletar

## 9. Filosofia central (em uma frase)

Vestigium não busca respostas rápidas.
Ele constrói entendimento sólido.
