# MeluXina HPC Resource Allocation & Usage Guide

## 1. Contact & Support Procedures

### Single Points of Contact (SPoCs) — University of Luxembourg
Submit new allocation requests, quota increases, and project extension requests to:

- **Dr. Julien Schleich** (Research Scientist – HPC Platform Lead) — [julien.schleich@uni.lu](mailto:julien.schleich@uni.lu)
- **Dr. Matteo Barborini** (Research Scientist – HPC Platform) — [matteo.barborini@uni.lu](mailto:matteo.barborini@uni.lu)

---

### Application Documents Required

To apply for a new resource allocation or an extension on MeluXina, you must complete and submit the following two documents:

1. **UniLu HPC Computer Allocation Request Form** ([Download file here](meluxina-files/LuxProvide_Allocations_Request_Form.docx))
   - Contains project summary, PI/contact details, list of collaborators, description of computational tools/runs, and requested node-hours (CPU, GPU, FPGA, BigMem) and storage.
2. **LuxProvide Terms of Use Agreement** ([Download file here](meluxina-files/LuxProvide_MeluXina_Terms_of_Use.pdf))
   - Must be read, acknowledged, and signed by the Principal Investigator / Project Owner.
   - Note: the comprehensive list of users cannot be added in the file, please ignore that part.

> **Submission Instruction:** Send both completed and signed documents via email directly to **Julien Schleich** ([julien.schleich@uni.lu](mailto:julien.schleich@uni.lu)) and **Matteo Barborini** ([matteo.barborini@uni.lu](mailto:matteo.barborini@uni.lu)).

---

### Request Procedure Breakdown

| Request Type | Responsible Entity | Submission Channel & Requirements |
| :--- | :--- | :--- |
| **New Allocation Applications** | UniLu SPoCs | Email [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu) with **completed Request Form + signed Terms of Use** |
| **Quota Increase Requests** | UniLu SPoCs & LuxProvide Service Desk | Create a ticket  in the [portal](https://servicedesk.lxp.lu/) and request to add [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu) to the ticket |
| **Project Extension Requests** | UniLu SPoCs & LuxProvide Service Desk | Create a ticket  in the [portal](https://servicedesk.lxp.lu/) and request to add [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu) to the ticket. **Attach the completed Request Form + signed Terms of Use**|
| **Quota Decrease Requests** | UniLu SPoCs & LuxProvide Service Desk | Create a ticket  in the [portal](https://servicedesk.lxp.lu/) and request to add [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu) to the ticket |
| **Technical Support / Bugs** | LuxProvide Service Desk | [Portal](https://servicedesk.lxp.lu/) / [servicedesk@lxp.lu](mailto:servicedesk@lxp.lu) |
| **Change User Access to a Project Requests** | LuxProvide Service Desk | [Portal](https://servicedesk.lxp.lu/) / [servicedesk@lxp.lu](mailto:servicedesk@lxp.lu) |

---

## 2. Resource Allocation & Usage Policy

LuxProvide has implemented a resource allocation policy to ensure that shared public computing infrastructure is utilized efficiently and responsibly rather than sitting idle.

### Core User Expectations
- **Active Allocation Usage:** Users are required to monitor their resource consumption continuously. Unused capacity incurs a public financial cost and prevents other researchers from utilizing available resources.
- **Proactive Communication:** Inform SPoCs as early as possible if your project is delayed, paused, or requires less capacity than requested. Early communication prevents automatic corrective measures.

---

### Progressive Monitoring Workflow (New Projects)
```
[Month 1 & 2] ➔ Check Usage
                 ├── Usage > 50% ➔ On Track (No Action)
                 └── Usage ≤ 50% ➔ 1st Warning Issued (SPoC requests plan/blockers)
 
[Month 3]     ➔ Check Usage
                 ├── Usage > 50% ➔ Recovered (No Reduction)
                 └── Usage ≤ 50% ➔ Allocation Reduced by 50% (Coordinated with LuxProvide)
 
[Month 4]     ➔ Check Usage
                 ├── Usage > 50% ➔ Stabilized (Maintains reduced allocation)
                 └── Usage ≤ 50% ➔ Project Closed (Capacity reallocated to other teams)
```
 
### Assessment for Existing Active Projects
* **Historical Benchmark:** Active projects are evaluated against their average consumption over the preceding **3 months**.
* **Capacity Realignment:** Significant gaps between allocated capacity and actual usage trigger adjustments, progressive reductions, or project decommissioning.
 
---
 
## 3. Onboarding & Allocation Schedule
 
* **Onboarding & Extension Dates:** New project creations and extensions are processed on the **1st** or **15th** of each month (or within two business days if falling on a weekend or public holiday).
* **Extension Deadlines:** Extension requests must be submitted to SPoCs **2 months prior** to the project end date to prevent service interruption.
* **Allocation Lifecycles & 2027 Extensions:**
  * Resources are granted via monthly allocations within the project lifecycle.
  * LuxProvide does **not** grant project allocations beyond December automatically.
  * Projects requiring compute resources into **2027** must submit a formal extension request.
* **Allocation Adjustments:**
  * **Decreases:** Implemented immediately upon review.
  * **Increases:** Typically processed within 3 working days, subject to capacity review and approval.
 
---
 
## 4. Reference Pricing & Cost Awareness
 
> **Note on Billing:** Reference pricing is provided strictly to foster awareness of the public investment scale. **These costs are informational and will NEVER be charged or billed to your project or department.**
 
| Resource Type | Reference Rate (100 Node-Hours) | 
| :--- | :--- | 
| **CPU Compute** | ~€350.00 | 
| **GPU Compute** | ~€800.00 | 
| **FPGA Compute** | ~€800.00 | 
| **Large Memory (BigMem)** | ~€1000.00 |
| **Data Storage** | LuxProvide has not released explicit storage reference rates. |
