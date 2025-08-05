import time
from process import Process
from logging_config import logger



class RingProcess(Process):
    """Implementa o algoritmo de eleição em Anel."""
    def __init__(self, process_id, all_processes):
        super().__init__(process_id, all_processes)
        self.next_node_id = None 

    def setup_ring(self):
        """Define o próximo nó no anel após todos os processos serem criados."""
        self.next_node_id = (self.id + 1) % len(self.all_processes)

    def find_next_active_node(self, start_id):
        """Encontra o próximo nó ativo no anel."""
        next_id = (start_id + 1) % len(self.all_processes)
        while next_id != self.id:
            if self.all_processes[next_id].active:
                return next_id
            next_id = (next_id + 1) % len(self.all_processes)
        return self.id 

    def start_election(self):
        """Inicia uma eleição usando o algoritmo em Anel."""
        next_id = self.find_next_active_node(self.id)
        election_message = {
            'type': 'ELECTION_RING',
            'participant_ids': [self.id]
        }
        logger.warning(f"[P{self.id}] Inicia ELEIÇÃO (Anel), enviando para [P{next_id}].")
        self.send_message(next_id, election_message)
    
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

        if msg_type == 'ELECTION_RING':
            participants = message.get('participant_ids', [])
            
            if self.id in participants:
            
                winner_id = max(participants)
                logger.info(f"✨ [P{self.id}] Eleição em Anel concluída. Participantes: {participants}. Vencedor: [P{winner_id}].")
                
               
                coordinator_message = {'type': 'COORDINATOR_RING', 'coordinator_id': winner_id}
                next_id = self.find_next_active_node(self.id)
                self.send_message(next_id, coordinator_message)
                self.set_coordinator(winner_id)
            else:
               
                participants.append(self.id)
                next_id = self.find_next_active_node(self.id)
                logger.debug(f"[P{self.id}] Participando da Eleição em Anel. Passando para [P{next_id}]. Participantes: {participants}")
                self.send_message(next_id, {'type': 'ELECTION_RING', 'participant_ids': participants})

        elif msg_type == 'COORDINATOR_RING':
            new_coord_id = message.get('coordinator_id')
            if self.coordinator_id == new_coord_id:
               
                return 
                
            logger.info(f"[P{self.id}] Recebeu anúncio. Novo coordenador é [P{new_coord_id}].")
            self.set_coordinator(new_coord_id)
            
           
            next_id = self.find_next_active_node(self.id)
            self.send_message(next_id, message)