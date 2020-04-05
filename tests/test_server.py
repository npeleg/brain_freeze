import pytest
from final import server

ADDRESS = '127.0.0.1', 5000


def test_server(tmp_path):
    server.run_server(address=ADDRESS, data_dir="./users")
    print("server running")

