# Average Slope for Drug-Absorption Rate

A small, dependency-free Python implementation of **average slope (AS)** from
observed concentration-time data, using all consecutive observations from
`t = 0` through the observed `Tmax` (inclusive).

## Definition

For `n` observations up to and including `Tmax`, the metric is:

```text
                 1       n-1  C[i+1] - C[i]
average slope = ----- ×   Σ   ---------------
                n - 1     i    t[i+1] - t[i]
```

It is the arithmetic (unweighted) mean of the individual slopes between
consecutive concentration-time observations. Its units are concentration/time.
With equally spaced sampling, `C(0) = 0`, and a unique peak, the expression
telescopes to `Cmax / Tmax`. With unequal intervals, AS generally differs from
`Cmax / Tmax`; do not replace the mean above with a single endpoint slope.

The definition follows:

> Karalis VD. On the Interplay between Machine Learning, Population
> Pharmacokinetics, and Bioequivalence to Introduce Average Slope as a New
> Measure for Absorption Rate. *Applied Sciences*. 2023;13(4):2257.
> <https://doi.org/10.3390/app13042257>

## Install

Python 3.9 or newer is required.

```bash
python -m pip install .
```

For development and tests (no third-party test runner is required):

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

## Python API

```python
from average_slope import average_slope

result = average_slope(
    times=[0, 0.5, 1.5, 3, 5],
    concentrations=[0, 2, 6, 9, 7],
)

print(result.average_slope)   # 3.3333333333333335
print(result.tmax)           # 3.0
print(result.interval_slopes) # (4.0, 4.0, 2.0)
```

## CSV command line

The bundled example contains two subjects:

```bash
average-slope examples/concentration_time.csv --group subject
```

Write the result to a file:

```bash
average-slope input.csv --group subject --output average_slope_results.csv
```

Rename columns when required:

```bash
average-slope input.csv --time TIME --concentration CONC --group ID
```

Input rows may be unordered; the CLI sorts observations within each group by
time. The Python API itself requires already ordered observations.

## Data rules and explicit choices

- Time must start at exactly `0`, be non-negative, finite, and strictly
  increasing within a profile.
- Concentrations must be finite and non-negative.
- At least one post-dose point is required before or at the peak.
- By default, the first occurrence of a tied observed Cmax defines Tmax.
  Choose the last occurrence with `--tmax-tie last`, or reject ties with
  `--tmax-tie error`.
- Missing and BLQ values are rejected rather than silently imputed. Apply and
  document the preprocessing rule required by your analysis plan before using
  this package.
- AS is calculated independently for each profile/subject; do not average
  concentrations across subjects first.

This software implements a calculation and is not validated for clinical or
regulatory decision-making. Users remain responsible for data review,
pre-specified handling rules, validation, and compliance with applicable
guidance.

## Repository contents

```text
src/average_slope/       library and CLI
tests/                   unit and CLI tests
examples/                example concentration-time CSV
CITATION.cff             citation metadata
LICENSE                  MIT license
.github/workflows/       GitHub Actions tests for Python 3.9, 3.11, and 3.13
```
