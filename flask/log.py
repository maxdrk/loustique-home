import logging 

logging.basicConfig(
filename='/var/log/loustique.log',
filemode='a',
format='%(asctime)s - %(name)s - %(levelname)/s - %(message)/s',
level=logging.DEBUG)



