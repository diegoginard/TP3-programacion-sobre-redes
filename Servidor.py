import socket
import threading
import queue
import json
import time
from concurrent.futures import ThreadPoolExecutor

class TaskServer:
    def __init__(self, host='0.0.0.0', port=65432, max_workers=10):
        self.host = host
        self.port = port
        self.task_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.running = True

    def process_task(self, task_data):
        """Simula procesamiento de una tarea"""
        try:
            print(f"Procesando tarea: {task_data}")
            # Simular trabajo (ej: cálculo, procesamiento)
            time.sleep(2)  
            
            result = {
                "status": "success",
                "task_id": task_data.get("task_id"),
                "result": f"Resultado de {task_data.get('type', 'unknown')}",
                "processed_at": time.time()
            }
            return result
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def handle_client(self, client_socket, addr):
        """Maneja la conexión de un cliente"""
        print(f"Conexión desde {addr}")
        try:
            data = client_socket.recv(4096).decode('utf-8')
            if data:
                task = json.loads(data)
                print(f"Tarea recibida: {task}")
                
                # Enviar a thread pool
                future = self.executor.submit(self.process_task, task)
                result = future.result()
                
                # Responder al cliente
                response = json.dumps(result).encode('utf-8')
                client_socket.sendall(response)
        except Exception as e:
            print(f"Error manejando cliente {addr}: {e}")
        finally:
            client_socket.close()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, addr)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print(f"Error aceptando conexión: {e}")

        server_socket.close()

if __name__ == "__main__":
    server = TaskServer()
    server.start()