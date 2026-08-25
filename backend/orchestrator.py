import sys
import os

sys.path.append(os.path.abspath("."))

import requests
import json
import os
from backend.services.agent_services.chat import start_chat

start_chat()
