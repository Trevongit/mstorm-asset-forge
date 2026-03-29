# Blender Asset Forge Addon
import bpy
import threading
import socket
import json
import os

bl_info = {
    "name": "Asset Forge Blender",
    "description": "Blender component for the MStorm Asset Forge",
    "author": "Asset Forge Team",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Asset Forge",
    "category": "Asset Forge",
}

class AssetForgeAgentServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.sock = None
        self.is_running = False
        self.thread = None

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.sock.settimeout(1.0)
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        print(f"AssetForgeAgentServer started on {self.host}:{self.port}")

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()
        if self.sock:
            self.sock.close()
        print("AssetForgeAgentServer stopped")

    def _run(self):
        while self.is_running:
            try:
                conn, addr = self.sock.accept()
                with conn:
                    data = conn.recv(4096)
                    if not data:
                        continue
                    msg = json.loads(data.decode('utf-8'))
                    if msg['type'] == 'execute':
                        code = msg['data']['code']
                        # Use a timer to execute in main thread
                        bpy.app.timers.register(lambda: self._execute_code(code))
                        conn.sendall(json.dumps({"status": "success", "message": "Code scheduled"}).encode('utf-8'))
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Server error: {e}")

    def _execute_code(self, code):
        try:
            exec(code, globals())
        except Exception as e:
            print(f"Execution error: {e}")
        return None

# Blender UI and Registration
class ASSETFORGE_PT_Panel(bpy.types.Panel):
    bl_label = "MStorm Asset Forge"
    bl_idname = "ASSETFORGE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Asset Forge'

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        if not bpy.app.driver_namespace.get("_asset_forge_server"):
            col.operator("asset_forge.start_server", text="Start Server", icon='PLAY')
        else:
            col.operator("asset_forge.stop_server", text="Stop Server", icon='PAUSE')

class ASSETFORGE_OT_StartServer(bpy.types.Operator):
    bl_idname = "asset_forge.start_server"
    bl_label = "Start Asset Forge Server"
    
    def execute(self, context):
        server = AssetForgeAgentServer()
        server.start()
        bpy.app.driver_namespace["_asset_forge_server"] = server
        return {'FINISHED'}

class ASSETFORGE_OT_StopServer(bpy.types.Operator):
    bl_idname = "asset_forge.stop_server"
    bl_label = "Stop Asset Forge Server"
    
    def execute(self, context):
        server = bpy.app.driver_namespace.get("_asset_forge_server")
        if server:
            server.stop()
            del bpy.app.driver_namespace["_asset_forge_server"]
        return {'FINISHED'}

classes = (
    ASSETFORGE_PT_Panel,
    ASSETFORGE_OT_StartServer,
    ASSETFORGE_OT_StopServer,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    server = bpy.app.driver_namespace.get("_asset_forge_server")
    if server:
        server.stop()

if __name__ == "__main__":
    register()
