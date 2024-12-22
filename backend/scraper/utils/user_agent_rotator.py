import random

class UserAgentRotator:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
            'Mozilla/5.0 (X11; Linux x86_64)...',
            # Add more user-agent strings
        ]

    def get_user_agent(self):
        return random.choice(self.user_agents)
