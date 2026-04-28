# cdc-mysql-to-mongodb-pipeline

**Overview**

This project demonstrates a lightweight **Change Data Capture (CDC)** pipeline that replicates data from a MySQL source system into a MongoDB target system using Python, Docker, and scheduled synchronization.  The pipeline simulates real-time data ingestion and propagation across heterogeneous databases—an essential pattern in modern data engineering.

**Architecture**
```python
MySQL (Source)  →  Scheduler (CDC Logic)  →  MongoDB (Target)
        ↑                  ↓
   Data Generation     Incremental Sync
```

**Key Components**
1. *Container Management*
   - Creates and destroys MySQL and MongoDB containers
   - Initializes MySQL schema
   - Uses environment variables for secure configuration

2. *MySQL (Source System)*
   - Creates `pluto` database and `posts` table
   - Inserts timestamp-based records (simulated events)
   - Supports read/write/delete operations

3. *MongoDB (Target System)*
   - Stores replicated records in `posts` collection
   - Uses **upsert logic** to avoid duplication
   - Supports read/write/delete operations
  
4. *Scheduler (CDC Engine)*
   
   - Runs a timed loop every 5 seconds
   - Writes new records to MySQL
   - Extracts latest records and syncs to MongoDB
   - Verifies replication integrity

**Data Flow**
1. Generate new record in MySQL
2. Read latest records from MySQL
3. Push records to MongoDB (upsert)
4. Validate replication
5. repeat on schedule

**How to Run**

1. **Set Environment Variable**
```python
export MYSQL_ROOT_PASSWORD = yourpassword
```

2. **Create Container**
   ```python
   python container.py -create
   ```

3. **Initialize MySQL**
   ```python
   python container.py -init
   ```

4. **Start CDC Pipeline**
   ```python
   python scheduler.py
   ```

5. **Stop Pipeline**
   ```python
   stop_timer()
   ```

**Real-World Use Cases**
- Event streaming simulation
- Microservices data synchronization
- Prototyping ETL/ELT pipelines

**Limitations**
- Not true CDC (no binlog tracking)
- No offset/state management
- No failure recovery
- No scalability (single-threaded timer)
- No schema evolution handling