# Shopify AI Sales Agent (RAG-Powered)

Turn any Shopify store into an AI sales assistant **in under 10 seconds** — just paste your store URL.

This project ingests a Shopify store, understands its products and business information, and deploys an AI agent that can answer questions, recommend products, manage a cart, and guide users toward checkout — all powered by Retrieval-Augmented Generation (RAG).

---

## What This Does

This system automatically:

- Ingests a Shopify store using **native Shopify endpoints**
- Extracts **products**, **prices**, **availability**, and **descriptions**
- Extracts **business information** (policies, contact info, about pages, FAQs, etc.)
- Chunks and embeds all content into a **vector search index**
- Runs an **agentic AI layer** that:
  - Answers product & business questions
  - Recommends products with confidence scoring
  - Manages a cart (add / remove / view / clear)
  - Maintains conversational context per user session

All of this is driven by **one input**:  
👉 **the Shopify store URL**

---

## Why This Exists

Most ecommerce traffic never reaches checkout because customers ask questions *before* buying:

- “What’s the difference between these two products?”
- “Do you ship to Ireland?”
- “Is this suitable for sensitive skin?”
- “What’s your return policy?”

This project gives Shopify merchants an **always-on AI sales rep** that understands their store as well as a human would — without manual setup, tagging, or training.

---

## Core Features

### ⚡ 10-Second Setup
- Paste a Shopify store URL
- Products and pages are auto-discovered
- No Shopify app install required

### 🧠 Product-Aware AI
- Uses `/products.json` and `/collections.json`
- Structured product embeddings (not scraped HTML)
- Accurate pricing, availability, and descriptions

### 🏢 Business-Aware AI
- Extracts:
  - About pages
  - Policies (shipping, returns, privacy)
  - Contact information
  - FAQ-style content
- Supports footer + homepage link discovery for non-standard pages

### 🔍 RAG-First Architecture
- All content is chunked and embedded
- Queries are answered using **retrieval + reasoning**
- Clear separation between:
  - Product knowledge
  - Business / informational knowledge

### 🛒 Agentic Cart Control
The AI can:
- Add items to cart
- Remove items
- Change quantities
- Show cart state
- Remember recently discussed products

### 🧩 Modular Pipeline
Each stage is isolated and testable:
- Product extraction
- Info page processing
- Chunking
- Embedding
- Querying
- Agent routing

---

## High-Level Architecture
Shopify Store URL
|
v
Ingestion Pipeline
├─ Products (products.json)
├─ Collections
├─ Pages / Policies
└─ Footer & Homepage Links
|
v
Chunking & Embeddings
|
v
Vector Store (per business)
|
v
Agent Layer (LangGraph)
├─ Enquiry
├─ Cart
├─ Payments (stubbed)
└─ Chitchat


---

## API Flow (Simplified)

1. **POST /login**
   - Authenticates user
   - Ensures `business_id` exists

2. **POST /ingest**
   - Input: `{ store_url, business_id }`
   - Extracts products + info pages
   - Builds RAG index
   - Returns `upload_batch_id`

3. **POST /query**
   - Input: `{ business_id, question }`
   - AI answers using store-specific knowledge

---

## Example Use Cases

- Embedded Shopify chat widget
- Telegram / WhatsApp sales assistant
- Internal sales support bot
- Headless commerce AI layer
- Conversational checkout assistant

---

## What This Is *Not*

- ❌ Not a generic chatbot
- ❌ Not scraping random HTML for products
- ❌ Not a single-prompt RAG demo
- ❌ Not Shopify-theme dependent

This is a **store-aware commerce agent**, built around structured data and long-term extensibility.

---

## Tech Stack

- Python
- FastAPI
- MongoDB
- OpenAI embeddings
- LangGraph / LangChain
- httpx
- Shopify native JSON endpoints

---

## Current Status

- ✅ Product ingestion working
- ✅ Business page extraction working
- ✅ Chunking + embeddings working
- ✅ Agent routing working
- ✅ Cart management working
- 🚧 Payments temporarily disabled
- 🚧 Social links extraction (planned)
- 🚧 Telegram / WhatsApp deployment (planned)

---

## Vision

The long-term goal is to make **AI-powered sales assistants a default layer** for ecommerce — where merchants don’t “build bots”, they just **turn one on**.

Paste your Shopify URL.  
Your AI sales agent is live in seconds.