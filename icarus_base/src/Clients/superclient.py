from threading import Thread, Lock
from src.skillstrategy import SkillStrategy
from src.message import MessageInfo
import time
import random

# outgoing = []
# outgoing_lock = Lock()


class SuperClient(Thread):

    id = None
    stop_request = False
    skill_strategy = None
    skill_threads = None

    def __init__(self, skill_strategy: SkillStrategy):
        Thread.__init__(self)
        self.id = random.randint(0, 999)
        self.skill_strategy = skill_strategy
        self.skill_threads = []

    def _queue_new_message(self, message: str, client_opt: dict = None):
        # print("Added new Message: {} to queue of length {}".format(message, len(self.inbound_fifo)))
        if message is "":
            return
        message = MessageInfo(message, self, client_opt)

        self.skill_strategy.get_matching_skill(message)
        message.run_next_skill()

    def stop(self):
        self.stop_request = True

    def send(self, message: str, client_attr):
        pass


class ClientStopException(Exception):
    pass
