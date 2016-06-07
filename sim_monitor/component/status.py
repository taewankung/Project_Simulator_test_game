from sim_monitor.sim_client.client_map import ApaimaneeMOBAClient

class Status:
    def __init__(self, hero):
        self.ac = ApaimaneeMOBAClient()
        self.hp = self.ac.game_logic.game_space


