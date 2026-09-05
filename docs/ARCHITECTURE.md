# RecoverAI Architecture

```mermaid
flowchart TD
    A[Failed Payment / Abandoned Checkout] --> B[Payment Service]

    B --> C[Recovery Agent]

    C --> D[Risk Scoring]
    C --> E[Failure Diagnosis]
    C --> F[Recovery Action Selection]

    D --> G[Policy Engine]
    E --> G
    F --> G

    G -->|Allowed| H[Recovery Execution]
    G -->|Blocked| I[Manual Escalation]

    H --> J[Measured Recovery Outcome]
    J --> K[Audit Trail]

    I --> K

    K --> L[Recovery Dashboard]
    G --> L
    C --> L