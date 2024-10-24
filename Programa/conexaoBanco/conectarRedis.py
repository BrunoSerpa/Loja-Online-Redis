from Programa.funcoes.utils.salvarErro import salvarErro

import redis

def conectarRedis():
    try:
        cliente = redis.Redis(
            host='host',
            port='porta',
            password='senha'
        )
        return cliente
    except Exception as e:  
        salvarErro("Erro ao conectar ao Redis", e)
        return None