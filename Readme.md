# PFO 3 — Sistema Distribuido Cliente-Servidor

**Materia:** Programación sobre Redes  
**Objetivo:** Rediseño de un sistema como arquitectura distribuida usando sockets en Python.

---

## Arquitectura del sistema

```
[Cliente Web / Móvil / Desktop]
          │
          ▼
  [Balanceador de Carga]      ← Nginx / HAProxy
          │
    ┌─────┼─────┐
    ▼     ▼     ▼
[Worker] [Worker] [Worker]    ← Servidor.py (Thread Pool)
    │       │       │
    └───────┼───────┘
            ▼
        [RabbitMQ]            ← Cola de mensajes entre servidores
            │
    ┌───────┴───────┐
    ▼               ▼
[PostgreSQL]      [S3/MinIO]  ← Almacenamiento distribuido
```

El diagrama completo en Mermaid se encuentra en [`Diagram.md`](Diagram.md).

---

## Archivos

| Archivo | Descripción |
|---|---|
| `Servidor.py` | Servidor TCP con pool de hilos (`ThreadPoolExecutor`). Recibe tareas de los clientes y las distribuye a workers. |
| `Cliente.py` | Cliente TCP que envía una tarea al servidor y muestra el resultado. |
| `Diagram.md` | Diagrama de la arquitectura completa en Mermaid. |

---

## Cómo ejecutar

### 1. Iniciar el servidor

```bash
python Servidor.py
```

Salida esperada:
```
[Servidor] Escuchando en 0.0.0.0:65432 con 4 workers
```

### 2. Ejecutar el cliente (en otra terminal)

```bash
python Cliente.py
```

Salida esperada:
```
Tipos de tarea disponibles:
  1. calcular
  2. procesar_texto
  3. analizar_imagen
Ingresá el tipo de tarea: calcular
[Cliente] Tarea enviada: {'task_id': 'task_1749...', 'tipo': 'calcular', ...}
[Cliente] Respuesta del servidor:
{
  "status": "exitoso",
  "task_id": "task_1749...",
  "resultado": "Tarea 'calcular' procesada correctamente",
  "timestamp": "01:20:05"
}
```

---

## Tecnologías utilizadas

- **Python 3** — lenguaje de implementación
- **socket** — comunicación TCP entre cliente y servidor
- **threading** — un hilo por cliente conectado
- **concurrent.futures.ThreadPoolExecutor** — pool de workers para procesar tareas concurrentemente
- **json** — serialización de mensajes

## Componentes del sistema distribuido (diseño)

| Componente | Tecnología |
|---|---|
| Balanceador de carga | Nginx / HAProxy |
| Cola de mensajes | RabbitMQ |
| Base de datos | PostgreSQL |
| Almacenamiento de objetos | Amazon S3 / MinIO |