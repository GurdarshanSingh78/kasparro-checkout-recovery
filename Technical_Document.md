# Technical Document: Architecture & Failure Handling

## 1. System Architecture
The MVP is built using Python and Streamlit, simulating both the client-side checkout UI and the backend agent logic.
* **Frontend State Machine:** Streamlit manages session states (`Active`, `Friction Detected`, `Recovered`, `Completed`) to simulate a live checkout lifecycle.
* **Event Listener Layer:** Captures simulated telemetry (Price Hesitation triggers, Shipping Confusion triggers).
* **Agent Engine:** A Python backend that compiles the user context (cart value, shipping fees, friction type) and dispatches a structured prompt to the OpenAI API (gpt-4o-mini) to generate a contextual intervention.

## 2. Key Implementation Decisions
* **Stateless Generation:** The LLM does not maintain a long, token-heavy conversation history. It receives a single, highly structured payload containing the exact state of the checkout and outputs a single intervention. This ensures low latency.
* **Clear Event Logging:** We built a live telemetry feed into the UI so merchants (and judges) can see exactly when the system transitions from deterministic monitoring to probabilistic AI generation.

## 3. The AI / Deterministic Boundary
* **Deterministic:** Session monitoring, friction trigger detection, cart math, and the application of discounts.
* **AI (LLM):** Compiling the context into a natural, empathetic, and persuasive message to the user. 
* **Why this line?** We cannot trust an LLM to accurately calculate cart totals or manage payment states (hallucination risk). We *can* trust it to handle the nuanced, human-facing communication of a deterministic discount.

## 4. Failure Handling & Degradation (Crucial)
Ecommerce infrastructure must have zero downtime. We engineered strict degradation protocols:
* **LLM Latency/Timeout:** If the OpenAI API takes too long or returns an error, the system traps the exception.
* **Graceful Degradation:** The system immediately falls back to a deterministic rules engine. If it detects "Price Hesitation" but the LLM is down, it bypasses the API and injects a hardcoded static string: *"Use code RECOVER10 at checkout right now for an immediate 10% off."*
* **Impact:** The Shopify API/LLM can completely crash, and the checkout recovery system will still function via static fallbacks. The user experience degrades from "Hyper-personalized" to "Standard," but it never breaks.