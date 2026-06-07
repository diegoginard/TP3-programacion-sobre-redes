import socket
import json
import time

HOST = "127.0.0.1"
PORT = 65432

def enviar_tarea(tipo):
    tarea = {
        "task_id": f"task_{int(time.time())}",
        "tipo": tipo,
        "datos": "Datos de ejemplo"
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.sendall(json.dumps(tarea).encode("utf-8"))
    print(f"[Cliente] Tarea enviada: {tarea}")

    respuesta = client.recv(4096).decode("utf-8")
    resultado = json.loads(respuesta)

    print(f"[Cliente] Respuesta del servidor:")
    print(json.dumps(resultado, indent=2, ensure_ascii=False))

    client.close()

if __name__ == "__main__":
    print("Tipos de tarea disponibles:")
    print("  1. calcular")
    print("  2. procesar_texto")
    print("  3. analizar_imagen")
    tipo = input("Ingresá el tipo de tarea: ").strip()
    enviar_tarea(tipo)