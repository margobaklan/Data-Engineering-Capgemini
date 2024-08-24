import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, FactorRange, Legend, HoverTool, CustomJS, Select
from bokeh.transform import factor_cmap
from bokeh.palettes import GnBu3, Category10
from bokeh.layouts import column

def calc_surv_rate(category):
  sr = df.groupby(category)['Survived'].agg(['mean', 'count', 'sum']).reset_index()
  sr[category] = sr[category].astype(str)
  sr.rename(columns={'mean': 'SurvivalRate', 'count': 'Total', 'sum':'Survived'}, inplace=True)
  sr['NotSurvived'] = sr['Total'] - sr['Survived']
  sr['SurvivalRate'] = sr['SurvivalRate'] * 100
  return sr

def set_fig_params(p, x_label=None, y_label=None, x_label_orient=0, y_start=0):
  p.title.align = 'center'
  p.xaxis.axis_label = x_label
  p.yaxis.axis_label = y_label
  p.y_range.start = y_start
  p.x_range.range_padding = 0.05
  p.xgrid.grid_line_color = None
  p.xaxis.major_label_orientation = x_label_orient

df = pd.read_csv('Titanic-Dataset.csv')

# Handle missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Cabin'].fillna('Unknown', inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Create AgeGroup column
bins = [0, 12, 21, 60, 81]
age_labels = ['Child', 'Young Adult', 'Adult', 'Senior']
df['AgeGroup'] = pd.cut(df['Age'], bins, labels=age_labels)

# Age Group Survival: a bar chart 
age_sr = calc_surv_rate('AgeGroup')

# Data source and figure
s1 = ColumnDataSource(age_sr)
p1 = figure(title='Survival by age group',
            width=800, height=650, x_range = list(age_sr['AgeGroup']),
            toolbar_location=None, tools=['hover', 'tap'], tooltips='@$name')

v = p1.vbar_stack(['Survived', 'NotSurvived'], x='AgeGroup', width=0.8, source=s1,
              fill_color=['#66c2a5', '#fc8d62'], line_color=None)

# Customize
legend = Legend(items=[("Survived",   [v[0]]), ("Not Survived",   [v[1]])], location=(0, -30))
p1.add_layout(legend, 'right')
p1.add_tools(HoverTool(tooltips=[("Count", '@$name'), ("Age Group", "@AgeGroup"), ("Survival Rate", "@SurvivalRate%")]))
set_fig_params(p1, x_label='Age group', y_label='Count')

output_file("Survival_by_age_group.html")
save(p1)


# Gender and Class Survival: a grouped bar chart 
gender_sr = calc_surv_rate('Sex')
class_sr = calc_surv_rate('Pclass')

cl = class_sr['Pclass'].tolist()
gend = gender_sr['Sex'].tolist()
categories = ['Survived', 'NotSurvived']

cl_x = [(s, cat) for s in cl for cat in categories]
gen_x = [(s, cat) for s in gend for cat in categories]

class_counts = sum(zip(class_sr['Survived'], class_sr['NotSurvived']), ())
gender_counts = sum(zip(gender_sr['Survived'], gender_sr['NotSurvived']), ())

gender_data = dict(x=gen_x, counts=gender_counts)
class_data = dict(x=cl_x, counts=class_counts)

# Data source and figure
s2 = ColumnDataSource(data=gender_data)
p2 = figure(x_range=FactorRange(*gen_x), height=600, width=300, title="Survival Counts by Gender or Class",
            toolbar_location=None, tools=['hover', 'tap'], tooltips='@counts')
p2.vbar(x='x', top='counts', width=0.9, source=s2,
        fill_color=factor_cmap('x', palette=GnBu3, factors=categories, start=1, end=2))
set_fig_params(p2, x_label_orient=1)

# JavaScript callback to switch data
callback = CustomJS(args=dict(source=s2, gender_data=gender_data, class_data=class_data, p2=p2), code="""
    var new_data = cb_obj.value === 'gender' ? gender_data : class_data;
    
    // Update data source
    source.data = new_data;
    
    // Update x_range
    p2.x_range.factors = new_data['x'];
    
    source.change.emit();
    p2.change.emit();
""")

# Dropdown menu
menu = Select(options=['gender', 'class'], value='gender', title='Select')
menu.js_on_change('value', callback)

layout = column(menu, p2)
output_file("Survival_by_gender_class.html")
save(layout)


# Fare vs. Survival: a scatter plot
# Data source and figure
s3 = ColumnDataSource(data=dict(
    Fare=df['Fare'],
    Survived=df['Survived'],
    Pclass=df['Pclass'].astype(str)  
))

pclass_list = df['Pclass'].astype(str).unique()
color_map = factor_cmap('Pclass', palette=Category10[3], factors=pclass_list)
p3 = figure(height=600, width=1300, title="Fare vs. Survival Status",
            x_axis_label='Fare', y_axis_label='Survived')
p3.scatter('Fare', 'Survived', source=s3,
                     color=color_map, 
                     legend_field='Pclass', 
                     size=8, 
                     fill_alpha=0.6)

# Customize
p3.add_layout(p3.legend[0], 'right')
p3.legend.title = 'Passenger Class'
p3.y_range.end = 1.5
set_fig_params(p3, x_label='Fare', y_label='Survival Status', y_start=-0.5)
p3.add_tools(HoverTool(tooltips=[
    ("Fare", "@Fare"),
    ("Survived", "@Survived"),
    ("Class", "@Pclass")
]))

output_file("Fare_vs_survival.html")
save(p3)


