\# SecureFlow 🔐



\*\*A Security-Focused Transaction Risk Assessment Platform\*\*



SecureFlow is a portfolio project designed to simulate how a financial transaction platform can evaluate transaction risk and make automated decisions based on configurable risk rules.



The project is part of my hands-on journey in \*\*Cloud Engineering, DevOps, DevSecOps, and AI Security Engineering\*\*, with a focus on building secure, observable, and reliable systems.



> \*\*Disclaimer:\*\* SecureFlow is a demonstration project. It does not connect to real banking systems, process real financial transactions, or provide production-grade fraud detection. Use fictional data only.



\## 🎯 The Problem



Financial applications need ways to identify potentially risky transactions before approving them.



SecureFlow demonstrates a basic approach to this problem by evaluating submitted transactions and assigning one of three outcomes:



\* \*\*ALLOW\*\* — The transaction falls within the configured low-risk range.

\* \*\*REVIEW\*\* — The transaction meets the threshold for additional investigation.

\* \*\*BLOCK\*\* — The transaction meets the configured high-risk blocking criteria.



The goal is to build a practical foundation for exploring transaction risk assessment, backend security, automation, infrastructure management, and monitoring.



\## 🏗️ Architecture



The current application consists of three main components:



\* \*\*Frontend:\*\* A web dashboard for interacting with the application and submitting transactions.

\* \*\*Backend API:\*\* A FastAPI application that handles authentication, transaction requests, and risk assessment.

\* \*\*Database:\*\* PostgreSQL for storing application data.



Nginx serves the frontend and proxies API requests to the backend. Docker Compose runs the application services together.



```text

&#x20;                User

&#x20;                  |

&#x20;                  v

&#x20;         Frontend Dashboard

&#x20;              (Nginx)

&#x20;                  |

&#x20;                  v

&#x20;           FastAPI Backend

&#x20;            /           \\

&#x20;           v             v

&#x20;    Risk Assessment   Authentication

&#x20;           |

&#x20;           v

&#x20;       PostgreSQL

```



\## 🛠️ Technology Stack



| Category                   | Technologies             |

| -------------------------- | ------------------------ |

| Backend                    | Python, FastAPI          |

| Database                   | PostgreSQL               |

| ORM                        | SQLAlchemy               |

| Database migrations        | Alembic                  |

| Authentication             | JWT-based authentication |

| Password security          | Argon2 password hashing  |

| Frontend                   | HTML, CSS, JavaScript    |

| Web server / reverse proxy | Nginx                    |

| Containerization           | Docker                   |

| Local orchestration        | Docker Compose           |

| Version control            | Git and GitHub           |



Terraform, Kubernetes, CI/CD, GitOps, security scanning, and observability are planned areas for future development.



\## ⚙️ Current Features



\### 1. Authentication



\* User registration and login endpoints.

\* Password hashing.

\* JWT-based authentication.

\* Protected transaction endpoints.

\* Role and account-status checks for transaction submission.



\### 2. Transaction Management



\* Submit simulated financial transactions.

\* Associate transactions with the authenticated user.

\* Retrieve transaction history subject to the implemented access controls.

\* Store transaction information in PostgreSQL.



\### 3. Risk Assessment Engine



The risk engine evaluates transactions using configurable thresholds and supports additional risk signals.



Current amount-based demonstration thresholds:



| Transaction Amount         | Expected Decision | Risk Level |

| -------------------------- | ----------------- | ---------- |

| Below ₦150,000             | ALLOW             | LOW        |

| ₦150,000 to below ₦500,000 | REVIEW            | MEDIUM     |

| ₦500,000 and above         | BLOCK             | HIGH       |



These are demonstration thresholds, not validated financial risk policies.



The risk engine also supports scoring additional signals, including unusually large transactions relative to a user's average, new devices, new beneficiaries, unusual locations, failed login attempts, and unusual transaction times.



Not all these additional signals are currently integrated into the transaction submission workflow.



\### 4. Risk Assessment Records



The backend creates a risk assessment containing the risk score, decision, risk level, and explanatory reasons associated with a transaction.



\### 5. Containerized Development Environment



Docker Compose runs the frontend, backend, and PostgreSQL database as separate services.



This provides a foundation for developing, testing, and later deploying the application using more advanced infrastructure and automation practices.



\## 🚀 Getting Started



\### Prerequisites



Install the following:



\* Git

\* Docker Desktop

\* Docker Compose



\### 1. Clone the repository



```bash

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>

cd secureflow

```



Replace `<YOUR\_GITHUB\_REPOSITORY\_URL>` with your actual repository URL.



\### 2. Configure environment variables



Create a `.env` file in the project root.



Configure the environment variables required by your Compose configuration, including:



```dotenv

POSTGRES\_USER=secureflow\_user

POSTGRES\_PASSWORD=REPLACE\_WITH\_A\_STRONG\_UNIQUE\_PASSWORD

POSTGRES\_DB=secureflow

POSTGRES\_PORT=5433



DATABASE\_URL=REPLACE\_WITH\_YOUR\_LOCAL\_DATABASE\_CONNECTION\_STRING



JWT\_SECRET\_KEY=REPLACE\_WITH\_A\_STRONG\_RANDOM\_SECRET

JWT\_ACCESS\_TOKEN\_EXPIRE\_MINUTES=15

```



Use unique local development credentials and a strong, randomly generated JWT secret. Ensure the database connection string matches your local configuration.



\*\*Never commit your actual `.env` file, database passwords, JWT secrets, access tokens, or other credentials to GitHub.\*\*



\### 3. Build and start the application



From the project root, run:



```bash

docker compose up -d --build

```



Check the running services:



```bash

docker compose ps

```



Check the backend logs:



```bash

docker compose logs --tail=50 backend

```



\### 4. Open the application



\* \*\*Dashboard:\*\* http://localhost:8081

\* \*\*API documentation:\*\* http://localhost:8081/api/docs



The application is configured for local development. It is not yet a production deployment.



\## 🧪 Testing the Risk Engine



The risk engine can be tested directly inside the backend container:



```bash

docker compose exec backend python -c "from decimal import Decimal; from app.services.risk\_engine import assess\_transaction\_risk; amounts = \[Decimal('5000'), Decimal('150000'), Decimal('600000')]; \[print({'amount': str(a), \*\*assess\_transaction\_risk(amount=a)}) for a in amounts]"

```



Expected decisions:



\* ₦5,000 → `ALLOW`

\* ₦150,000 → `REVIEW`

\* ₦600,000 → `BLOCK`



These tests verify the configured amount thresholds. They do not establish the accuracy of the system against real-world fraud.



\## 🔒 Security Considerations



Security is a core design consideration for SecureFlow.



Current measures include:



\* Password hashing.

\* JWT-based authentication.

\* Protected API endpoints.

\* Transaction ownership checks.

\* Role-based restrictions on transaction submission.

\* Environment-based configuration for sensitive settings.

\* A non-root user in the backend container.

\* A frontend service bound to the local host interface.

\* Separation of frontend, backend, and database services.



Further security work is planned, including automated security testing, dependency and secret scanning, hardened deployment configurations, improved auditability, and more comprehensive authorization tests.



\## 🗺️ Roadmap



SecureFlow is an evolving project. Planned improvements include:



\* \[x] Build the initial FastAPI backend.

\* \[x] Integrate PostgreSQL.

\* \[x] Implement registration and authentication endpoints.

\* \[x] Build the initial transaction risk assessment engine.

\* \[x] Containerize the frontend and backend.

\* \[x] Run the application with Docker Compose.

\* \[x] Validate the basic amount-based risk decisions through the application.

\* \[ ] Improve dashboard risk scores, decisions, and explanatory reasons.

\* \[ ] Expand automated tests for authentication, authorization, and transaction processing.

\* \[ ] Verify transaction and risk assessment persistence through database queries.

\* \[ ] Improve security logging and audit trails.

\* \[ ] Add CI/CD automation and security scanning.

\* \[ ] Provision infrastructure with Terraform.

\* \[ ] Explore Kubernetes deployment and Argo CD GitOps workflows.

\* \[ ] Add Prometheus and Grafana monitoring.

\* \[ ] Explore additional cloud security and AI security controls.

\* \[ ] Introduce deployment safeguards and cost controls.



\## 👩🏽‍💻 Project Goals



Through SecureFlow, I am developing practical skills in:



\* Cloud infrastructure and automation.

\* Containerization and application deployment.

\* CI/CD and DevSecOps.

\* Identity and access management.

\* Application and infrastructure security.

\* Observability and incident troubleshooting.

\* AI security engineering principles.



The long-term goal is to evolve SecureFlow into a well-documented, security-focused project that demonstrates how these technologies can work together.



\---



\*\*Status:\*\* Active development

\*\*Project type:\*\* Learning and portfolio project

\*\*Focus:\*\* Cloud Engineering | DevOps | DevSecOps | AI Security Engineering



