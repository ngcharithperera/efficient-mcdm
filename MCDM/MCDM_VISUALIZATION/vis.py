
#from bokeh.plotting import figure, output_file, show
#from bokeh.io import export_png

## prepare some data
#x = [1, 2, 3, 4, 5]
#y = [6, 7, 2, 4, 5]

## output to static HTML file
##output_file("lines.html")

## create a new plot with a title and axis labels
#p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

## add a line renderer with legend and line thickness
#p.line(x, y, legend="Temp.", line_width=2)

#export_png(p, filename="C:\\Users\\Charith\\ResearchCode\\efficient_mcdm\\MCDM\\MCDM_VISUALIZATION\\plot.png")

## show the results
##show(p)

import plotly.plotly as py
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

N = 1000
random_x = np.random.randn(N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y,
    mode = 'markers'
)

data = [trace]

# Plot and embed in ipython notebook!
py.iplot(data, filename='basic-scatter')

# or plot with: plot_url = py.plot(data, filename='basic-line')