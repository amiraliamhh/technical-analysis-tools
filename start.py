from listener import Queue
from bot import Decider

queue = Queue(Decider)

queue.run()
