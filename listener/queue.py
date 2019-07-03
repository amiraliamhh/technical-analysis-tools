#!/usr/bin/env python
import pika
import json
import psycopg2
import redis
from bot import Decider

r = redis.Redis(host='localhost', port=6379, db='takeprofits')

conn = psycopg2.connect("dbname=cryptoc user=cryptoc password=1234asdf")
cur = conn.cursor()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='candlestick')

def callback(ch, method, properties, body):
    lastCandle = json.loads(body)
    pair = lastCandle.pair
    cur.execute("""
    SELECT 
    "c" AS "close", 
    o AS "open", 
    l AS "low", 
    h AS "high",
    (CAST(h AS float) - CAST(o AS float)) / CAST(o AS float) AS bindex,
    (CAST(o AS float) - CAST(l AS float)) / CAST(o AS float) AS sindex,
    CASE
    WHEN CAST("c" AS float) - CAST(o AS float) > 0 THEN TRUE
    ELSE FALSE END AS green
    FROM %(tableName)s;
    """, { 'tableName': pair })
    candles = cur.fetchall()
    decider = Decider(candles, pair.close, isTuple=True)
    decision = decider.decision()
    if decision == -1:
        # send buy signal
        pass
    else:
        # save take profit in redis
        saved = r.set(pair, decision)
        if not saved:
            # handle error
            pass

channel.basic_consume(
    queue='candlestick', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()