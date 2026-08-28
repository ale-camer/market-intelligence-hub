# Issue #13 — Kafka Producer & Consumer

**Branch**: `feature/issue-13-kafka-messaging`
**Milestone**: M3 — Storage & Warehouse
**Depends on**: Issue #12 ✅
**Status**: 🟡 Not Started

---

## Objective

Implementar la capa de mensajería asíncrona y procesamiento en tiempo real utilizando **Apache Kafka**. Se desarrollarán clientes **Producer** y **Consumer** utilizando `confluent-kafka`, serializando las entidades del dominio (`MarketQuote`, `FinancialArticle`) preferentemente mediante **Avro** (`fastavro`) para asegurar consistencia de esquemas y eficiencia de red.

---

## Architecture

- **`src/messaging/kafka/`**: Directorio principal de mensajería.
  - `config.py`: Variables y parámetros de conexión (Bootstrap servers, Schema Registry, Consumer Groups).
  - `producer.py`: Clase `KafkaEventProducer` encargada de serializar y enviar (publish) eventos.
  - `consumer.py`: Clase `KafkaEventConsumer` encargada de suscribirse, realizar `poll()` y deserializar eventos.
  - `schemas/`: Archivos `.avsc` (Avro Schemas) que definen la estructura de los contratos de mensajería.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurarse de tener la rama actualizada: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-13-kafka-messaging`.
- [ ] Validar que las dependencias `confluent-kafka` y `fastavro` estén presentes en `pyproject.toml`.

### ⚙️ Step 2 — Configuration & Avro Schemas
- [ ] Desarrollar `src/messaging/kafka/config.py` con settings basales (e.g., `KAFKA_BOOTSTRAP_SERVERS="localhost:9092"`).
- [ ] Crear el directorio `src/messaging/kafka/schemas/`.
- [ ] Escribir `market_quote.avsc` (definiendo campos de `MarketQuote`).
- [ ] Escribir `financial_news.avsc` (definiendo campos de `FinancialArticle`).

### 🚀 Step 3 — Kafka Producer
- [ ] Desarrollar `src/messaging/kafka/producer.py`.
- [ ] Implementar la clase `KafkaEventProducer` envolviendo `confluent_kafka.Producer`.
- [ ] Crear método `publish_market_quote(quote: MarketQuote)` publicando en el tópico `market-events`.
- [ ] Crear método `publish_financial_news(article: FinancialArticle)` publicando en el tópico `news-events`.
- [ ] Incorporar callbacks de confirmación (`delivery_report`) para logs de éxito/fallo.

### 📥 Step 4 — Kafka Consumer
- [ ] Desarrollar `src/messaging/kafka/consumer.py`.
- [ ] Implementar la clase `KafkaEventConsumer` envolviendo `confluent_kafka.Consumer` e inyectando un `group.id`.
- [ ] Crear método `subscribe(topics: list[str])`.
- [ ] Crear método generador `consume_events(timeout: float = 1.0)` que implemente el loop iterativo de `poll()` manejando errores de Kafka y deserializando con Avro a dicts.

### 🧪 Step 5 — Local Tests (Mocks)
- [ ] Crear `tests/unit/messaging/test_kafka.py`.
- [ ] Utilizar `unittest.mock.patch` para interceptar llamadas nativas de `confluent_kafka.Producer` y `Consumer`.
- [ ] Validar la correcta serialización de objetos Pydantic contra los esquemas Avro (usando `fastavro` de forma aislada).

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `make format && make lint && make typecheck && make coverage`
- [ ] `git add -A`
- [ ] `git commit -m "feat(messaging): implement kafka producer and consumer clients (#13)"`
- [ ] `git push origin feature/issue-13-kafka-messaging`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.
- [ ] Issue #13 closed on GitHub.

---

## Design Notes
- Kafka actuará como el bus de datos en tiempo real del proyecto. Las abstracciones Pydantic creadas en M1 son la única fuente de verdad (Single Source of Truth), y deben ser serializadas en bytes antes de enviarse a Kafka.
- La serialización Avro (`fastavro.schemaless_writer`) es recomendada porque el payload es muy liviano, perfecto para arquitecturas orientadas a eventos y pipelines robustos.
