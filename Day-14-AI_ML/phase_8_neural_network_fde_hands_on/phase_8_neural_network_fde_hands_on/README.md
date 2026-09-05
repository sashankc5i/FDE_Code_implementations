# Phase 8 — Neural Network FDE Hands-On

## Objective
Train a neural network on a synthetic customer-churn problem and troubleshoot realistic training failures.

## Workflow
1. Inspect data and target distribution.
2. Build a baseline MLP.
3. Train and evaluate it.
4. Reproduce a failure mode.
5. Diagnose using evidence.
6. Apply one targeted fix.
7. Compare before/after validation performance.
8. Document root cause and FDE recommendation.

## Failure modes
- Learning rate too high
- Overfitting
- Vanishing gradients
- Data/preprocessing mismatch

Do not change several major factors at once. Form a hypothesis, make one targeted change, and re-measure.
