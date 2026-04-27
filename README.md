# Processo Seletivo – Intensivo Maker | IoT
## Etapa Prática – Sistemas Embarcados

Bem-vindo(a) à **etapa prática do processo seletivo para o Intensivo Maker | IoT**.

Esta atividade tem como objetivo avaliar suas competências em **Sistemas Embarcados**, com foco em **organização de projeto, lógica de firmware e simulação de hardware**, a partir da aplicação prática dos conhecimentos adquiridos nos cursos EAD da etapa anterior.

> 🎯 **Objetivo principal**  
> Avaliar sua capacidade de **planejar, estruturar e desenvolver** uma solução funcional de sistemas embarcados, seguindo boas práticas de engenharia.

---

## 🏁 Passo 0 – Antes de Tudo

Se você **nunca utilizou Git ou GitHub**, não se preocupe.  
Siga atentamente os passos abaixo — eles fazem parte do processo de aprendizagem esperado.

---

### 1️⃣ Criação de Conta no GitHub

1. Acesse: https://github.com  
2. Clique em **Sign up**  
3. Crie sua conta gratuita seguindo as instruções da plataforma  

> 📌 O GitHub será utilizado para:
> - Envio do seu projeto  
> - Versionamento do código  
> - Correção e validação automática via GitHub Actions  

---

### 2️⃣ Instalação do Git

O **Git** é a ferramenta responsável pelo controle de versões do seu código.

### Windows
Baixe e instale o **Git Bash**:  
https://git-scm.com/downloads

### Linux / macOS
Verifique se o Git já está instalado:

```bash
git --version
```
> Caso não esteja, instale pelo gerenciador de pacotes do seu sistema.

## ⚙ Passo 1 – Preparando o Ambiente

Para desenvolver o desafio, você deverá criar uma cópia deste repositório no seu GitHub.

### 1️⃣ Fork do Repositório
No canto superior direito desta página, clique em Fork

<img width="219" height="45" alt="image" src="https://github.com/user-attachments/assets/5d629626-513a-445c-ba0f-e5bb3e225187" />


Uma cópia do repositório será criada no seu perfil do GitHub

> 🔎 O Fork permite que você trabalhe de forma independente, sem alterar o repositório original do processo seletivo.

### 2️⃣ Clone do Repositório

No repositório do seu Fork, clique em **<> Code**

<img width="149" height="52" alt="image" src="https://github.com/user-attachments/assets/abbd331b-a005-4633-89c6-afd16acbe828" />

Copie a URL e execute no terminal:

```bash
git clone https://github.com/SEU_USUARIO/nome-do-repositorio.git
cd nome-do-repositorio
```

> O comando git clone cria uma cópia local do repositório para desenvolvimento.

### 3️⃣ Preparação do Ambiente de Execução

Você pode executar o projeto de duas formas. Escolha apenas uma.

#### 🔹 Opção A – Ambiente Python Local

**Requisitos:**

- Python 3.10 ou 3.11
- pip

**Instale as dependências:**

```bash
pip install -r requirements.txt
```

#### 🔹 Opção B – Dev Container (Recomendado)

Este repositório inclui um Dev Container, garantindo um ambiente padronizado.

**Requisitos:**

- VS Code
- Docker instalado
- Extensão Dev Containers

**Passos:**

1. Abra o repositório no VS Code
2. Clique em “Reopen in Container”
3. Aguarde a criação automática do ambiente

> ➡️ Todas as dependências serão instaladas automaticamente.

## 🔐 Passo 2 – Criando sua API Key do Wokwi

A simulação do projeto será executada automaticamente via GitHub Actions, utilizando o Wokwi CLI.

Para isso, você precisa gerar uma API Key.

1. Acesse: https://wokwi.com/dashboard/ci
2. Faça login (Google ou GitHub)
3. Clique em Generate API Token
4. Copie a chave gerada (exemplo: wokwi-xxxxxxxx)

>⚠️ Importante
- Nunca faça commit dessa chave
- Ela deve ser armazenada apenas como secret no GitHub

## 🔒 Passo 3 – Configurando a API Key no GitHub (Secrets)

**No repositório do seu Fork:**

1. Vá em Settings
2. Acesse Secrets and variables → Actions
3. Clique em New repository secret
4. Nome: WOKWI_API_KEY
5. Valor: sua chave gerada
6. Salve

> ✔️ As GitHub Actions do template já estão preparadas para usar essa variável automaticamente.

## 🧠 Passo 4 – Desafio Técnico

Você deverá desenvolver um projeto de sistemas embarcados simulados, utilizando Python e Wokwi.

### 📁 Estrutura mínima esperada

```text
/project
 ├── src/
 │   └── main.py        # Código principal do projeto
 ├── wokwi.toml         # Configuração da simulação
 ├── diagram.json       # Circuito no Wokwi
 └── README.md          # Explicação do seu projeto
```

> Você pode expandir essa estrutura se desejar, desde que mantenha os arquivos essenciais.

### 🛠 Como Desenvolver seu Projeto

O desenvolvimento acontece principalmente nos arquivos abaixo:

#### 1️⃣ src/main.py

- Código Python executado na simulação
- Implementa a lógica do sistema embarcado
- Exemplos: controle de LEDs, leitura de sensores, estados, temporizações, etc.

#### 2️⃣ diagram.json

- Define o hardware virtual do projeto
- Componentes como:
  - LEDs
  - Botões
  - Sensores
  - Placa microcontroladora

#### 3️⃣ wokwi.toml

- Configura a simulação:
  - Tipo de placa
  - Framework
  - Dependências adicionais

#### 4️⃣ Commit e Push

Após suas alterações:

```bash
git add .
git commit -m "Descrição clara do que foi feito"
git push
```
### ⚙ Execução Automática (GitHub Actions)

A cada push, o GitHub Actions irá automaticamente:

- Executar o pipeline de build
- Rodar a simulação via Wokwi CLI
- Validar que o projeto executa sem erros

### 📌 Caso algo falhe:

- Vá até a aba Actions
- Analise os logs da execução
- Corrija e envie novamente

## 📊 Critérios de Avaliação

Esta etapa será avaliada considerando:

- Funcionamento correto da simulação
- Código organizado e legível
- Estrutura de arquivos correta
- Uso adequado do Wokwi
- Commits claros e bem descritos
- Projeto executando sem falhas nas Actions

---

## 📎 Submissão Final

Após concluir o desenvolvimento:

1. Verifique se o projeto **executa sem erros** nas GitHub Actions  
2. Confirme que todos os arquivos obrigatórios estão presentes  
3. Copie o link do **seu repositório no GitHub**

📤 Envie o link conforme as orientações do processo seletivo na plataforma **Moodle**.

---

## 📝 Relatório do Candidato

import os

## Relatório do Projeto: ArgosGuard – Sensor Inteligente de Fadiga

Este repositório contém a solução para o desafio técnico do Intensivo Maker | IoT. O projeto **ArgosGuard** é um sistema embarcado focado na segurança rodoviária, utilizando IoT para monitorizar a atenção do condutor.

---

### 👤 Identificação do Candidato
- **Nome completo:** Francisco Irlan de Oliveira Barros
- **GitHub:** https://github.com/IrlanBarros

---

## 1️⃣ Visão Geral da Solução

O **ArgosGuard** é um sensor de segurança vestível (*wearable*) desenhado para prevenir acidentes causados por fadiga ou micro-sono. O sistema utiliza um acelerómetro para identificar inclinações excessivas da cabeça do condutor que indiquem sonolência.

### 🚨 Problemática e Importância
A fadiga ao volante é uma das causas mais comuns de acidentes graves em estradas. O condutor muitas vezes não percebe o início do sono. O ArgosGuard atua como uma camada de proteção ativa:
1.  **Detecção em Tempo Real:** Identifica a queda da cabeça instantaneamente.
2.  **Alerta Imediato:** Aciona um buzzer e LED para despertar o condutor.
3.  **Monitorização Remota:** Notifica terceiros via Telegram, permitindo uma intervenção externa se necessário.

---

## 2️⃣ Arquitetura do Sistema Embarcado

A arquitetura foi pensada para ser robusta, eficiente e interativa, utilizando **MicroPython**:

-   **Processamento de Sinal:** Implementação de um Filtro Passa-Baixa (EMA) para suavizar as leituras do sensor e evitar alarmes falsos causados por vibrações do veículo.
-   **Lógica de Negócio:** Monitorização de tempo de fadiga (3 segundos) e lógica de normalização após resets.
-   **Gestão de Energia:** Redução da frequência do CPU para 80MHz e uso de amostragem adaptativa (*Duty Cycling*) para prolongar a vida útil da bateria.
-   **Comunicação IoT:** Integração bidirecional com a API do Telegram para alertas e comandos remotos.

---

## 3️⃣ Componentes Utilizados na Simulação

Os componentes foram selecionados para criar um protótipo funcional no **Wokwi**:

-   **ESP32 DevKit V4:** Microcontrolador principal com Wi-Fi nativo.
-   **MPU6050:** Acelerómetro e Giroscópio para medir o ângulo de inclinação.
-   **Buzzer Piezoelétrico:** Alerta sonoro de alta intensidade (Pino 18).
-   **LED Vermelho:** Sinalização visual de alerta (Pino 5).
-   **Botão de Pressão:** Utilizado para reset físico e recalibração (Pino 4).
-   **Potenciómetro:** Simula a descarga de uma bateria para testes de telemetria (Pino 34).

---

## 4️⃣ Decisões Técnicas Relevantes

-   **Calibração Dinâmica:** O sistema não assume um "zero" fixo; ele calibra-se de acordo com a posição inicial do motorista ao ligar ou via comando.
-   **Amostragem Adaptativa:** Em estado normal, o sistema lê o sensor a cada 800ms. Se detectar inclinação, a taxa sobe para 50ms para garantir precisão no disparo do alarme.
-   **Estabilidade de Memória:** Uso extensivo de `gc.collect()` e codificação manual de bytes em UTF-8 para evitar *crashes* de memória ao enviar emojis via Telegram.
-   **Segurança de Dados:** O sistema valida o `CHAT_ID` do remetente para garantir que apenas o utilizador autorizado possa enviar comandos ao sensor.

---

## 5️⃣ Resultados Obtidos e Funcionalidades

O sistema encontra-se 100% funcional, apresentando os seguintes recursos:

-   **Detecção de Fadiga:** Alarme sonoro/visual e mensagem no Telegram após 3 segundos de inclinação.
-   **Monitorização de Bateria:** Alerta automático no Telegram quando a bateria está fraca, com *cooldown* de 5 minutos para evitar spam.
-   **Interatividade via Telegram:**
    -   `/status`: Relatório de bateria, inclinação e estado de alerta.
    -   `/recalibrar`: Ajusta o "zero" do sensor remotamente.
    -   `/reset`: Silencia o alarme e reinicia o sistema remotamente.
    -   `/limiar [valor]`: Ajusta a sensibilidade do sensor sem precisar de reprogramar a placa.

---

## 🚀 Instruções para o Avaliador

Para testar o projeto corretamente, siga os passos abaixo:

### 1. Configuração do Telegram
Para receber as notificações no seu telemóvel, é necessário configurar as credenciais no topo do ficheiro `src/main.py`:

1.  **BOT_TOKEN:**
    -   No Telegram, procure pelo `@BotFather`.
    -   Crie um novo bot com `/newbot` e copie o Token gerado.
2.  **CHAT_ID:**
    -   Procure pelo bot `@ArgosGuard`.
    -   Envie qualquer mensagem e ele responderá com o seu **Id** numérico.
3.  **Ativação:** Procure pelo bot que criou e clique em **Começar/Start**.

### 2. Como Rodar
O projeto utiliza um sistema de ficheiros simulado. No seu ambiente local ou Dev Container, execute o seguinte comando antes de iniciar a simulação no Wokwi:

```bash
python src/build_fs.py
```

## 6️⃣ Comentários Adicionais

-   **Desafios Técnicos:** A gestão de memória RAM ao lidar com requisições HTTPS e o tratamento de instabilidades no `light_sleep` do firmware v1.24.1 foram os principais obstáculos, resolvidos com otimização de código e amostragem adaptativa.
-   **Aprendizados:** Como professor de robótica, este projeto reforçou a importância do **Processamento Digital de Sinais (DSP)** na base de qualquer sistema de segurança confiável.
-   **Melhorias Futuras:** Integração com módulos GSM para conectividade rural e implementação de Deep Sleep total para autonomia de longa duração.

---

> Projeto submetido para avaliação técnica - Intensivo Maker | IoT.
"""

> ✅ Este relatório faz parte da avaliação técnica.  
> Clareza, objetividade e organização são tão importantes quanto o funcionamento do código.

---

## 🆘 Suporte

Em caso de dúvidas:

- Consulte o material dos cursos EAD
- Leia atentamente este README
- Analise os logs das GitHub Actions
- Utilize os canais oficiais para contato com os instrutores

Boa sorte no processo seletivo.
Mostre sua capacidade de pensar como um engenheiro de sistemas embarcados.
****
