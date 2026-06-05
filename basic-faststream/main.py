from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import BaseModel

broker = RabbitBroker()
app = FastStream(broker)

class Pessoa(BaseModel):
    nome: str
    idade: int

@broker.subscriber("test")
async def base_handler(pessoa: Pessoa):
    print("Olaa {pessoa.nome}]")
    return pessoa

