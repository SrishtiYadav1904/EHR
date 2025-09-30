#Distributed Electronic Hospital Record (EHR) System
🌟 Project Overview
This is a university mini-project using XML-RPC to simulate a secure, highly available, and concurrent Electronic Hospital Record (EHR) system. The implementation integrates solutions for critical distributed computing challenges.

✨ Key Distributed Features
The system achieves integrity and resilience through several key algorithms:

Concurrency Control: Manages simultaneous updates using Ricart-Agrawala and Priority-Based Locking to resolve conflicts and ensure correct transaction ordering.

Data Consistency: Ensures durability and fault tolerance through Quorum-Based Replication across multiple server replicas.

Clock Synchronization: Uses a Berkeley Algorithm variant to guarantee all patient and doctor log entries have uniform, consistent timestamps.

Load Management: Implements Internal Cloning to balance load and ensure fast responses for patient read requests under heavy traffic.

⚙️ Core RPC Functions
All system logic is handled by the three primary XML-RPC functions: doctor(), patient(), and exchange().
