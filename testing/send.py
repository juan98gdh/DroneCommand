#!/usr/bin/env python3

import pika

conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = conn.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='hello world')

print('\nsent messagge...\n')

conn.close()
