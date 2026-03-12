# Proyecto: Validación de Conectividad y Despliegue de Agentes Vertex AI

## 1. Contexto del Proyecto

Este repositorio es un entorno de pruebas técnico para agentes de IA que serán desplegados en Vertex AI Agent Builder. El objetivo es validar la infraestructura de datos y automatizar el despliegue.

### Estructura del Repositorio

- src/vertex-agent-adk/: Agentes desarrollados con Google Agent Development Kit (ADK). Se gestiona con uv.
  - src/vertex-agent-adk/README.md: Documentación del agente ADK.
- src/vertex-agent-langchain/: Agentes desarrollados con LangChain y modelos Gemini. Se gestiona con uv.
  - src/vertex-agent-langchain/README.md: Documentación del agente LangChain.
- terraform/*: Código/Modulo de Terraform para el aprovisionamiento de recursos.
- terraform/cloudbuild.yaml: Pipeline de Cloud Build para la automatización del despliegue.
- README.md: Documentación general del proyecto.

## 2. Definición de Agentes (Misión de Antigravity)

### [Agente: ADK Specialist]

- Rol: Experto en el framework ADK de Google.
- Instrucciones: Desarrollar tools en Python que utilicen google-adk. Debe implementar la gestión de estado de sesión persistente.
- Objetivo: Crear funciones de validación para Redis (Memorystore Google Valkey) evaluando latencia y conectividad.

### [Agente: LangChain Specialist]

- Rol: Ingeniero de modelos y orquestación.
- Instrucciones: Implementar cadenas de LangChain que expongan funciones (Function Calling) para interactuar con bases de datos.
- Objetivo: Ejecutar pruebas de conexión y consultas de esquema en Cloud SQL.

### [Agente: DevOps Orchestrator]

- Rol: Arquitecto de Infraestructura como Código (IaC).
- Instrucciones: Generar configuraciones de Terraform para Vertex AI Agent Engine y scripts de despliegue para Cloud Builder.
- Objetivo: Automatizar el despliegue de los agentes asegurando que las políticas de red (VPC) permitan el acceso a Redis y SQL.

## 3. Herramientas y Skills Requeridas

El entorno de Antigravity debe operar con las siguientes capacidades:
1. Shell Environment: Acceso a uv para instalar dependencias y ejecutar uv run en subcarpetas.
2. GCP Auth: Capacidad de usar gcloud para verificar permisos de Service Accounts.
3. Database Inspector: Lectura de metadatos de Cloud SQL para la generación de herramientas de LangChain.

## 4. Checklist de Validación

- [ ] Ejecución de ping/auth exitoso hacia Valkey/Redis desde el agente ADK.
- [ ] Prueba de lectura/escritura en Cloud SQL mediante herramientas de LangChain.
- [ ] Verificación de variables de entorno críticas en el archivo .env o Secret Manager.
- [ ] Ejecución de terraform plan sin errores de permisos.

## 5. Reglas de Desarrollo

- Gestión de Librerías: Prohibido usar pip directamente; siempre usar uv.
- Reasoning: Si se utiliza Gemini 3, el código debe estar preparado para manejar y mostrar Thought Signatures.
- Seguridad: No incluir secretos en el código. Utilizar inyección de variables de entorno para las IPs de Redis y Cloud SQL.
- Modularidad: Mantener los agentes de ADK y LangChain aislados en sus respectivas carpetas para facilitar las pruebas unitarias.
