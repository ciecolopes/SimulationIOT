# 🚀 Pipeline de Stream de Dados em Tempo Real do aplicativo Pede Pronto

## Bem-vindo!

Bem-vindo ao projeto de Pipeline de Stream de Dados de Ponta a Ponta do aplicativo Pede Pronto, onde o cliente realiza o pedido no restaurante, o restaurante atualiza o status do pedido e o cliente no final faz a avaliação do pedido!

## Sobre o Projeto

O projeto serve como um pipeline abrangente de transmissão de dados em tempo real

## 🛠️ Componentes Principais

- 📊 **Dispositivos IoT**: Criado um simulador de envio de sensores e dispositivos implatados no aplicativo do cliente e dos restaurantes.
- 🛠️ **Apache Kafka**: Um sistema de mensagens escalável e tolerante a falhas para ingestão e processamento de fluxos de dados.
- 🛠️ **Apache Spark**: Um poderoso motor para processamento e análise de dados em tempo real, garantindo geração rápida de insights.
- 🛠️ **Docker**: Tecnologia de containerização para empacotar e implantar nossos componentes de pipeline com facilidade.
- 🛠️ **AWS Cloud**: Infraestrutura em nuvem para armazenamento e processamento de dados escaláveis e confiáveis.
- 🛠️ **AWS Glue**: Serviço de integração de dados sem servidor para automatizar operações ETL e tarefas de transformação de dados.
- 🛠️ **AWS Athena**: Serviço de consulta interativa para analisar dados armazenados no Amazon S3 usando consultas SQL padrão.
- 🛠️ **AWS Redshift**: Solução de data warehouse totalmente gerenciada, otimizada para análises de alto desempenho e consultas complexas.
- 🛠️ **Power BI, Looker Studio, QuickSight**: Ferramenta de inteligência de negócios para visualizar e explorar dados com dashboards interativos e insights impulsionados por ML.

## 🌟 Exploração Detalhada

1. **Ingestão de Dados**: Ingestão em tempo real de dados de dispositivos IoT (simulador em python) no Apache Kafka para processamento.
2. **Processamento de Dados**: Utilização do Apache Spark para processamento e análise em tempo real dos fluxos de dados.
3. **Armazenamento de Dados**: Armazenamento seguro dos dados processados no AWS S3 e Redshift para análise e visualização posterior.
4. **Visualização de Dados**: Visualização de insights e tendências usando o Power Bi, Looker Studio ou até mesmo o AWS QuickSight

## 📊 Análises com Power BI

O Power BI é uma suíte de ferramentas de análise de negócios desenvolvida pela Microsoft, projetada para transformar dados brutos em insights visuais e interativos. Ele permite que os usuários conectem-se a uma ampla variedade de fontes de dados, criem relatórios detalhados e dashboards interativos, e compartilhem esses insights com outras partes interessadas dentro da organização.

## 📊 Análises com Looker Studio

O Looker Studio, anteriormente conhecido como Google Data Studio, é uma plataforma de inteligência de negócios e visualização de dados desenvolvida pelo Google. Ele permite que os usuários criem relatórios e dashboards interativos a partir de diversas fontes de dados, facilitando a análise e a comunicação de insights de maneira visual e intuitiva.

## 📊 Análises com QuickSight

Conjunto de ferramentas de inteligência de negócios de próxima geração que oferece dashboards interativos, análises preditivas e geração de insights impulsionados por ML, permitindo que as partes interessadas visualizem e explorem dados com clareza e agilidade sem precedentes.

## 🚀 Arquitetura/Fluxos de Trabalho

![313504181-321a5329-edc2-4715-b8d9-77e03a70341e](https://github.com/ciecolopes/SimulationIOT/blob/main/arquitetura.jpg?raw=true)

## 🏙️ Componentes do Sistema

- **docker-compose.yml**: Configura o ambiente hospedando o broker Kafka, Zookeeper e nós Spark.
- **main.py**: Simulador com a geração de dados, criação de tópicos Kafka (producer.py) e processamento inicial de dados.
- **producer.py**: Function para criação de tópicos Kafka.
- **spark-pedepronto.py**: Consome dados dos tópicos Kafka e os transmite para os buckets designados do Amazon S3.
