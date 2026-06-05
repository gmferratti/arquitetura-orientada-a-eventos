# Introducao a Arquitetura Orientada Eventos com Faststream

Concorrente do Fast Stream Selery

Sistema de Mensageria
Event-Driven architecture

"Architecture is about the important stuff. Whatver that is."
"entendimento compartilhado do design do sistema pelos desenvolvedores experientes"

Arquitetura hexagonal: ports & adapters
Arquitetura monolitica
Arquitetura de microsservicos
Arquitetura Model View Controller
Arquitetura orientada a Eventos

User --> App --> Message Broker --> Mensagem X, Mensagem Y
                                --> Mensagem Z

Arquitetura reativa. So funciona quando alguem chama.
Nao espera requisicioes. Ex. Recuperacao de senha

Assincronismo. Usuario enia evento e nao espera resposta, processamento acontece quando der (ex. telefone vs. ZAP)

Desacoplamento, produtores nao conhecem consumidores, comunicacao intermediada por message broker

Advanced Message Queuing Protocol (AMQP) com Rabbit MQ (Open source)

Producer
Exchanges (direct, faz match exato entre routing e exchanging; fanout, envia a mensagem para todas as filas da exchange,
topic, match particial entre routing e binding; headers, match pelo metadados da mensagem - direct com esteroides; default - forca nome da queue = binding key = routing key)
Queues
Consumers (ack, avisa que a mensagem foi recebida de fato e remove da fila, nack, mensagem falhou)

DLQ - Dead Letter Queue

## Fast Stream

Biblioteca par lidar com sistema de mensageria em Python



Routing key e binding key

Locust - Biblioteca Python para desenvolver teste de carga (muito facil, boa interface grafica)
https://locust.io/

