# Diagrama de Arquitectura - Sistema Distribuido Cliente-Servidor

```mermaid
flowchart TD
    subgraph Clientes
        C1[🌐 Cliente Web]
        C2[📱 Cliente Móvil]
        C3[🖥️ Cliente Desktop]
    end

    subgraph LB["Balanceador de Carga"]
        NX[Nginx / HAProxy]
    end

    subgraph Servidores["Servidores Workers"]
        S1["🖧 Worker Server 1\n(Thread Pool)"]
        S2["🖧 Worker Server 2\n(Thread Pool)"]
        S3["🖧 Worker Server N\n(Thread Pool)"]
    end

    subgraph Cola["Cola de Mensajes"]
        MQ[🐇 RabbitMQ]
    end

    subgraph Almacenamiento["Almacenamiento Distribuido"]
        DB[(🐘 PostgreSQL)]
        S3S[☁️ S3 / MinIO]
    end

    C1 --> NX
    C2 --> NX
    C3 --> NX

    NX --> S1
    NX --> S2
    NX --> S3

    S1 <--> MQ
    S2 <--> MQ
    S3 <--> MQ

    S1 <--> DB
    S2 <--> DB
    S3 <--> DB

    S1 <--> S3S
    S2 <--> S3S
    S3 <--> S3S

    classDef clientStyle fill:#4ade80,stroke:#166534,color:#000
    classDef lbStyle fill:#60a5fa,stroke:#1e40af,color:#000
    classDef serverStyle fill:#f87171,stroke:#991b1b,color:#000
    classDef queueStyle fill:#c084fc,stroke:#6b21a8,color:#000
    classDef storageStyle fill:#fbbf24,stroke:#b45309,color:#000

    class C1,C2,C3 clientStyle
    class NX lbStyle
    class S1,S2,S3 serverStyle
    class MQ queueStyle
    class DB,S3S storageStyle
```

## Explicación de cada capa

| Componente | Rol |
|---|---|
| **Clientes** (web, móvil, desktop) | Envían tareas al sistema vía HTTP o sockets |
| **Balanceador (Nginx / HAProxy)** | Distribuye las conexiones entrantes entre los servidores workers |
| **Worker Servers** | Cada servidor tiene un `ThreadPoolExecutor` con N hilos. Reciben la tarea, la procesan y devuelven el resultado |
| **RabbitMQ** | Cola de mensajes para comunicación asíncrona entre servidores (p. ej., redistribuir trabajo, notificaciones) |
| **PostgreSQL** | Base de datos relacional para guardar resultados y estado de las tareas |
| **S3 / MinIO** | Almacenamiento distribuido de objetos (archivos, imágenes, resultados pesados) |

## Flujo de una tarea

```
Cliente → Balanceador → Worker Server → Thread Pool → Resultado → Cliente
                                    ↕
                                 RabbitMQ
                                    ↕
                         PostgreSQL / S3 (persistencia)
```