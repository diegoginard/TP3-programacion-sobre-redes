import socket
import json
import sys
import time

def send_task(host='127.0.0.1', port=65432, task_type="process_data"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        
        task = {
            "task_id": f"task_{int(time.time())}",
            "type": task_type,
            "data": "Datos de ejemplo para procesar",
            "timestamp": time.time()
        }
        
        message = json.dumps(task).encode('utf-8')
        client.sendall(message)
        
        # Recibir respuesta
        response = client.recv(4096).decode('utf-8')
        result = json.loads(response)
        
        print("✅ Respuesta del servidor:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task_type = sys.argv[1]
    else:
        task_type = "process_data"
    
    print(f"Enviando tarea de tipo: {task_type}")
    send_task(task_type=task_type)