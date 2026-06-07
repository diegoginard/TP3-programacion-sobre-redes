# Diagrama de Arquitectura - Sistema Distribuido Cliente-Servidor

```mermaid
flowchart TD
    subgraph Clientes
        C1[Cliente Web]
        C2[Cliente Móvil]
        C3[Cliente Desktop]
    end

    subgraph "Balanceador de Carga"
        LB[Nginx / HAProxy]
    end

    subgraph "Servidores de Aplicación"
        S1[Worker Server 1\nThread Pool]
        S2[Worker Server 2\nThread Pool]
        S3[Worker Server N\nThread Pool]
    end

    subgraph "Cola de Mensajes"
        MQ[RabbitMQ]
    end

    subgraph "Almacenamiento Distribuido"
        DB[PostgreSQL Cluster]
        S3Storage[S3 / MinIO]
    end

    Clientes --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    S1 <--> MQ
    S2 <--> MQ
    S3 <--> MQ
    S1 <--> DB
    S2 <--> DB
    S3 <--> DB
    S1 <--> S3Storage
    S2 <--> S3Storage
    S3 <--> S3Storage

    classDef client fill:#4ade80,stroke:#166534
    classDef lb fill:#60a5fa,stroke:#1e40af
    classDef server fill:#f87171,stroke:#991b1b
    classDef queue fill:#c084fc,stroke:#6b21a8
    classDef storage fill:#fbbf24,stroke:#b45309

    class Clientes client
    class LB lb
    class Servidores server
    class MQ queue
    class Almacenamiento storage
```

## Explicación del Diagrama
- **Clientes**: Acceden a través de web/móvil.
- **Balanceador**: Distribuye conexiones entre servidores.
- **Workers**: Cada uno maneja un pool de hilos para procesar tareas concurrentemente.
- **RabbitMQ**: Para comunicación asíncrona entre servidores/workers.
- **Almacenamiento**: PostgreSQL para datos estructurados + S3 para archivos.