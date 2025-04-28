# AI Autonomous Business Project

## 1. Introduction

This project aims to build an autonomous AI-managed digital product business. The system will leverage an AI core (analogous to Gemini 2.5 Pro capabilities) to manage the sale and fulfillment of digital productivity templates (e.g., Notion, Canva) through a Shopify store, integrating various services like Stripe, NOWPayments, HubSpot, and Google Analytics with minimal human intervention.

This repository contains the implementation code and related planning documents.

**Development Environment:** Visual Studio Code (VS Code)
**Primary Language:** Python
**Version Control:** Git

Refer to the original `implementation-plan.md` for the full strategic blueprint and detailed phase descriptions. This breakdown focuses on actionable steps for specific components.

## 2. Prerequisites

Before starting development (Phase 1), ensure the following are set up:

**Accounts:**

* Shopify Account (Partner account recommended for development)
* Stripe Account (Start in Test Mode)
* NOWPayments Account
* HubSpot Account (Free CRM minimum)
* Google Account (for Google Analytics & Google Cloud)
* GitHub Account (or other Git provider)
* Access to an LLM API (e.g., Google AI Studio for Gemini API key)

**Software:**

* Visual Studio Code (VS Code): [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Python (Latest stable version, e.g., 3.10+): [https://www.python.org/](https://www.python.org/)
* Git: [https://git-scm.com/](https://git-scm.com/)
* `pip` (Python package installer, usually included with Python)
* A method for managing environment variables (e.g., `.env` file)

**VS Code Extensions (Recommended):**

* Python (Microsoft)
* Pylance (Microsoft)
* GitLens
* Docker (If using containers for deployment)
* Prettier - Code formatter (Optional)
* DotENV (Supports `.env` file syntax highlighting)
* Thunder Client or similar REST client (For testing API endpoints)

## 3. Project Structure Overview

(Refer to the file structure breakdown provided separately for details on directories like `modules/`, `tests/`, etc.)

## 4. Setup Instructions

1.  Clone the repository: `git clone <your-repo-url>`
2.  Navigate to the project directory: `cd ai_autonomous_business`
3.  Create and activate a Python virtual environment:
    ```bash
    python -m venv .venv
    # Activate (Windows PowerShell): .\.venv\Scripts\Activate.ps1
    # Activate (macOS/Linux): source .venv/bin/activate
    ```
4.  Install dependencies: `pip install -r requirements.txt`
5.  Create a `.env` file (copy from `.env.example` if provided) and populate it with your API keys and secrets. **Do not commit `.env` to Git.**
6.  Follow the phase-specific implementation plans (e.g., `PHASE_1_SETUP.md`).

