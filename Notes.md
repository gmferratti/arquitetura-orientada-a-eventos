# Introdução à Arquitetura Orientada a Eventos com FastStream

## O que é Arquitetura?

Duas definições clássicas que valem fixar:

> *"Architecture is about the important stuff. Whatever that is."* — Ralph Johnson

> Arquitetura é o entendimento compartilhado do design do sistema pelos desenvolvedores experientes.

Ou seja: arquitetura não é sobre diagramas — é sobre as decisões que são difíceis ou caras de mudar depois.

---

## Estilos Arquiteturais

| Estilo | Característica central |
|---|---|
| **Monolítica** | Tudo em um único processo/deploy |
| **MVC** | Separa dados (Model), lógica de apresentação (View) e controle (Controller) |
| **Hexagonal** (Ports & Adapters) | Isola o núcleo da aplicação de tecnologias externas via portas e adaptadores |
| **Microsserviços** | Serviços independentes, deploy separado, comunicação via rede |
| **Orientada a Eventos** | Componentes comunicam-se publicando e consumindo eventos assíncronos |

---

## Arquitetura Orientada a Eventos (EDA)

**Motivação principal:** desacoplamento e assincronismo.

- O **produtor** publica um evento e *não espera resposta* — segue em frente.
- O **consumidor** processa quando puder — pode ser milissegundos ou horas depois.
- Eles nunca se conhecem diretamente; tudo passa pelo **message broker**.

**Analogia:** SMS vs ligação telefônica. No SMS (assíncrono) você envia e faz outra coisa. Na ligação (síncrono/reativo) você fica parado esperando.

**Exemplo prático:** recuperação de senha. Quando o usuário clica em "esqueci minha senha", a aplicação publica um evento `PasswordResetRequested`. O serviço de e-mail, que assina esse evento, processa e envia o e-mail — sem que a API principal precise saber quem vai fazer o envio.

---

## AMQP e RabbitMQ

**AMQP** (Advanced Message Queuing Protocol) é o protocolo padrão de mensageria. O **RabbitMQ** é a implementação open-source mais popular.

### Componentes principais

**Producer** → publica mensagens com uma *routing key*.

**Exchange** → recebe a mensagem e decide para qual(is) fila(s) enviá-la. Tipos:

| Tipo | Comportamento |
|---|---|
| `direct` | Match exato entre routing key e binding key |
| `fanout` | Envia para *todas* as filas ligadas à exchange |
| `topic` | Match parcial com wildcards (`*` = uma palavra, `#` = zero ou mais) |
| `headers` | Usa metadados da mensagem em vez da routing key — como um `direct` com esteroides |
| `default` | Exchange interna; routing key = nome da fila diretamente |

**Queue** → fila onde as mensagens ficam aguardando consumo.

**Consumer** → consome mensagens. Deve responder com:
- `ack` — "recebi e processei com sucesso", mensagem é removida da fila.
- `nack` — "falhou", mensagem pode ser recolocada na fila ou redirecionada.

**Dead Letter Queue (DLQ)** → fila especial que recebe mensagens que falharam repetidamente (excederam retries, expiraram o TTL, ou receberam `nack` sem requeue). Permite inspecionar e reprocessar falhas sem perder dados.

---

## FastStream

Biblioteca Python para criar produtores e consumidores de forma declarativa. É concorrente do Celery para casos de uso de mensageria — mas com foco em tipagem, async nativo e melhor DX (developer experience).

```python
from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost/")
app = FastStream(broker)

@broker.subscriber("minha-fila")
async def handle(msg: str):
    print(f"Recebido: {msg}")
```

Conceitos importantes no FastStream:
- **routing key** → identifica o destino da mensagem publicada pelo produtor.
- **binding key** → define quais mensagens a fila aceita (configurado na exchange).

---

## Teste de Carga: Locust

Para validar o comportamento do sistema sob carga, use o **Locust** — biblioteca Python com interface gráfica simples.

```python
from locust import HttpUser, task

class MeuUsuario(HttpUser):
    @task
    def publicar_evento(self):
        self.client.post("/events", json={"tipo": "teste"})
```

Execute com `locust -f locustfile.py` e acesse `http://localhost:8089`.

Documentação: [locust.io](https://locust.io)