# MeluXina HPC Resource Allocation & Usage Guide
**University of Luxembourg — High-Performance Computing (HPC) Platform**

 ## ⚠️ Important: Changes for 2027
 The global MeluXina allocation is **full**: it is capped at **170,000 CPU node-hours and 50,000 GPU node-hours per month**. Starting with 2027, resources are allocated through **quarterly project calls**:

* **Existing projects with resources already allocated in 2027 must reapply to the first call** (Q1: 1st January 2027,  **submission to the SPoCs until 15 December 2026**).
* Projects must be submitted to the UniLu SPoCs **at least 2 weeks before the call cutoff date**, and requests **may be resized** to fit the available global allocation.
* Calls are held **for 2027 only**: no project will be allocated resources in 2028.
* Users and PIs **must not contact LuxProvide directly**. Everything goes through the UniLu SPoCs.

---

##  Onboarding & Allocation Schedule

### Quarterly Project Calls (2027)

The global MeluXina allocation is now **full**. It is limited to **170,000 CPU node-hours and 50,000 GPU node-hours per month**, shared across all projects. Out of fairness to the different PIs, resources are allocated through **quarterly project calls**:

* Projects must be submitted to the UniLu SPoCs **2 weeks before the call cutoff date**.
* Projects duration can be 3, 6, 9 or 12 months. Extensions must follow the same procedures.
* Requests **may be resized** to fit the available global allocation.
* Calls are held **for 2027 only**. **No project will be allocated resources in 2028.**
* **Existing projects with resources already allocated in 2027 must reapply to the first call (Q1: 27 January 2027, cutoff 15 December 2026).**

| Call | Starting Date | Call Cutoff Date (Submit to the SPoCs by) |
| :--- | :--- | :--- | 
| **Q1** | January 2027 | 15 December 2026 | 
| **Q2** | April 2027 | 15 March 2027 | 
| **Q3** | July 2027 | 15 June 2027 | 
| **Q4** | October 2027 | 15 September 2027 |

## Contact & Support Procedures

> **Important:** Users and PIs **must not contact LuxProvide directly** (including the LuxProvide Service Desk), as per LuxProvide's request. **All requests and communications must go through the University of Luxembourg SPoCs**, who will liaise with LuxProvide when needed.

### Single Points of Contact (SPoCs) — University of Luxembourg
Submit all requests for new allocations, quota changes and project extensions to:

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

> **Submission Instruction:** Send both completed and signed documents via email to **Julien Schleich** ([julien.schleich@uni.lu](mailto:julien.schleich@uni.lu)) and **Matteo Barborini** ([matteo.barborini@uni.lu](mailto:matteo.barborini@uni.lu)) **at least 2 weeks before the cutoff date of the relevant quarterly call** (see [Section 3](#3-onboarding-allocation-schedule)). Do not send them to LuxProvide.


---

## Resource Allocation & Usage Policy

LuxProvide has implemented a resource allocation policy to ensure that shared public computing infrastructure is utilized efficiently and responsibly rather than sitting idle.

- **Active Allocation Usage:** Users are required to monitor their resource consumption continuously. Unused capacity incurs a public financial cost and prevents other researchers from utilizing available resources.
- **Proactive Communication:** Inform SPoCs as early as possible if your project is delayed, paused, or requires less capacity than requested. Early communication prevents automatic corrective measures.

---

### Progressive Monitoring Workflow
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

## Procedure summary for all types of requests

| Request Type | Responsible Entity | Submission Channel & Requirements |
| :--- | :--- | :--- |
| **New Allocation Applications** | UniLu SPoCs | Email [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu) with **completed Request Form + signed Terms of Use**, at least 2 weeks before the cutoff date of a quarterly call. **Do not contact LuxProvide directly.** |
| **Quota Increase or Decrease Requests** | UniLu SPoCs | Email [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barborini@uni.lu). The SPoCs will relay the request to LuxProvide. **Do not contact LuxProvide directly.** |
| **Project Extension Requests** | UniLu SPoCs | Email [Julien Schleich](mailto:julien.schleich@uni.lu) & [Matteo Barborini](mailto:matteo.barbaaaaaorini@uni.lu) with the **completed Request Form + signed Terms of Use**, at least 2 weeks before the cutoff date of a quarterly call. **Do not contact LuxProvide directly.** |
| **Technical issue and user change requests** | LuxProvide Service Desk | [LuxProvide Portal](https://servicedesk.lxp.lu/) / [servicedesk@lxp.lu](mailto:servicedesk@lxp.lu) |


 
## Reference Pricing & Cost Awareness
 
**Note on Billing:** Reference pricing is provided strictly to foster awareness of the public investment scale. **These costs are informational and will NEVER be charged or billed to your project or department.**
 
| Resource Type | Reference Rate (100 Node-Hours) | 
| :--- | :--- | 
| **CPU Compute** | ~€350.00 | 
| **GPU Compute** | ~€800.00 | 
| **FPGA Compute** | ~€800.00 | 
| **Large Memory (BigMem)** | ~€1000.00 |
| **Data Storage** | LuxProvide has not released explicit storage reference rates. |
