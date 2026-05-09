import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r.hset('bicicleta:1', mapping={
	'color': 'azul', 
	'marca': 'ORBEA', 
	'tipo': 'carreras', 
	'precio': '400'
	})
v = r.hmget('bicicleta:1','marca', 'precio')
v1 = r.hgetall('bicicleta:1')
print(v)
print(v1)

r.close()
