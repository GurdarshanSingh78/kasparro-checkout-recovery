# Product Document: AI-Assisted Checkout Recovery

## 1. The Problem and Why It Matters
Cart abandonment happens in the margins. A user with high intent drops off because shipping costs are slightly too high, or they can't find a valid coupon code. Current solutions (abandoned cart emails) are reactive and asynchronous. They try to bring a cold lead back. We need a synchronous, active intervention system that resolves friction while the user's intent is still hot.

## 2. Target User & Current Experience
* **The Buyer:** High-intent shoppers who experience sudden hesitation at the final checkout step. Currently, their experience is passive: they encounter friction, get frustrated, and leave. 
* **The Merchant:** Shopify store owners losing 60-70% of carts at the final step. Currently, they rely on generic email blasts to recover 3-5% of those lost carts.

## 3. The Core User Journey
1. Buyer adds items to cart and proceeds to checkout.
2. The system monitors behavioral telemetry (time on page, field toggles, coupon failures).
3. The system detects a specific friction archetype (e.g., "Shipping Confusion").
4. An AI agent intervenes in real-time with a hyper-contextual, low-friction remedy (e.g., waiving the specific shipping fee).
5. Buyer accepts the remedy and completes the purchase in the same session.

## 4. Key Product Decisions
* **Real-time over Retrospective:** We chose to build an active session intervention rather than a post-abandonment email generator. Real-time intervention preserves the psychological momentum of the purchase.
* **Targeted Interventions over Generic Chat:** We disabled open-ended chat. The agent only speaks when specific friction thresholds are met, preventing the UI from becoming a distracting toy.

## 5. Scope Decisions (What we chose NOT to build)
* We chose NOT to build a full Shopify App integration for the MVP. Building OAuth flows and database syncing would consume the hackathon timeframe. Instead, we built a highly focused simulation environment to prove the *logic, timing, and recovery mechanics* of the AI agent.

## 6. Tradeoffs
We traded complex behavioral tracking (mouse movements, eye tracking) for simple, deterministic event triggers (button clicks/time delays). This reduces system overhead and makes the MVP highly reliable, though it sacrifices some nuance in intent detection.