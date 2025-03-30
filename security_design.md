# BUSINESS POSTURE

The project aims to develop a healthcare chatbot that can provide preliminary diagnoses and health information to users based on their symptoms.

- Business Priorities and Goals:
    - Provide accessible and convenient initial health guidance to users.
    - Offer a self-service tool for users to understand potential health concerns.
    - Reduce the initial burden on healthcare providers by filtering common queries.

- Business Risks:
    - Misdiagnosis or inaccurate health information leading to incorrect self-treatment or delayed professional medical help.
    - User reliance on the chatbot for serious medical conditions without seeking professional medical advice.
    - Data privacy risks if user input or interaction data is stored or logged without proper security measures.
    - Availability and reliability of the chatbot service, especially during peak usage times.

# SECURITY POSTURE

- Existing Security Controls:
    - security control: The application is currently running in debug mode (`app.run(debug=True)` in `app.py`). This is suitable for development but should be disabled in production. Implemented in `/target/uploads/app.py`.

- Accepted Risks:
    - accepted risk: Lack of authentication and authorization. The application appears to be publicly accessible without any user authentication or role-based access controls.
    - accepted risk: Input validation is not explicitly implemented. The application takes user input from the `msg` parameter in the GET request without sanitization or validation.
    - accepted risk: Cryptography is not used. There is no evidence of encryption for data in transit or at rest.
    - accepted risk: No secure software development lifecycle (SSDLC) is mentioned or implemented in the provided files.
    - accepted risk: Deployment model is not defined, but based on `app.run(debug=True)` it is likely a simple, non-hardened deployment.

- Recommended Security Controls:
    - security control: Implement input validation and sanitization for user input to prevent injection attacks.
    - security control: Disable debug mode in production to prevent information leakage and reduce attack surface.
    - security control: Consider implementing HTTPS to encrypt communication between the user and the chatbot.
    - security control: Define a secure deployment process and environment, potentially using containerization and a hardened server configuration.
    - security control: Implement logging and monitoring to detect and respond to potential security incidents.
    - security control: Establish a basic SSDLC including code reviews and security testing.

- Security Requirements:
    - Authentication: Depending on the sensitivity of the application and data, consider adding user authentication to control access. For the current scope, it might not be strictly necessary but should be evaluated if user data is stored or personalized features are added.
    - Authorization: Not strictly required for the current scope as there are no different user roles. However, if administrative functions are added in the future, authorization will be necessary.
    - Input Validation: Implement robust input validation for all user inputs to prevent injection attacks and ensure data integrity. This is critical for preventing unexpected behavior and potential security vulnerabilities.
    - Cryptography: If any user data or sensitive information is stored or transmitted, implement encryption both in transit (HTTPS) and at rest. For the current scope, if no user data is persistently stored, HTTPS should be considered as a baseline.

# DESIGN

## C4 CONTEXT

```mermaid
flowchart LR
    subgraph Internet
        A[/"Web Browser"/]
    end
    B[/"Healthcare Chatbot"/]
    C[/"CSV Data Files"/]

    A --/"Queries & Receives Responses"/--> B
    B --/"Reads Data"/--> C
    style A fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style B fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style C fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
```

- Context Diagram Elements:
    - - Name: Web Browser
      - Type: Person
      - Description: User interface for patients to interact with the Healthcare Chatbot.
      - Responsibilities: Allows users to input symptoms and receive chatbot responses.
      - Security controls: Implemented by standard web browser security features.

    - - Name: Healthcare Chatbot
      - Type: Software System
      - Description: The Flask application that provides health information based on user input and a decision tree model.
      - Responsibilities: Receives user queries, processes them using the decision tree model, and returns health-related information.
      - Security controls: Input validation (recommended), HTTPS (recommended), secure deployment (recommended).

    - - Name: CSV Data Files
      - Type: Data Store
      - Description: Local file storage for training data, symptom descriptions, severity, and precautions used by the chatbot.
      - Responsibilities: Provides data for the chatbot's decision-making process and information retrieval.
      - Security controls: File system permissions to restrict access to the data files on the server.

## C4 CONTAINER

```mermaid
flowchart LR
    subgraph Internet
        A[/"Web Browser"/]
    end
    B[/"Flask Web Application"/]
    C[/"Chatbot Logic"/]
    D[/"Data Files"/]

    A --/"HTTP Requests & Responses"/--> B
    B --/"Calls Python Functions"/--> C
    C --/"Reads Data"/--> D
    style A fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style B fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style C fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style D fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
```

- Container Diagram Elements:
    - - Name: Flask Web Application
      - Type: Web Application
      - Description: Python Flask application (`app.py`) that handles HTTP requests, serves the user interface, and orchestrates the chatbot logic.
      - Responsibilities: Web server, request handling, response generation, UI rendering, interaction with Chatbot Logic.
      - Security controls: Input validation (implemented in application code), HTTPS (to be configured), web application firewall (optional, depending on deployment environment).

    - - Name: Chatbot Logic
      - Type: Python Module
      - Description: Python modules (`chat_bot.py`, `chat_bot2.py`) containing the decision tree model, data processing, and disease prediction logic.
      - Responsibilities: Disease prediction, symptom analysis, data loading and processing, interaction with data files.
      - Security controls: Code review, dependency scanning (for libraries used like pandas, scikit-learn, etc.), secure coding practices.

    - - Name: Data Files
      - Type: File System
      - Description: CSV files (`Training.csv`, `Testing.csv`, `symptom_Description.csv`, `symptom_precaution.csv`, `symptom_severity.csv` in `Data/` and `MasterData/` directories) storing the chatbot's knowledge base.
      - Responsibilities: Persistent storage of training data, symptom information, and disease descriptions.
      - Security controls: File system permissions, access control to the server hosting the files, data validation during loading by the Chatbot Logic.

## DEPLOYMENT

For a simple deployment, the application can be deployed on a single virtual machine or server. A more robust deployment could involve containerization and cloud services. Let's describe a simple VM deployment.

```mermaid
flowchart LR
    subgraph Virtual Machine
        A[/"Operating System"/]
        B[/"Python Runtime"/]
        C[/"Flask Application"/]
        D[/"Data Files"/]
    end
    E[/"Internet"/]
    F[/"User Browser"/]

    F --/"HTTPS Requests"/--> E --/"Port 443"/--> C
    C --/"Reads Files"/--> D
    C --/"Uses Runtime"/--> B
    B --/"Runs on"/--> A

    style A fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style B fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style C fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style D fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style F fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
```

- Deployment Diagram Elements:
    - - Name: Virtual Machine
      - Type: Infrastructure
      - Description: A virtual server instance running the application.
      - Responsibilities: Provides the execution environment for the application.
      - Security controls: OS hardening, firewall, intrusion detection system (IDS), regular security patching.

    - - Name: Operating System
      - Type: Software
      - Description: Linux or Windows Server operating system.
      - Responsibilities: Provides core system functionalities, resource management.
      - Security controls: OS security configurations, access control lists, security updates.

    - - Name: Python Runtime
      - Type: Software
      - Description: Python interpreter and libraries required to run the Flask application.
      - Responsibilities: Executes the Python code of the Flask application and Chatbot Logic.
      - Security controls: Keeping Python runtime updated with security patches, using virtual environments to isolate dependencies.

    - - Name: Flask Application
      - Type: Software
      - Description: Deployed Flask web application files.
      - Responsibilities: Serves web pages and chatbot functionality.
      - Security controls: Application-level security measures (input validation), secure configuration, regular updates of Flask and dependencies.

    - - Name: Data Files
      - Type: Data
      - Description: CSV data files deployed on the server's file system.
      - Responsibilities: Provides data for the application.
      - Security controls: File system permissions, access control to the VM.

## BUILD

The build process can be simplified for this project. A more robust setup would involve CI/CD pipelines. Let's describe a basic automated build process using GitHub Actions as an example.

```mermaid
flowchart LR
    A[/"Developer"/] --> B[/"Code Commit to GitHub"/]
    B --> C[/"GitHub Actions CI Pipeline"/]
    C --> D{/"Build & Test"/}
    D -- Yes --> E[/"Artifacts (e.g., zip file)"/]
    D -- No --> F[/"Build Failure Notification"/]
    E --> G[/"Deployment to VM"/]
    style A fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style B fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style C fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style D fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style E fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style F fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
    style G fill:#CCEEFF,stroke:#0077BB,stroke-width:2px
```

- Build Process Elements:
    - - Name: Developer
      - Type: Person
      - Description: Software developer working on the project.
      - Responsibilities: Writes code, commits changes to the repository.
      - Security controls: Secure development environment, code review process.

    - - Name: Code Commit to GitHub
      - Type: Action
      - Description: Developer commits and pushes code changes to a GitHub repository.
      - Responsibilities: Version control, triggering the CI pipeline.
      - Security controls: Access control to the GitHub repository, branch protection.

    - - Name: GitHub Actions CI Pipeline
      - Type: Automation
      - Description: Automated CI pipeline defined in GitHub Actions.
      - Responsibilities: Automated build, testing, and potentially deployment.
      - Security controls: Secure pipeline configuration, secret management for credentials, vulnerability scanning of dependencies.

    - - Name: Build & Test
      - Type: Process
      - Description: Steps in the CI pipeline to build the application and run automated tests (if any are implemented).
      - Responsibilities: Compiling code (if needed), running linters and SAST scanners (recommended), executing unit and integration tests (recommended).
      - Security controls: SAST scanning, dependency vulnerability checks, linting, secure build environment.

    - - Name: Artifacts (e.g., zip file)
      - Type: File
      - Description: Build artifacts, such as a zip file containing the application code and data files.
      - Responsibilities: Packaging the application for deployment.
      - Security controls: Artifact signing, secure artifact storage.

    - - Name: Deployment to VM
      - Type: Action
      - Description: Automated or manual deployment of the build artifacts to the target Virtual Machine.
      - Responsibilities: Deploying the application to the runtime environment.
      - Security controls: Secure deployment scripts, access control to the deployment environment, deployment automation to reduce manual errors.

# RISK ASSESSMENT

- Critical Business Processes:
    - Providing health-related information to users through the chatbot.
    - Maintaining the availability and accuracy of the chatbot service.

- Data to Protect and Sensitivity:
    - Training Data (CSV files): Moderately sensitive. Integrity and availability are important for the chatbot's functionality. Confidentiality is less critical unless the data contains PII (which is not indicated in the provided files, but should be verified).
    - User Input (Symptoms): Potentially sensitive if logged or stored. Sensitivity depends on logging practices and data retention policies. If user inputs are logged, they should be treated as potentially Personally Identifiable Information (PII) and protected accordingly.
    - System Logs: Can contain operational and potentially security-relevant information. Should be protected to maintain confidentiality and integrity.

# QUESTIONS & ASSUMPTIONS

- BUSINESS POSTURE:
    - Question: What is the intended user base for this chatbot (general public, specific demographic)?
    - Assumption: The chatbot is intended for general public use for initial health information seeking.
    - Question: Are there any specific regulatory compliance requirements (e.g., HIPAA, GDPR) depending on the target users and data handling?
    - Assumption: For this initial version, regulatory compliance is not a primary focus, but data privacy best practices should be considered.
    - Question: What is the acceptable level of accuracy and reliability for the chatbot's responses?
    - Assumption: The chatbot is expected to provide reasonably accurate initial guidance but is not a substitute for professional medical advice.

- SECURITY POSTURE:
    - Question: Are there any existing organizational security policies or standards that this project needs to adhere to?
    - Assumption: No specific organizational security policies are provided, so general security best practices are assumed.
    - Question: What is the organization's risk tolerance for this project?
    - Assumption: A moderate risk tolerance is assumed for this initial phase, with a focus on addressing high-priority security risks.
    - Question: Is there any plan to log user interactions or store user data?
    - Assumption: Currently, there is no explicit data storage of user interactions in the provided code. If logging is implemented, security measures for data protection will be required.

- DESIGN:
    - Question: What is the expected scale and performance requirements for the chatbot?
    - Assumption: Initially, a small to medium scale is expected, with performance requirements suitable for a single VM deployment.
    - Question: What is the planned infrastructure for deployment (cloud, on-premise, etc.)?
    - Assumption: A simple VM-based deployment is assumed for this initial design document, but cloud deployment could be considered for scalability and resilience.
    - Question: Are there any specific technology constraints or preferences for the deployment environment?
    - Assumption: No specific technology constraints are mentioned, so a standard Linux-based VM environment with Python and Flask is assumed.