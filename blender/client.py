import socket
import json
from .headless import execute_headless_blender, should_use_headless

HOST = 'localhost'
PORT = 8888

"""
BlenderClient: Minimal client for communicating with the Blender Asset Forge server.

Available functions:
    execute_code_socket(code): Execute Blender code via socket
"""

def execute_code_socket(code):
    """
    Execute Blender code via socket connection to the Asset Forge Blender addon.
    
    Args:
        code: The Python code to execute in Blender
        
    Returns:
        The response from the Blender server
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            client.sendall(json.dumps({"type": "execute", "data": {"code": code}}).encode('utf-8'))
            
            resp_data = b""
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break
                resp_data += chunk
                
            resp = json.loads(resp_data.decode('utf-8'))
            print(f"Server response: {resp}")
            return resp
        except ConnectionRefusedError:
            print(f"Error: Connection refused. Is the Asset Forge Blender addon running on {HOST}:{PORT}?")
            return {"status": "error", "message": f"Connection refused. Is the Asset Forge addon running?"}
        except Exception as e:
            print(f"Exception in execute_code_socket: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            client.close()
