# Classical Mechanics Lab 05: Video Analysis Instructions

## Project Overview
This lab analyzes projectile motion from video footage using Python. Two parallel notebooks exist:
- **vedioAnalysis.ipynb** - Main analysis workflow
- **analysis.ipynb** - Duplicate/reference version

Both notebooks perform identical analysis on video-extracted trajectory data from Logger Pro.

## Data Structure & Workflow

### Input Data (`data/data.csv`)
CSV contains 5 columns extracted from Logger Pro video analysis:
- `VideoAnalysis: Time (s)` - Time (normalized to 0 at start)
- `VideoAnalysis: X (m)` - Horizontal displacement
- `VideoAnalysis: Y (m)` - Vertical displacement  
- `VideoAnalysis: X Velocity (m/s)` - Extracted velocity (not used in fits)
- `VideoAnalysis: Y Velocity (m/s)` - Extracted velocity (not used in fits)

### Core Analysis Pattern
1. **Load & normalize time**: `data['VideoAnalysis: Time (s)'] -= data['VideoAnalysis: Time (s)'][0]`
2. **Fit models**:
   - Horizontal: Linear model `y = A*x + B` (constant velocity)
   - Vertical: Quadratic model `y = A*x² + B*x + C` (constant acceleration)
3. **Extract physics**: velocities (v_x, v_y), angles, range from curve parameters
4. **Compare**: Python scipy results vs Logger Pro software results

## Key Physics & Uncertainties

### Measurement Uncertainties
- **Position uncertainty**: ±1 meter (sum of:
  - Calibration error: ±0.5 m (cone height 1.22m vs Logger Pro 1.31m)
  - Tracking error: ±0.5 m (ball displacement per frame)
- **Time uncertainty**: ±0.034 seconds
- **Dominant source**: Eye-tracking error (not sub-meter precision possible)

### Physics Calculations
- **Launch angle**: $\theta = \tan^{-1}(v_y / v_x)$
- **Range formula**: $R = \frac{v_0^2 \sin(2\theta)}{g} + x_{intercept}$
- **Initial velocity**: $v_0 = \sqrt{v_x^2 + v_y^2}$

## Conventions & Patterns

### Curve Fitting Pattern
```python
from scipy.optimize import curve_fit

linear_model = lambda x, A, B: x * A + B
quadratic_parameters, cov = curve_fit(
    quad_model, 
    data["VideoAnalysis: Time (s)"], 
    data["VideoAnalysis: Y (m)"],
    sigma=(np.ones(len(data))) * y_uncertainity  # Uncertainty weighting
)
```

### Plotting Pattern
- Always set `xlim` using `min()`/`max()` of data
- Set `ylim(bottom=0)` for displacement plots (ground reference)
- Error bars use identical `xerr=0.034` across all time measurements
- Vertical uncertainty varies: ±1 m for X, ±0.5 m for Y

### Result Presentation
- Report fitted parameters with uncertainties: "8.3 (m/s) +/- 1 (m/s)"
- Include LaTeX math cells explaining physics connections
- Compare Python results to Logger Pro baseline (expect ~5% agreement)

## Common Modifications
- Adjust uncertainty values if calibration changes
- Expand analysis to extract acceleration from velocity data
- Add goodness-of-fit metrics (chi-squared, R²)
- Validate physics by checking energy conservation or momentum
