import socket
import threading
import json
import time
from concurrent.futures import ThreadPoolExecutor

def procesar_tarea(tarea):
    """Simula el procesamiento de una tarea en un worker."""
    print(f"[Worker] Procesando tarea: {tarea['task_id']} | tipo: {tarea['tipo']}")
    time.sleep(2)  # Simula trabajo
    return {
        "status": "exitoso",
        "task_id": tarea["task_id"],
        "resultado": f"Tarea '{tarea['tipo']}' procesada correctamente",
        "timestamp": time.strftime("%H:%M:%S")
    }

def manejar_cliente(conn, addr):
    """Maneja la conexión de un cliente y despacha su tarea al pool."""
    print(f"[Servidor] Conexión recibida desde {addr}")
    try:
        datos = conn.recv(4096).decode("utf-8")
        tarea = json.loads(datos)

        # Enviamos la tarea al pool de workers
        future = executor.submit(procesar_tarea, tarea)
        resultado = future.result()

        conn.sendall(json.dumps(resultado).encode("utf-8"))
    except Exception as e:
        error = json.dumps({"status": "error", "mensaje": str(e)})
        conn.sendall(error.encode("utf-8"))
    finally:
        conn.close()
        print(f"[Servidor] Conexión cerrada: {addr}")

HOST = "0.0.0.0"
PORT = 65432
MAX_WORKERS = 4

executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(10)

print(f"[Servidor] Escuchando en {HOST}:{PORT} con {MAX_WORKERS} workers")

while True:
    conn, addr = server.accept()
    hilo = threading.Thread(target=manejar_cliente, args=(conn, addr))
    hilo.daemon = True
    hilo.start()