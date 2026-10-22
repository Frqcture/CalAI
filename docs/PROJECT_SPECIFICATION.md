# CalAI Project Specification

## Project Overview

**CalAI** is an AI-powered calibration and diagnostics intelligence platform for automotive engineers.

It is designed to ingest engineering artifacts and provide traceable, engineering-focused answers through natural language interaction.

## Vision

CalAI is a self-hosted engineering knowledge platform for understanding and analyzing:

- eHandbook (`.ehb`) files
- Calibration datasets
- Signal databases
- Diagnostic architectures
- MF4 measurement files
- Control strategy documentation
- Requirements documents
- MATLAB exports
- OBD monitor definitions
- Simulink exports
- Engineering PDFs and spreadsheets

## Target Customers

### Primary

- OEM Calibration Engineers
- OBD Engineers
- Diagnostics Engineers
- Controls Engineers
- Validation Engineers
- Development Test Engineers

### Secondary

- Tier 1 Automotive Suppliers
- Engineering Consultancies
- Motorsport Teams
- Universities
- Research Organizations

## Deployment Model

CalAI is designed primarily for **self-hosted** deployment due to proprietary data, strict security requirements, and air-gapped operation needs.

### Container Architecture

- Frontend Container
- Backend API Container
- AI Service Container
- PostgreSQL Container
- Vector Database Container
- License Service Container

### Deployment Methods

- Docker Compose (primary)
- Kubernetes (future option)

### Future Enterprise Options

- On-prem clusters
- Air-gapped installations
- Enterprise Kubernetes deployments

## Core Features

1. **Knowledge Base**
   - Upload: EHB, PDF, DOCX, XLSX, CSV, TXT, JSON, XML, MATLAB exports, signal dictionaries, test specs, requirements.
   - Pipeline: extraction → entity parsing → embeddings → relationship graph → search/RAG storage.

2. **AI Engineering Assistant**
   - Chat interface for engineering QA, diagnostics, signal tracing, calibration discovery, and root-cause analysis.
   - Responses include explanation, confidence, and traceable sources.

3. **Signal Dependency Explorer**
   - Interactive signal graph with traversal, filtering, search, and export.

4. **Diagnostic Explorer**
   - DTC-centric analysis: enable/entry/exit/inhibit conditions, related calibrations, dependencies, and fault trees.

5. **Calibration Explorer**
   - Calibration metadata, relationships, compare/revision/delta workflows, and impact analysis.

6. **MF4 Analysis**
   - Signal extraction, resampling, event/anomaly detection, statistical analysis, and natural-language analysis.

7. **Multi-File Correlation**
   - Cross-run failure condition mining, trend analysis, and repeatability/correlation detection.

8. **Strategy Documentation Generator**
   - Auto-generates strategy descriptions with I/O, failure modes, calibration summaries, and diagnostic interactions.
   - Export: PDF, DOCX, Markdown.

9. **Engineering Wiki**
   - Auto-generated internal engineering knowledge pages connecting monitors, signals, and calibrations.

## AI Architecture

CalAI uses Retrieval-Augmented Generation (RAG):

1. User question
2. Embedding search
3. Relevant engineering chunks
4. Prompt construction
5. AI response with evidence

Benefits:
- Better accuracy
- Reduced hallucinations
- Traceable answers
- Faster response cycles

## Supported AI Models

### Cloud
- OpenAI GPT
- Azure OpenAI

### Local
- Llama
- Mistral
- DeepSeek
- Other OpenAI-compatible APIs

## File Type Roadmap

### Release 1
- PDF, DOCX, TXT, CSV, JSON, XLSX

### Release 2
- MF4, A2L, DBC, MAT

### Release 3
- EHB, SLX, M Files, ARXML

## EHB Flagship Capability

EHB parsing includes:

- Functions
- Signals
- Diagnostics
- Tables
- Hyperlinks
- Images
- Calibration references

Output is a structured engineering relationship graph enabling deep reference queries.

## Technology Stack

### Frontend
- React
- TypeScript
- Next.js
- Material UI

### Backend
- Python
- FastAPI

### AI Layer
- LangChain
- LlamaIndex

### Databases
- PostgreSQL
- Vector option: Qdrant or PostgreSQL + pgvector

### Authentication
- Keycloak with LDAP/AD/SSO/local account support

## Security Requirements

Mandatory:

- Role-based access control
- Audit logging
- TLS encryption
- Encrypted storage
- User permissions
- Project isolation
- Multi-tenant support
- Air-gap compatibility

## Licensing

### Option 1: Offline License Key
Includes company, license ID, expiry, user limit, feature flags, cryptographic signature.

### Option 2: Online Validation
Periodic checks against `license.calai.com` for validity, seats, expiry, and updates.

### Recommended Hybrid
- Monthly online validation
- 90-day offline grace period
- Full offline licensing option for enterprise

## Licensing Tiers

### Community
- 1 user
- Limited features
- Non-commercial

### Professional
- Up to 10 users
- Unlimited projects
- Standard support

### Enterprise
- Unlimited users
- Air-gapped deployment
- Priority support
- Custom branding
- Offline licensing

## Revenue Model

- Professional: **£99 per user/month**
- Enterprise: **£10,000–£50,000 per year** (based on user count, data volume, support, and deployment complexity)

## Minimum Viable Product (v1)

Must-have scope:

- User authentication
- Docker deployment
- Licensing system
- Document upload
- RAG knowledge base
- AI engineering chat
- Signal relationship graph
- EHB parsing

Future scope includes MF4 analytics, DTC explorer, calibration impact analysis, engineering wiki, automated docs, and multi-file correlation.

## Success Criteria

An engineer should be able to:

1. Upload engineering documentation.
2. Ask a plain-English question.
3. Receive a technically accurate answer.
4. Trace the answer to source evidence.
5. Navigate relationships visually.
6. Reduce investigation time significantly.
