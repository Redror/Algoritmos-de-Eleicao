import threading
import time
import queue
from logging_config import logger

class Process(threading.Thread):
    """Classe base para um processo em um sistema distribuído simulado."""
    def __init__(self, process_id, all_processes):
        super().__init__()
        self.id = process_id
        self.all_processes = all_processes
        self.is_coordinator = False
        self.coordinator_id = None
        self.active = True
        self.message_queue = queue.Queue()
        self.daemon = True 

    def run(self):
        """Loop principal do processo."""
        while self.active:
            self.check_coordinator()
            time.sleep(2)

    def check_coordinator(self):
        """Verifica se o coordenador está ativo."""
        if self.coordinator_id is None or not self.all_processes[self.coordinator_id].active:
            if self.active:
                 logger.debug(f"[P{self.id}] Detectou a falha do coordenador {self.coordinator_id}. Iniciando eleição.")
                 self.start_election()
    
    def start_election(self):
        """Inicia o processo de eleição. Deve ser implementado pelas subclasses."""
        raise NotImplementedError

    def send_message(self, target_id, message):
        """Envia uma mensagem para a fila de outro processo."""
        if target_id in self.all_processes and self.all_processes[target_id].active:
            self.all_processes[target_id].message_queue.put(message)
            return True
        return False

    def set_coordinator(self, coordinator_id):
        """Define o novo coordenador."""
        self.coordinator_id = coordinator_id
        self.is_coordinator = (self.id == coordinator_id)
        if self.is_coordinator:
            logger.info(f"👑 [P{self.id}] Eu sou o novo COORDENADOR.")

    def deactivate(self):
        """Simula a falha do processo."""
        self.active = False
        logger.error(f"🔴 [P{self.id}] FALHOU e está offline.")

    def activate(self):
        """Simula a recuperação do processo."""
        self.active = True
        logger.info(f"🟢 [P{self.id}] RECUPERADO e está online.")
        self.start_election()