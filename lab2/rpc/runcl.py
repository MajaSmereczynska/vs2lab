import rpc
import logging
import time

from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)
logger = logging.getLogger('vs2lab.rpc.cl')

cl = rpc.Client()
cl.run()

base_list = rpc.DBList({'foo'})
cl.append('bar', base_list, lambda x: print("Result: {}".format(x.value)))

for _ in range(15):
    time.sleep(1)
    logger.info("Client sleeping")

cl.stop()
