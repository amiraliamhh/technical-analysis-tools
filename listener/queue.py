import pika
import json
import psycopg2
import redis
import logging

class Queue:
    def __init__(self, Decider):
        self.Decider = Decider
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        conn = psycopg2.connect("dbname=cryptoc user=cryptoc password=1234asdf")
        self.cur = conn.cursor()

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = connection.channel()

        self.channel.queue_declare(queue='candlestick')

    def callback(self, ch, method, properties, body):
        lastCandle = json.loads(body)
        pair = lastCandle['pair']
        self.cur.execute("""
        SELECT 
        CAST("c" AS float) AS "close", 
        CAST(o AS float) AS "open", 
        CAST(l AS float) AS "low", 
        CAST(h AS float) AS "high",
        (CAST(h AS float) - CAST(o AS float)) / CAST(o AS float) AS bindex,
        (CAST(o AS float) - CAST(l AS float)) / CAST(o AS float) AS sindex,
        CASE
        WHEN CAST("c" AS float) - CAST(o AS float) > 0 THEN TRUE
        ELSE FALSE END AS green
        FROM """ + pair.lower() + """;""")
        candles = self.cur.fetchall()
        decider = self.Decider(candles, lastCandle['close'], isTuple=True)
        decision = decider.decision()
        if decision == -1:
            # send buy signal
            self.channel.basic_publish(exchange='',
                routing_key='buy_signal',
                body=pair)
        elif decision == 0:
            pass
        else:
            # save take profit in redis
            saved = self.r.set(pair.lower(), decision)
            if not saved:
                logging.error(saved)

    def run(self):
        self.channel.basic_consume(
            queue='candlestick', on_message_callback=self.callback, auto_ack=True)

        print('Subscribed to queue ...')
        self.channel.start_consuming()