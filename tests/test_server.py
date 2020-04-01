import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from final import server

ADDRESS = '127.0.0.1', 5000


def test_server():
    server.run_server(address=ADDRESS, data_dir="./users")
    print("server running")


test_server()
