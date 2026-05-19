# Build Decision Log

* **May 19: Considered building a full Shopify app. Chose a Streamlit prototype instead.** * *Reasoning:* To maximize our time on the actual product logic (intent detection, prompt engineering, failure handling) rather than fighting with OAuth and boilerplate backend setup. It proves the concept faster.
* **May 19: Chose gpt-4o-mini over gpt-4 or Claude Opus.**
  * *Reasoning:* Speed. In a checkout scenario, an intervention needs to appear instantly. The slight dip in reasoning capabilities is worth the massive reduction in latency.
* **May 19: Implemented strict deterministic fallbacks for the AI agent.**
  * *Reasoning:* If we deploy an agent to a real merchant, it cannot crash the checkout page if the LLM provider has an outage. The static rule-based fallback guarantees the recovery loop stays active.
* **May 19: Decided to simulate friction via explicit buttons rather than complex timers.**
  * *Reasoning:* For a 3-minute hackathon demo video, waiting 60 seconds for a timer to trigger an event is bad UX. Explicit buttons allow us to rapidly demonstrate the state changes and system logic.
  