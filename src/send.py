import pika

if __name__ == "__main__":
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5674, virtual_host='/', 
        credentials=pika.credentials.PlainCredentials('admin', 'admin')))

    channel = connection.channel()

    channel.exchange_declare(exchange='exchangeX', durable=True)
    channel.queue_declare(queue='sincronizar', durable=True, 
    arguments = {'x-dead-letter-exchange': 'reprocessar', 'x-dead-letter-routing-key': 'sincronizar'})
    channel.queue_bind(queue='sincronizar', exchange='exchangeX', routing_key='sincronizar')

    message = '{ Id = 10 }'

    channel.basic_publish(exchange='exchangeX', routing_key='sincronizar', body=message, 
    properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2))
    print(" [x] Sent 'Hello World!'")
    connection.close()