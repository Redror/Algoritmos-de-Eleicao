import time
from process import Process
from logging_config import logger

class BullyProcess(Process):
    """Implementa o algoritmo de eleição Bully."""
    def __init__(self, process_id, all_processes):
        super().__init__(process_id, all_processes)
        self.election_in_progress = False
        self.waiting_for_ok = False

    def start_election(self):
        """Inicia uma eleição usando o algoritmo Bully."""
        if self.election_in_progress:
            return

        logger.warning(f"[P{self.id}] Inicia ELEIÇÃO (Bully).")
        self.election_in_progress = True
        self.waiting_for_ok = True
        
        higher_processes = [pid for pid in self.all_processes if pid > self.id]

        if not higher_processes:
          
            self.announce_victory()
            return
            
       
        responses = 0
        for pid in higher_processes:
            logger.debug(f"[P{self.id}] Enviando mensagem de ELEIÇÃO para [P{pid}].")
            if self.send_message(pid, {'type': 'ELECTION_BULLY', 'from': self.id}):
                responses += 1

        if responses == 0:
       
            self.announce_victory()
            return

  
        time.sleep(1.5) 
        self.waiting_for_ok = False

        if not hasattr(self, 'got_ok') or not self.got_ok:
           
            self.announce_victory()
        
     
        self.got_ok = False
        self.election_in_progress = False


    def run(self):
        """Loop principal do processo, escutando mensagens."""
        while self.active:
            try:
                message = self.message_queue.get(timeout=1)
                self._handle_message(message)
            except Exception:
                
                self.check_coordinator()
        
    def _handle_message(self, message):
        """Processa as mensagens recebidas."""
        msg_type = message.get('type')

        if not self.active: return 

        if msg_type == 'ELECTION_BULLY':
            sender_id = message.get('from')
            logger.debug(f"[P{self.id}] Recebeu ELEIÇÃO de [P{sender_id}]. Enviando OK.")
            self.send_message(sender_id, {'type': 'OK_BULLY', 'from': self.id})
         
            if not self.election_in_progress:
                self.start_election()
        
        elif msg_type == 'OK_BULLY':
             if self.waiting_for_ok:
                logger.debug(f"[P{self.id}] Recebeu OK de [P{message.get('from')}]. Desistindo da eleição.")
                self.got_ok = True
        
        elif msg_type == 'COORDINATOR_BULLY':
            new_coord_id = message.get('from')
            logger.info(f"[P{self.id}] Recebeu anúncio. Novo coordenador é [P{new_coord_id}].")
            self.set_coordinator(new_coord_id)
            self.election_in_progress = False

    def announce_victory(self):
        """Anuncia para todos os processos que é o novo coordenador."""
        logger.info(f"🏆 [P{self.id}] Venci a eleição! Anunciando a todos...")
        for pid, process in self.all_processes.items():
            self.send_message(pid, {'type': 'COORDINATOR_BULLY', 'from': self.id})
        self.set_coordinator(self.id)
        self.election_in_progress = False