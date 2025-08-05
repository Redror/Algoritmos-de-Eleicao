import logging

# Define um formato de log personalizado com cores para diferentes níveis
class ColorFormatter(logging.Formatter):
    GREY = "\x1b[38;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BLUE = "\x1b[34;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"

    FORMATS = {
        logging.INFO: f"[%(asctime)s] {GREEN}%(message)s{RESET}",
        logging.WARNING: f"[%(asctime)s] {YELLOW}%(message)s{RESET}",
        logging.ERROR: f"[%(asctime)s] {RED}%(message)s{RESET}",
        logging.CRITICAL: f"[%(asctime)s] {BOLD_RED}%(message)s{RESET}",
        logging.DEBUG: f"[%(asctime)s] {BLUE}%(message)s{RESET}",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def setup_logging():
    """Configura o logger principal para a simulação."""
    logger = logging.getLogger("Simulacao")
    logger.setLevel(logging.DEBUG)
    
    # Evita adicionar handlers duplicados
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(ColorFormatter())
        logger.addHandler(ch)
        
    return logger

logger = setup_logging()