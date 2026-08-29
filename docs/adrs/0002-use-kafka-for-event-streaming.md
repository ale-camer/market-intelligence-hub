# ADR 0002: Use Kafka for Event Streaming

## Status
Accepted

## Context
The platform requires robust data ingestion from external APIs. Directly writing data from Airflow tasks to the Data Warehouse or PostgreSQL can lead to tight coupling, high latency, and dropped data in case of database downtime or schema changes. We needed a decoupled messaging layer to buffer incoming data.

## Decision
We decided to use **Apache Kafka** as the central event streaming bus for all raw data ingestion before it is persisted to storage.

## Consequences
- **Positive:**
  - Decouples producers (extractors) from consumers (loaders).
  - Provides a highly scalable, fault-tolerant buffer that prevents data loss during downtime.
  - Allows multiple consumers to subscribe to the same data streams (e.g., real-time analytics vs. batch storage).
- **Negative:**
  - Adds operational complexity (managing Zookeeper/Kraft, Kafka brokers, topics).
  - Increases the infrastructure footprint of the local stack.
