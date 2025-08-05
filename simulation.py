import time
from bully_process import BullyProcess
from ring_process import RingProcess
from logging_config import logger

class Simulation:
    """Orquestra a simulação dos algoritmos de eleição."""
    def __init__(self, num_processes, algorithm_type):
        self.num_processes = num_processes
        self.algorithm_type = algorithm_type
        self.processes = {}
# TRECHO CORRIGIDO em simulation.py

    def _initialize_processes(self):
        """Cria e inicializa os processos para a simulação."""
        logger.critical(f"--- INICIANDO SIMULAÇÃO COM ALGORITMO {self.algorithm_type.upper()} ---")
        self.processes = {}
        process_class = BullyProcess if self.algorithm_type == 'bully' else RingProcess

        for i in range(self.num_processes):
            # Este laço cria todos os processos
            self.processes[i] = process_class(i, self.processes)

        # ADICIONE ESTA PARTE APENAS PARA O ANEL
        if self.algorithm_type == 'ring':
            for i in range(self.num_processes):
                # Este laço configura o anel, agora que todos os processos existem
                self.processes[i].setup_ring()
        
        # Define o coordenador inicial como o processo de maior ID
        initial_coordinator = self.num_processes - 1
        # ... (o resto do código continua igual) ...

        # Define o coordenador inicial como o processo de maior ID
        initial_coordinator = self.num_processes - 1
        for i in range(self.num_processes):
            self.processes[i].set_coordinator(initial_coordinator)
        
        logger.info(f"Sistema inicializado com {self.num_processes} processos. Coordenador inicial é [P{initial_coordinator}].")
        time.sleep(1)

    def start(self):
        """Inicia as threads de todos os processos."""
        for process in self.processes.values():
            process.start()
        logger.info("Todos os processos foram iniciados.")
        time.sleep(1)

    def stop(self):
        """Para todos os processos ativos."""
        for process in self.processes.values():
            if process.active:
                process.active = False
        logger.critical("--- FIM DA SIMULAÇÃO ---")
    
    def run_scenario_a(self):
        """
        Cenário A: Coordenador falha e retorna após eleição. 
        """
        logger.critical("\n--- EXECUTANDO CENÁRIO A ---")
        logger.warning("Cenário A: Coordenador falha e retorna após a eleição.")
        time.sleep(2)
        
        # 1. Falha do coordenador
        coordinator_id = self.num_processes - 1
        logger.error(f"SIMULAÇÃO: Desativando o coordenador [P{coordinator_id}].")
        self.processes[coordinator_id].deactivate()
        
        # 2. Espera a detecção da falha e a nova eleição
        logger.info("Aguardando detecção da falha e nova eleição...")
        time.sleep(8) # Tempo para a eleição acontecer

        # 3. Recupera o antigo coordenador
        logger.info(f"SIMULAÇÃO: Reativando o antigo coordenador [P{coordinator_id}].")
        self.processes[coordinator_id].activate()
        
        # 4. Observa a nova eleição (o antigo coordenador deve vencer se for Bully)
        logger.info("Aguardando a eleição iniciada pelo processo recuperado...")
        time.sleep(5)
        logger.critical("--- CENÁRIO A CONCLUÍDO ---\n")

    def run_scenario_b(self):
        """
        Cenário B: Múltiplos processos falham e um novo coordenador precisa ser escolhido. 
        """
        logger.critical("\n--- EXECUTANDO CENÁRIO B ---")
        logger.warning("Cenário B: Múltiplos processos falham, forçando uma nova eleição entre os sobreviventes.")
        time.sleep(2)

        # 1. Falha de múltiplos processos, incluindo o coordenador atual
        procs_to_fail = [self.num_processes - 1, self.num_processes - 3]
        for pid in procs_to_fail:
            if pid in self.processes:
                logger.error(f"SIMULAÇÃO: Desativando o processo [P{pid}].")
                self.processes[pid].deactivate()
                time.sleep(0.5)

        # 2. Espera a detecção e a nova eleição
        logger.info("Aguardando detecção da falha e nova eleição entre os processos restantes...")
        time.sleep(8)
        logger.critical("--- CENÁRIO B CONCLUÍDO ---\n")


if __name__ == '__main__':
    NUM_PROCESSOS = 6

    # Executa a simulação para o algoritmo Bully
    sim_bully = Simulation(NUM_PROCESSOS, 'bully')
    sim_bully._initialize_processes()
    sim_bully.start()
    sim_bully.run_scenario_a()
    time.sleep(3)
    sim_bully.run_scenario_b()
    sim_bully.stop()
    
    time.sleep(5) # Pausa entre as duas simulações

    # Executa a simulação para o algoritmo em Anel
    sim_ring = Simulation(NUM_PROCESSOS, 'ring')
    sim_ring._initialize_processes()
    sim_ring.start()
    sim_ring.run_scenario_a()
    time.sleep(3)
    sim_ring.run_scenario_b()
    sim_ring.stop()