# Clínica Médica – Simulador Estocástico de Fluxo Clínico

**Contexto:** Projeto de Simulação Computacional & Engenharia de Software


---

## 1. Resumo do Projeto

Este projeto consiste no desenvolvimento de um **Sistema de Apoio à Decisão (DSS)** destinado à modelação e simulação de eventos discretos num ambiente hospitalar. O software permite analisar a eficiência operacional de equipas médicas sob diferentes cargas de trabalho e distribuições probabilísticas, fornecendo métricas quantitativas sobre filas de espera, tempos de atendimento e taxas de ocupação.

O sistema integra um motor de cálculo estocástico (*Backend*) com uma interface gráfica de utilizador (*Frontend*), fundamentado na lógica de priorização da Triagem de Manchester.

---

## 2. Arquitetura do Sistema

O projeto foi estruturado seguindo o princípio da **Separação de Responsabilidades** (*Separation of Concerns*), adotando uma arquitetura modular próxima do padrão **MVC (Model-View-Controller)** para garantir a escalabilidade e manutenção do código.

### Controlador (Controller)
* **Ficheiro:** `Main.py`
* **Função:** Atua como orquestrador central. É responsável pela inicialização do *runtime*, gestão do ciclo de vida da aplicação, validação de inputs e coordenação entre a interface e o motor de simulação.

### Modelo e Lógica (Model)
* **Ficheiro:** `Base.py`
* **Função:** Núcleo computacional do simulador. Implementa:
    * **Algoritmos Estocásticos:** Geração de chegadas aleatórias baseadas em distribuições estatísticas (Exponencial, Normal, Uniforme).
    * **Gestão de Filas:** Implementação de *Priority Queues* baseadas na gravidade clínica.
    * **Alocação de Recursos:** Lógica de atribuição de médicos livres a pacientes.

### Apresentação (View)
* **Ficheiros:** `Interface.py` e `Gráficos.py`
* **Função:**
    * `Interface.py`: Implementação da GUI utilizando `FreeSimpleGUI`, focada na usabilidade e feedback visual.
    * `Gráficos.py`: Motor de renderização analítica. Utiliza `Matplotlib` para transformar vetores de dados em visualizações estatísticas (histogramas, séries temporais).

### Segurança e Persistência
* **Ficheiro:** `Login.py`
* **Função:** Gestão de controlo de acesso, encriptação visual de credenciais e persistência de dados de utilizador em formato JSON (`utilizadores.json`).

---

## 3. Metodologia de Simulação

O sistema permite a parametrização de variáveis exógenas e de decisão para a realização de análises de sensibilidade (*What-If Analysis*):

### Variáveis de Entrada
1.  **Dimensão da Equipa ($k$):** Número de servidores (médicos) disponíveis no sistema ($M/M/k$).
2.  **Taxa de Chegada ($\lambda$):** Fluxo de pacientes por hora.
3.  **Distribuição Probabilística:**
    * *Exponencial:* Para simular chegadas independentes (Padrão de Poisson).
    * *Normal:* Para simular picos de afluência em torno de uma média.
    * *Uniforme:* Para cenários de controlo linear.

### Indicadores de Performance (KPIs)
O sistema gera relatórios em tempo real focados em:
* **Latência:** Tempo médio de espera segregado por prioridade (Manchester).
* **Throughput:** Volume total de pacientes processados.
* **Eficiência:** Taxa de ocupação dos recursos ($\rho$), permitindo identificar subutilização ou saturação.

---

## 4. Requisitos Técnicos

Para a execução do ambiente de simulação, são necessárias as seguintes dependências:

* **Python 3.8+**
* **Bibliotecas:**
    * `FreeSimpleGUI` (GUI Abstraction)
    * `Matplotlib` (Scientific Plotting)

### Instalação

Execute o seguinte comando no terminal para instalar as dependências necessárias:

```bash

pip install FreeSimpleGUI matplotlib
