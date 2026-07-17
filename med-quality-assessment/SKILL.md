---
name: quality-assessment
description: This skill should be used when the user asks to "assess study quality", "evaluate risk of bias", "use RoB 2", "apply Newcastle-Ottawa Scale", "use AMSTAR 2", "assess with CASP", "check study validity", "rate research quality", or mentions methodological quality assessment of research studies. Provides standardized quality assessment tools and structured evaluation templates for different study designs.
---

# Quality Assessment — Research Study Evaluation

Systematically evaluate the methodological quality and risk of bias of research studies using validated, standardized assessment tools. Quality assessment determines how much confidence to place in a study's findings — a critical step before evidence synthesis.

## Core Concept

Quality assessment answers: **"How well was this study conducted, and how much should we trust its results?"**

Different study designs require different assessment tools. This skill provides the correct tool for each design type.

## Assessment Workflow

Follow this numbered pipeline for every quality assessment:

1. **Identify study design** — Read the methodology section. Classify the study as RCT, cohort, case-control, systematic review, qualitative, diagnostic accuracy, or other. If mixed design, note the primary design.
2. **Select assessment tool** — Use the Tool Selection Guide below to pick the matching validated instrument. If uncertain between two tools, present both options with rationale and ask user to confirm.
3. **Assess each domain** — Systematically evaluate every domain/item of the chosen tool using the structured YAML templates below. Mark items as yes/no/no-information. Add notes for each rating decision.
4. **Determine overall rating** — Apply the tool-specific overall rating rules (e.g., RoB 2: any domain high → overall high; NOS: star count → Good/Fair/Poor; AMSTAR 2: critical weaknesses → confidence level).
5. **Generate summary table** — Create a risk of bias summary table (see Summary Visualization section) across all assessed studies. Flag studies rated as high risk or critically low confidence.

After Step 5, the output is ready for downstream use by `evidence-synthesis` or `paper-comparison`.

## Tool Selection Guide

| Study Design | Assessment Tool | Domains |
|---|---|---|
| **Randomized Controlled Trial** | RoB 2 (Cochrane) | 5 bias domains |
| **Observational (Cohort)** | Newcastle-Ottawa Scale | 3 categories, 8 items |
| **Observational (Case-Control)** | Newcastle-Ottowa Scale | 3 categories, 8 items |
| **Systematic Review** | AMSTAR 2 | 16 items |
| **Qualitative Research** | CASP Qualitative | 10 questions |
| **Diagnostic Accuracy** | QUADAS-2 | 4 domains |
| **Prevalence/Incidence** | JBI Critical Appraisal | 9 items |
| **Case Report** | JBI Case Report | 8 items |
| **Economic Evaluation** | CASP Economic | 12 questions |
| **Animal Studies** | SYRCLE's RoB | 6 domains |

## Assessment Tools

### RoB 2 — Randomized Controlled Trials

Assess 5 bias domains, each rated as Low / Some Concerns / High:

```yaml
rob2_assessment:
  study_id: "Author (Year)"

  domain_1_randomization:
    question_1_1: "Was the allocation sequence random?" # yes/no/probably yes/probably no/no information
    question_1_2: "Was the allocation sequence concealed until participants were enrolled?"
    question_1_3: "Did baseline differences between intervention groups suggest a problem with randomization?"
    rating: "low | some_concerns | high"
    notes: "..."

  domain_2_deviation_from_intended:
    question_2_1: "Were participants aware of their assigned intervention?"
    question_2_2: "Were carers/people aware of assigned intervention?"
    question_2_3: "If relevant, was there deviation from intended intervention?"
    question_2_4: "Were these deviations likely to affect the outcome?"
    question_2_5: "Were these deviations from intended intervention balanced between groups?"
    question_2_6: "Was an appropriate analysis used to estimate the effect of assignment?"
    rating: "low | some_concerns | high"
    notes: "..."

  domain_3_missing_data:
    question_3_1: "Were data available for all participants randomized?"
    question_3_2: "Were data missing for the primary outcome?"
    question_3_3: "Were missing data balanced between groups?"
    question_3_4: "Was the potential impact of missing data assessed?"
    rating: "low | some_concerns | high"
    notes: "..."

  domain_4_measurement:
    question_4_1: "Was the method of measuring the outcome inappropriate?"
    question_4_2: "Could measurement differ between intervention groups?"
    question_4_3: "Were outcome assessors aware of intervention received?"
    question_4_4: "Was the assessment likely influenced by knowledge of intervention?"
    rating: "low | some_concerns | high"
    notes: "..."

  domain_5_selection_reporting:
    question_5_1: "Were results selected from multiple outcome measurements?"
    question_5_2: "Were results selected from multiple analyses?"
    question_5_3: "Is the registered report consistent with the published results?"
    rating: "low | some_concerns | high"
    notes: "..."

  overall_rating: "low | some_concerns | high"
  overall_notes: "..."
```

**Overall rating rules:**
- **Low risk**: All domains low
- **Some concerns**: At least one domain has concerns, but none high
- **High risk**: At least one domain high, or multiple concerns

### Newcastle-Ottawa Scale (NOS) — Cohort Studies

```yaml
nos_cohort_assessment:
  study_id: "Author (Year)"

  selection:  # Max 4 stars
    representativeness:
      question: "Is the exposed cohort representative?"
      options: ["truly representative ★", "somewhat representative ★", "selected group", "no description"]
      score: "★"
    non_exposed_selection:
      question: "Is the non-exposed cohort from the same community?"
      options: ["same community ★", "different community", "no description"]
      score: "★"
    ascertainment_of_exposure:
      question: "Was exposure ascertainment secure?"
      options: ["secure record ★", "structured interview ★", "written self-report", "no description"]
      score: "★"
    outcome_not_present_at_start:
      question: "Was the outcome not present at start?"
      options: ["yes ★", "no"]
      score: "★"

  comparability:  # Max 2 stars
    main_factor:
      question: "Are cohorts comparable on the main factor?"
      options: ["yes ★", "no"]
      score: "★"
    additional_factor:
      question: "Are cohorts comparable on any additional factor?"
      options: ["yes ★", "no"]
      score: "★"

  outcome:  # Max 3 stars
    assessment:
      question: "Was outcome assessment blind/independent?"
      options: ["independent blind assessment ★", "record linkage ★", "self-report", "no description"]
      score: "★"
    follow_up_length:
      question: "Was follow-up long enough for outcomes to occur?"
      options: ["yes ★", "no"]
      score: "★"
    adequacy_of_follow_up:
      question: "Was follow-up adequate (>80%)?"
      options: ["yes ★", "no (describe %)", "no description"]
      score: "★"

  total_stars: "7/9"
  quality_rating: "good (7-9) | fair (4-6) | poor (0-3)"
```

### AMSTAR 2 — Systematic Reviews

```yaml
amstar2_assessment:
  study_id: "Author (Year)"

  item_1: "Did the research questions and inclusion criteria include PICO?" # yes/no
  item_2: "Did the report contain an explicit statement that the review methods were established prior to the review?"
  item_3: "Did the review authors explain their selection of study designs?"
  item_4: "Did the review authors use a comprehensive literature search strategy?"
  item_5: "Did the review authors perform study selection in duplicate?"
  item_6: "Did the review authors perform data extraction in duplicate?"
  item_7: "Did the review authors provide a list of excluded studies and justify exclusions?"
  item_8: "Did the review authors describe included studies in adequate detail?"
  item_9: "Did the review authors use a satisfactory technique for assessing RoB in individual studies?"
  item_10: "Did the review authors report sources of funding for included studies?"
  item_11: "If meta-analysis was performed, did they use appropriate methods?"
  item_12: "If meta-analysis was performed, did they assess the impact of RoB?"
  item_13: "Did the review authors account for RoB in individual studies when interpreting results?"
  item_14: "Did the review authors provide a satisfactory explanation for heterogeneity?"
  item_15: "If they planned to do so, did they assess publication bias?"
  item_16: "Did the report sources of funding for the review?"

  critical_weaknesses: ["item_4"]  # Items 4, 7, 9, 11, 12, 15 are critical
  non_critical_weaknesses: ["item_5"]

  overall_confidence: "high | moderate | low | critically low"
```

### CASP — Qualitative Research

```yaml
casp_qualitative_assessment:
  study_id: "Author (Year)"

  screening_questions:
    q1: "Was there a clear statement of the aims of the research?" # yes/can't tell/no
    q2: "Is a qualitative methodology appropriate?"

  design:
    q3: "Was the research design appropriate to address the aims?"
    q4: "Was the recruitment strategy appropriate?"
    q5: "Was the data collected in a way that addressed the research issue?"

  data:
    q6: "Has the relationship between researcher and participants been considered?"
    q7: "Have ethical issues been taken into consideration?"
    q8: "Was the data analysis sufficiently rigorous?"

  findings:
    q9: "Is there a clear statement of findings?"
    q10: "How valuable is the research?"

  overall_rating: "rigorous | acceptable | flawed"
  notes: "..."
```

## Summary Visualization

Generate a risk of bias summary table across all assessed studies:

```markdown
### Risk of Bias Summary

| Study | Randomization | Deviations | Missing Data | Measurement | Reporting | Overall |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Smith 2023 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 |
| Jones 2022 | 🟢 | 🟡 | 🟢 | 🔴 | 🟢 | 🔴 |
| Lee 2024 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |

🟢 Low risk  🟡 Some concerns  🔴 High risk
```

## Error Handling and User Checkpoints

### Checkpoints
- **After tool selection**: present the chosen assessment tool and why it fits. If the study design is ambiguous (e.g., quasi-experimental vs RCT), ask user to confirm before proceeding.
- **After completing assessment**: show the filled assessment form with ratings. Ask user to verify critical domain ratings before finalizing.
- **Before "High risk" ratings**: if any domain is rated "High", present the evidence for that rating and ask user to confirm. High ratings significantly affect downstream evidence weighting.

### Error Handling
- **Incomplete methodology section**: if key assessment items cannot be answered from available text, mark as "no information" (not "low risk" or "high risk"). Flag to user whether to seek full text or rate as unclear.
- **Mixed study design**: if a study combines RCT and observational elements, note the conflict. Apply the most conservative applicable tool and flag the limitation to user.
- **Assessment tool uncertainty**: if no standard tool fits the study design, present the closest match with caveats and ask user whether to proceed or use a custom assessment.
- **Contradictory evidence within study**: if different sections of the paper suggest different quality levels, flag the contradiction and let user decide which to prioritize.

## Integration with Other Skills

- **paper-reader** — Extract methodology section for assessment
- **evidence-synthesis** — Use quality ratings to weight evidence
- **systematic-screening** — Quality assessment is the final screening stage
- **paper-comparison** — Include quality ratings in comparison matrix

## Additional Resources

### Reference Files
- **`references/assessment-tools-full.md`** — Complete item-level details for all assessment tools with scoring guidance
