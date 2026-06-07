# PFO 3 - Sistema Distribuido Cliente-Servidor

## Descripción
Rediseño de un sistema como arquitectura distribuida usando sockets en Python, con soporte para múltiples workers y thread pools.

## Estructura del Proyecto
```
pfo3_distributed_system/
├── diagram.md          # Diagrama en Mermaid
├── server.py           # Servidor con thread pool
├── client.py           # Cliente para enviar tareas
└── README.md
```

## Cómo Ejecutar

### 1. Iniciar el Servidor
```bash
python server.py
```

### 2. Ejecutar el Cliente (en otra terminal)
```bash
python client.py
# o con tipo de tarea específica
python client.py analizar_imagen
```

## Arquitectura
- **Sockets TCP** para comunicación cliente-servidor.
- **ThreadPoolExecutor** para procesar múltiples tareas concurrentemente.
- Preparado para escalar con Load Balancer + RabbitMQ + PostgreSQL.

## Próximos Pasos (para producción)
1. Implementar RabbitMQ para distribución asíncrona de tareas.
2. Agregar Nginx/HAProxy como balanceador.
3. Conectar a PostgreSQL para persistencia.
4. Dockerizar los servicios.