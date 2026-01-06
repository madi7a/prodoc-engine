# 📄 ProDoc Engine: Intelligent Document Generation System

> **Technical Assessment Submission for Inuvaira – Software Engineer Position**
> **Author:** Madiha Saeid

---

## 🚀 Overview

**ProDoc Engine** is a scalable, agentic document generation platform designed to eliminate manual corporate reporting. It cleanly decouples **Intelligence** (Generative AI) from **Presentation** (Deterministic Rendering), transforming raw, unstructured user notes into pixel‑perfect, corporate‑compliant PDF reports.

Unlike traditional template fillers, ProDoc Engine uses an **Agentic Workflow** to first understand *intent and context* before structuring content. The system dynamically switches between:

* **Consultant Mode** – creative, high‑level drafting for abstract topics
* **Editor Mode** – strict restructuring of provided data with zero hallucination

---

## 📺 Video Demo & Walkthrough

🎥 **Technical Deep‑Dive & Live Demo**
👉 *https://drive.google.com/file/d/1M8aps7cb4daGuaejkDbeVuK3my8DQ3kX/view?usp=drivesdk*

---

## 🏗️ System Architecture

The platform follows a **decoupled microservices architecture**, ensuring that AI reasoning and document rendering remain independently scalable.

```mermaid
graph LR
    A[React Frontend] -- JSON Request --> B[FastAPI Backend]
    B -- Prompt Engineering --> C[AI Agent (Qwen 2.5)]
    C -- Structured JSON --> B
    B -- Data Injection --> D[Jinja2 Templates]
    D -- HTML + CSS Paged Media --> E[WeasyPrint Engine]
    E -- PDF Binary --> A
```

### Key Architectural Decisions

1. **FastAPI (Async Backend)**
   Chosen for its high‑performance asynchronous model, enabling non‑blocking AI inference calls and efficient request handling under load.

2. **Logic Routing Layer ("The Brain")**
   A custom intent‑detection layer determines how the LLM should behave:

   * *Creator Mode:* Acts as a consultant for abstract or strategic prompts
   * *Editor Mode:* Acts as a strict editor, restructuring only supplied data

3. **WeasyPrint Rendering Engine**
   Uses **CSS Paged Media** (`@page`) instead of heavyweight headless browsers (e.g., Puppeteer), allowing precise print layouts with minimal server overhead.

4. **Resilient JSON Parsing**
   A custom `repair_json` utility sanitizes and repairs malformed LLM outputs, ensuring pipeline stability even under imperfect generations.

---

## 🛠️ Tech Stack

### Backend

* **Python 3.10+**
* **FastAPI** – API orchestration & async handling
* **Hugging Face Inference Client** – LLM access (`Qwen/Qwen2.5-7B-Instruct`)
* **Jinja2** – Deterministic HTML templating
* **WeasyPrint** – HTML‑to‑PDF rendering
* **Pydantic** – Data validation & schema enforcement

### Frontend

* **React.js** – Component‑based UI
* **Axios** – API communication
* **CSS Modules** – Scoped, maintainable styling

---

## ⚡ Core Features

* **Dual‑Mode Intelligence** – Automatic switching between drafting and strict editing
* **Dynamic Author Extraction** – NLP‑based detection of author names from raw notes (fallback: *AI Consultant*)
* **Smart Tables** – Automatic conversion of lists, metrics, and comparisons into styled tables
* **Corporate Branding Enforcement** – Consistent typography, spacing, and color schemes via CSS
* **Zero‑Hallucination Guardrails** – Strict prompts prevent fabricated data in Editor Mode

---

## 🔧 Installation & Setup

### Prerequisites

* Python **3.10+**
* Node.js & npm
* Hugging Face API Token

---


## 🔮 Strategic Roadmap (Scalability Plan)

To evolve this PoC into a production‑grade system capable of supporting **1,000+ concurrent users**, the following roadmap is proposed:

1. **Event‑Driven Processing**
   Offload PDF generation to background workers using **Redis + Celery** to avoid HTTP blocking.

2. **Serverless Rendering**
   Deploy WeasyPrint workloads on **AWS Lambda** for elastic CPU scaling.

3. **Adapter Pattern (Sprint‑2 Priority)**
   Abstract the rendering layer to support **PDF, DOCX, and HTML** exports via plug‑and‑play adapters.

4. **Real‑Time Collaboration**
   Introduce **WebSockets** and **CRDTs** for multi‑user, real‑time document editing.

---

## 📂 Project Structure

```text
prodoc-engine/
├── backend/
│   ├── content_generator.py   # AI logic & prompt engineering
│   ├── report_generator.py    # Jinja2 + WeasyPrint rendering
│   ├── server.py              # FastAPI endpoints
│   └── output/                # Generated PDFs
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   └── App.js             # Main application logic
│
└── README.md
```

---

✅ **Status:** Production‑ready Proof of Concept
📌 **Purpose:** Technical assessment demonstrating system design, AI orchestration, and scalable backend engineering

