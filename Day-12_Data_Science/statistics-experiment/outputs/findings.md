# Statistics for FDEs — Experiment Findings

## Objective
Determine whether the observed AOV difference between Treatment and Control is statistically meaningful and whether the evidence is sufficient for a business decision.

## Experiment Results
| Metric | Result |
|---|---:|
| Control AOV | ₹1,962.31 |
| Treatment AOV | ₹2,061.28 |
| Absolute difference | ₹98.97 |
| Relative lift | 5.04% |
| 95% Confidence Interval | ₹68.36 to ₹129.57 |
| t-statistic | 6.34 |
| p-value | 2.38 × 10⁻¹⁰ |

Sample sizes:
- Control: **9,938**
- Treatment: **10,062**

## Hypotheses
**H₀:** μTreatment − μControl = 0

**H₁:** μTreatment − μControl ≠ 0

## P-value Interpretation
The p-value is **2.38 × 10⁻¹⁰**. It is not the probability that the null hypothesis is true. Assuming the null hypothesis and test assumptions hold, it measures how surprising a result at least as extreme as the observed result would be.

The extremely small p-value provides strong evidence against H₀, so we reject H₀.

## Confidence Interval
Estimated Treatment − Control difference: **₹98.97**.

95% CI: **₹68.36 to ₹129.57**.

Because the interval does not include zero, it is consistent with the hypothesis-test conclusion. It also communicates plausible effect magnitude rather than only significance.

## Statistical Conclusion
Treatment AOV is approximately **5.04% higher** than Control AOV, and the difference is statistically significant under the test assumptions.

## Business Interpretation
Statistical significance does not automatically imply business significance or prove causality. Before recommending rollout, investigate:
- Experiment randomization and group comparability
- Outliers and data quality
- Segment-level behavior
- Conversion impact
- Orders and customer behavior
- Margin/economic impact
- Retention and downstream metrics

## Segment Investigation
Treatment variability was higher than Control in several segments. North was particularly notable:
- North Control standard deviation: **~₹1,078**
- North Treatment standard deviation: **~₹1,321**

This is a signal for further investigation, not proof of a problem.

## FDE Statistical Mental Model
**Observed difference → Variation → Uncertainty → Confidence Interval → Hypothesis Test → P-value → Statistical Significance → Effect Size → Business Significance → Decision**

## Key Takeaway
> Statistics for an FDE is not about mechanically producing a p-value. The practical question is: "Is the observed customer result supported strongly enough by the data, is the effect large enough to matter, and is the experiment trustworthy enough for us to recommend action?"
