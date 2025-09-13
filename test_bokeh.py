from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
import pandas as pd

# Minimal working example with hardcoded data
x = pd.to_datetime([
    '2023-01-01 05:31',
    '2023-01-01 11:27',
    '2023-01-01 18:44',
    '2023-01-02 01:18'
])
y = [1.58, 1.03, 2.05, 0.98]
colors = ['blue', 'blue', 'blue', 'blue']

source = ColumnDataSource(data=dict(datetime=x, tide_level=y, color=colors))

p = figure(title="Test Bokeh Plot", x_axis_label='datetime', y_axis_label='tide_level', tools="pan,wheel_zoom,box_zoom,reset", x_axis_type='datetime')
p.circle('datetime', 'tide_level', color='color', size=20, source=source)

hover = HoverTool(tooltips=[('datetime', '@datetime{%F %T}'), ('tide_level', '@tide_level')], formatters={'@datetime': 'datetime'})
p.add_tools(hover)

output_file("test_bokeh.html")
show(p)
