# Interactive plot for David et al. (2012) model

Calculates stress-strain curve during uniaxial compression of a microcracked material. Strain is calculated as a function of stress, crack density, crack aspect ratio, and the intact Young's modulus of the material.

This model accounts for hysteresis during loading/unload stress cycling, due to the sliding and locking of microcracks when stress is applied and released.

David, E.C., Brantut, N., Schubnel, A., Zimmerman, R.W., 2012. Sliding crack model for nonlinearity and hysteresis in the uniaxial stress-strain curve of rock. International Journal of Rock Mechanics and Mining Sciences 52, 9–17. https://doi.org/10.1016/j.ijrmms.2012.02.001


## Requirements
pandas
matplotlib
numpy

## Example
Run plotDavidModel to load the data in ./data/data_template.xlsx

Fit the modelled curve (red line) to the data (blue line), changing the model parameters by clicking within the corresponding bars, or by dragging the sliders.

Standard deviation or error between the modelled stress-strain curve and the data is printed to the terminal.

![Screenshot](/images/screenshot.png)