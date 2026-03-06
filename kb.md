# Knowledge Base — Michael Mabinuola

Copyright© 2026 Michael Mabinuola

This document provides structured context about Michael Mabinuola's professional background. It is designed to be embedded in an LLM system prompt so the model can give accurate, relevant advice about Michael's career, skills, and experience.

---

## Identity

- **Name:** Michael Mabinuola
- **Email:** michaelmabinuola@gmail.com
- **Location:** Seoul, South Korea
- **Title:** Database & AI Engineer
- **Languages:** English (Native), Russian (Proficient), Korean (Intermediate)

---

## Professional Summary

Michael is a Database and AI Engineer with four years experience. He builds scalable, high-performance data and AI systems. His core specializations include SingleStore internal optimization, vector database architecture, Kafka data pipelines, and RAG-based AI applications. He has hands-on experience running client PoCs (proofs of concept) and resolving complex performance issues across distributed OLTP/OLAP environments. He delivers practical, production-ready solutions that balance performance, scalability, and simplicity.

---

## Work Experience

### Database / AI Engineer — 에이플랫폼 (Agile Platform), Seoul

**Dec 2023 – Present** | IT Services & Consulting (SingleStore-focused)

- Leads online and offline database migrations.
- Diagnoses and resolves SingleStore performance bottlenecks.
- Designs Kafka-based data pipelines to simulate real customer workloads.
- Optimizes SingleStore for vector data storage and high-performance retrieval.
- Benchmarks vector index accuracy and performance (HNSW, IVF, etc.).
- Builds semantic search systems and RAG-based AI pipelines.
- Provides technical support for AI search and vector features.
- Produces clear technical documentation for engineers and business stakeholders.

### Data Analyst / Engineer — 별따러가자 (Starpickers), Seoul

**Sept 2021 – Nov 2023** | IT Telematics Company

- Designed and implemented end-to-end ETL pipelines.
- Conducted data quality validation to ensure accuracy and integrity.
- Configured real-time workflow monitoring and alerting in Apache Airflow.
- Processed and analyzed 1M+ rows of data daily from 300+ users.
- Developed algorithms to detect driving maneuvers (U-turns, sharp turns, overtaking, lane changes).
- Contributed to a driving behavior scoring system for usage-based insurance (UBI).
- Built an SVM model achieving 92% accuracy to classify road vs. sidewalk driving.
- Developed and maintained KPI monitoring dashboards.

---

## Skills

### Programming & APIs
Python, SQL, Bash, JavaScript, REST API Development, API Integration

### Data Engineering & Systems
Apache Kafka, Apache Airflow, dbt, Linux, Distributed Systems, OLAP/OLTP Architecture

### Databases
SingleStore, MySQL, MongoDB, Firebase

### Cloud
AWS (EC2), Oracle OCI

### Data Visualization
Tableau, Streamlit, Plotly

### AI & Machine Learning
Machine Learning, TensorFlow, LLMs, RAG, Semantic Search, Vector Databases, AI Pipelines & Agents

### Soft Skills
Technical Writing, Strong Analytical & Problem-Solving Ability, Growth Mindset

---

## Education

| Degree | Institution | GPA | Graduated |
|---|---|---|---|
| MBA | Chung-Ang University, Seoul | 4.16 / 4.5 | Aug 2021 |
| BSc (Hons) in Economics | Don State Technical University, Russia | 4.83 / 5.0 | Jul 2018 |

### Professional Certification
- Google Career Certificate in Advanced Data Analytics (2023)

---

## Awards & Certificates

### Certificates
- SingleStore Certified Developer (2024)
- Junction Asia 2022 Hackathon Participant
- Data Analytics Certificate (2020)

### Awards
- Government of Korea Scholar (GKS), 2018
- Nigeria/Russia Bilateral Scholarship, 2013

---

## Technical Writing

Michael authors technical guides and tutorials on his Notion blog. Below is a summary of each article. For full details, code samples, and step-by-step walkthroughs, visit the linked pages.

### Text-to-SQL with LangChain
**Link:** https://www.notion.so/Text-to-SQL-with-LangChain-2aad45e50c3281e59fc0c73328c1a658
Demonstrates how to convert natural language queries into SQL executable on SingleStoreDB using OpenAI's ChatGPT API and LangChain. Covers database connection via SQLAlchemy, dynamic table selection with Pydantic extraction chains, dynamic few-shot example selection using semantic similarity (embeddings stored in SingleStore), ChatPromptTemplate construction, and a full query-generation-to-answer pipeline with conversation memory using LangChain's `create_sql_query_chain`, `QuerySQLDataBaseTool`, and `RunnablePassthrough`.

### Vector DB Semantic Search (Tutorial)
**Link:** https://www.notion.so/Vector-DB-Semantic-Search-Tutorial-2aad45e50c3281ad8845d00e05de7304
A hands-on tutorial covering vector, fulltext, and hybrid search in SingleStore using 1.1M+ Korean Wikipedia embeddings (768 dimensions, Cohere model). Topics include KNN search (exact, no index), ANN search with vector indexes (IVF_FLAT, IVF_PQ, IVF_PQFS, HNSW_FLAT, HNSW_PQ), vector index caching behavior and memory management, Fulltext v2 search using MATCH and BM25 scoring, and hybrid search combining vector + fulltext scores. Includes performance benchmarks showing the impact of index caching on query latency.

### Vector Index Concepts (ANN)
**Link:** https://www.notion.so/Vector-Index-ANN-2bdd45e50c32802b9a72f535592e82fa
An educational article explaining vector index internals in SingleStore. Covers IVF (Inverted File) with nlist/nprobe parameters and centroid-based partitioning, HNSW (Hierarchical Navigable Small World) with its multi-layer graph structure, Product Quantization (PQ) for vector compression and memory reduction, and SingleStore's on-disk columnstore LSM design for per-segment vector indexes with background merging.

### RAG — KNN + ANN + Hybrid Search with LangChain (User Guide)
**Link:** https://www.notion.so/RAG-KNN-ANN-Hybrid-Search-With-LangChain-User-Guide-with-Python-2aad45e50c3281fcb771d16bb6c39065
A complete RAG demo with four retrieval approaches using SingleStore as the vector store: (1) LangChain RetrievalQA with ANN vector search, (2) RetrievalQA with `as_retriever()`, (3) pure SingleStore SQL for hybrid search, and (4) a custom LangChain retriever using SingleStore SQL for hybrid search. Uses Llama 2 (7B, GGUF quantized) as the local LLM. Includes setup instructions, config, and full output examples for each approach.

### dbt + SingleStore Pipeline + Kafka CDC
**Link:** https://www.notion.so/dbt-SingleStore-Pipeline-Kafka-CDC-2aad45e50c3281e98198d7bc44663c7a
End-to-end guide for CDC (Change Data Capture) from MySQL to SingleStore using Debezium, Kafka, SingleStore Pipelines, and dbt. Covers MySQL binlog-based CDC via Debezium connector, Kafka topic creation and connector configuration, SingleStore Pipeline ingestion into a staging table, and dbt incremental models with `delete+insert` strategy to apply insert/update/delete events. Implements soft deletes using an `is_deleted` flag column instead of hard deletes.

### Data Build Tool (dbt) + SingleStore DB
**Link:** https://www.notion.so/Data-Build-Tool-dbt-SingleStore-DB-2bdd45e50c3280b094c9c0e38a6d7b65
A setup and usage guide for dbt with SingleStore. Covers dbt-singlestore adapter installation and connection configuration, project initialization and debug verification, basic table materialization from JSON data, and incremental strategy (`delete+insert`) with timestamp-based change detection. Includes internal behavior analysis showing how dbt creates temporary tables, loads transformed data, and renames to the final target.

### Kafka Cluster Setup Guide
**Link:** https://www.notion.so/Kafka-2bdd45e50c3280c7b763f5bfa9a70629
A reference guide for setting up a single-node Kafka cluster. Covers Java runtime prerequisites, firewall configuration, Zookeeper and Kafka broker installation from the Apache archive, data/log directory configuration, and a comprehensive command reference for topic management, producer/consumer operations, and consumer group administration.
