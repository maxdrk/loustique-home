import logging

def setup_log():
    logger = logging.getLogger("loustique")
    logger.setLevel(logging.DEBUG)
    
    handler = logging.FileHandler('/var/log/loustique.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.handlers = []  
    werkzeug_logger.addHandler(handler)  
    werkzeug_logger.propagate = False

    return logger

log = setup_log()