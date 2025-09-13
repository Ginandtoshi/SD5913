from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool
import pandas as pd

print("Script started")

csv_path = 'tides_processed.csv'

def load_data(path):
    df = pd.read_csv(path)
    print("Columns:", df.columns)
    print("Sample data:\n", df.head())
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df['tide_level'] = pd.to_numeric(df['tide_level'], errors='coerce')
    df = df.dropna(subset=['datetime', 'tide_level'])
    print("After cleaning, rows:", len(df))
    return df['datetime'], df['tide_level']

datetime, tide_level = load_data(csv_path)

# Map y values to blue intensity (0-255)
min_tide, max_tide = min(tide_level), max(tide_level)
blue_intensity = [int(255 * (val - min_tide) / (max_tide - min_tide)) if max_tide > min_tide else 128 for val in tide_level]
colors = [f"rgb(0,0,{b})" for b in blue_intensity]

source = ColumnDataSource(data=dict(
    datetime=list(datetime),
    tide_level=list(tide_level),
    color=colors
))

p = figure(
    title="Tidal Data Scatter Plot",
    x_axis_label='datetime',
    y_axis_label='tide_level',
    tools="pan,wheel_zoom,box_zoom,reset",
    x_axis_type='datetime'
)
p.circle('datetime', 'tide_level', color='color', size=10, source=source)

hover = HoverTool(
    tooltips=[('datetime', '@datetime{%F %T}'), ('tide_level', '@tide_level')],
    formatters={'@datetime': 'datetime'}
)
p.add_tools(hover)

output_file("tidal_scatter.html")
show(p)

print(f"Points: {len(datetime)}")
print(f"First datetime: {datetime.iloc[0]}, First tide_level: {tide_level.iloc[0]}")