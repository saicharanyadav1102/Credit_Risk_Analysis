# PaySprint: FinTech Digital Lending Platform
## From Raw Data to Product Idea

---

## SLIDE 01: Title & Team
**Company:** PaySprint (FinTech - Digital Lending)
**Team:** Group 4
**Roles:**
- **Data Cleaner:** Fixed categorical inconsistencies, duplicate handling, numeric bound constraints.
- **Analyst:** Built charts, quantified dropout, default, and rejection metrics.
- **Product Thinker:** Identified the underserved "Gig Worker" segment & proposed alternative scoring.
- **Storyteller:** Created this presentation and tied insights to product-market fit.

---

## SLIDE 02: The Dataset in One Slide
- **Scope:** 7,095 rows and 31 columns covering 15 months of loan applications.
- **What one row represents:** A single loan application from a user (approved or rejected).
- **Data Origin:** PaySprint's core lending & origination system, including KYC, underwriting, and loan repayment databases.

---

## SLIDE 03: Data Quality Report
**What was broken & How we fixed it:**
- **Duplicates:** Found and removed 95 exact duplicate rows.
- **Categorical Variants:** `employment_type` had 12 spellings (e.g., 'Gig-Worker', 'gig worker'). Consolidated into standard types. Similar fixes applied to `product_type` and `kyc_status`.
- **Logic Errors:** 50 rows had `approved_amount` > `requested_amount`. Capped the approved amount to the requested amount.
- **Invalid Metrics:** 35 rows with credit score >900 or <300. 30 rows with age >80 or <18. Set to `NaN` as they are invalid.
- **Structural Nulls:** `approved_amount_inr` (3635 blanks) is missing because the application was rejected. `days_past_due` (4104 blanks) is missing because money was never disbursed. `rejection_reason` (4654 blanks) missing because they were approved. We did not zero-fill these as doing so would falsely skew means and suggest loans were approved for $0 or paid on time.

---

## SLIDE 04: The Problem We Found
**Problem:** Massive over-rejection of the "Gig Worker" segment despite a viable demand.
- **Rejection Rates:** Gig workers face a 40.3% rejection rate compared to Salaried workers (29.5%). 
- **Top Rejection Reasons:** High existing obligations, Low credit scores, and Thin credit files.
- **Defaults:** When disbursed, Gig workers default at 5.2%. While higher than Salaried (3.7%), it represents an acceptable risk given their average requested ticket size of ~149,845 INR. We are leaving massive potential revenue on the table because traditional credit bureaus fail to evaluate gig workers accurately.

---

## SLIDE 05: What is the Product?
**Name:** SprintScore for Gig Workers
**Description:** An alternative credit-scoring engine integrated into the underwriting workflow that evaluates thin-file and gig economy workers using alternative digital markers (e.g., app session engagement, device OS, consistent micro-income patterns) instead of relying solely on traditional bureau scores.
**Type:** Feature/Engine integrated into the existing PaySprint approval funnel.

---

## SLIDE 06: What is it used for? (User Journey)
1. **Application:** A gig worker (e.g., a delivery partner) applies for a 150k INR personal loan on the PaySprint App.
2. **Traditional Underwriting:** The bureau returns a "Thin File" or score of 620. Previously, this was a hard reject.
3. **SprintScore Engine:** The system routes the application to SprintScore. The engine analyzes their consistent device usage, KYC success, and predictable monthly income variations.
4. **Outcome:** The user is approved for a smaller, right-sized "starter" credit line of 50k INR with terms they can afford, building their credit history with PaySprint.

---

## SLIDE 07: Target Customer
- **Demographics:** Gig workers and Self-employed individuals, typically 22-35 years old.
- **City Tier:** Heavily concentrated in Tier 2 and Tier 3 cities where traditional banking footprints are small.
- **Data Footprint:** 1,146 Gig Workers and 1,798 Self-Employed individuals in the current file (~42% of the applicant base). Nearly a third of these were rejected due to poor traditional credit metrics.

---

## SLIDE 08: Product-Market Fit
**Evidence of Demand:**
- 42% of our inbound applications are from Gig or Self-employed workers, indicating they *want* PaySprint's products. 
- Over 183 Gig Worker applications in the sample were rejected *solely* for thin files or low credit scores, representing immediate lost market share.
- **Falsifiable Test:** If we run a 5% shadow approval experiment using SprintScore and the default rate exceeds 8%, the PMF thesis is invalid.

---

## SLIDE 09: Market Size & Share
- **TAM:** The Indian digital lending market is projected to reach $350 Billion by 2024 (Source: Experian/BCC).
- **SAM:** The blue-collar and gig worker credit segment is heavily underserved.
- **Competitors:** KreditBee, Navi, Paytm Postpaid. 
- **Differentiation:** Most competitors rely heavily on CIBIL. By evaluating alternative data, PaySprint captures a "first-mover" advantage on creditworthy thin-file customers before competitors do.

---

## SLIDE 10: Adoption Plan
**The first 1,000 users:**
- We don't need external marketing. We have thousands of previously rejected applicants in our database.
- **Launch strategy:** Send a "You've been pre-approved for a Starter Loan!" push notification to 3,000 gig workers who were rejected in the last 6 months for "Thin credit file".
- At a conservative 33% conversion rate, this acquires our first 1,000 users at $0 Customer Acquisition Cost (CAC).

---

## SLIDE 11: Integrated or Standalone?
**Decision: Integrated Engine**
1. *Does it need existing user data to work?* Yes, it needs the app session, KYC, and application data.
2. *Would a new user download it on its own?* No, borrowers want a loan, not a scoring tool.
3. *Does it serve a different buyer?* Not initially.
*Future upside:* If SprintScore proves highly effective, PaySprint can package the engine as a B2B API (Standalone Infrastructure) sold to other lenders.

---

## SLIDE 12: Pricing & Business Model
**Business Model:** Risk-adjusted Interest Pricing.
- Because alternative scoring carries marginally higher risk initially, these loans will be priced 200-300 basis points higher than prime salaried loans.
- The product acts as an on-ramp. Once the gig worker successfully repays their first 3 EMIs, they "graduate" to standard PaySprint rates, fostering loyalty and driving repeat borrowing.

---

## SLIDE 13: Success Metrics, Risks & Fairness
**Success Metrics:**
1. **Approval Rate for Gig Workers:** Target increase from 59% to 75%.
2. **First-EMI Default Rate on new segment:** Target < 6%.
3. **Disbursal TAT:** Target under 12 hours (automated alternative approval instead of manual review).

**Risks & Mitigations:**
- *Risk:* Alternative data models overfit and approve bad loans. *Mitigation:* Roll out progressively (5% of traffic) and cap the first loan amount at 25,000 INR.

**Fairness (Mandatory):**
- *Concern:* Alternative data (like device OS or app sessions) could proxy for income/gender/tier and inadvertently penalize Tier 3 female applicants who share phones.
- *Action:* We will run a monthly demographic parity check on the SprintScore approvals. If approval rates diverge by more than 15% across gender or city tier, the model weights will be manually audited and adjusted.
