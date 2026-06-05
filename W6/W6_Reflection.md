# Week 6 Reflection — Probabilistic Models & Bayesian Inference
**Swopnim Ghimire | Fusemachines AI Fellowship**

---

## Concrete Example: The VP's New 40-Customer Segment (Part 1 / Part 2)

**The decision:** Should the VP of Retention immediately allocate budget to intervene with the 40 customers enrolled in the new contract tier?

**What the MLE says:** Churn rate = 15/40 = 37.5%. Based purely on this, the VP might say "yes, intervene — that's a high churn rate."

**What the full Bayesian answer says:** The posterior is Beta(17, 30) under our weakly informative Beta(2,5) prior. The 94% HDI is **[0.231, 0.493]** — a 26-percentage-point range. P(θ > 0.25) = ~0.92, which barely clears a 90% decision threshold. At n=6 customers the threshold was also crossed — but with n=6, the HDI spans ~0.60.

**The mechanism — Uncertainty Quantification:** The MLE 0.375 is a point estimate with no margin of error. A frequentist 95% CI at n=40 also crosses 0.25 at n=6, but it only states "94% of repeated experiments would produce intervals covering the true θ." The Bayesian HDI makes a direct probability statement: *there is a 94% probability the true churn rate lies between 23% and 49%.* This range is wide enough that "37.5%" is not an actionable number — the churn rate could plausibly be as low as 23% (moderate, not urgent) or as high as 49% (critical). The MLE would have led the VP to a single-number decision; the posterior HDI correctly forces the VP to acknowledge that **with only 40 observations, we do not know enough to act confidently**, and that 43 more customers should be observed before crossing a reliable decision threshold (per the sequential updating analysis in Part 2).

**Why this matters:** Allocating retention budget for a segment where θ could be anywhere from 0.23 to 0.49 risks either over-spending on a segment that's performing fine (lower bound) or under-spending on one that's critically leaking (upper bound). The Bayesian HDI quantifies this risk explicitly — the MLE hides it.

---

*"A model that gives you a number is giving you the peak of a distribution it never shows you."*
