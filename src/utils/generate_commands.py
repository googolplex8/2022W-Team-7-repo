from collections import deque
import time


class CommandGenerator:
    gestures = deque([])
    last_command_time = 0

    def __init__(self, deque_size=10, command_interval=1, vote_threshold=0.7):
        self.deque_size = deque_size
        self.command_interval = command_interval
        self.vote_count = vote_threshold*deque_size

    def add_gestures(self, gesture):
        if time.time() - self.last_command_time > self.command_interval:
            self.gestures.append(gesture)
            if len(self.gestures) > self.deque_size:
                self.gestures.popleft()

    def get_command(self):
        current_time = time.time()
        if current_time - self.last_command_time > self.command_interval:
            
            majority_vote = self.get_majority_vote()
            # open and close gestures
            if majority_vote == -1:
                return -1
            else:
                self.last_command_time = time.time()
                self.gestures.clear()
                return majority_vote
        # it has not been long enough since last command
        else:
            return -1

    def get_majority_vote(self):
        if self.gestures.count(2) >= self.vote_count:
            return 2
        elif self.gestures.count(3) >= self.vote_count:
            return 3
        elif self.gestures.count(4) >= self.vote_count:
            return 4
        elif self.gestures.count(5) >= self.vote_count:
            return 5
        elif self.gestures.count(6) >= self.vote_count:
            return 6
        return -1
