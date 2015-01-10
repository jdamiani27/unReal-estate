import pandas as pd
from datetime import datetime
from ggplot import *

def process_date(_date):
	dt_list = _date.split("/")
	
	return datetime(int(dt_list[2]), int(dt_list[0]), int(dt_list[1]))

def get_unit_type(_unitNumber):
	# ensure we're working with an int
	unitAsInt = int(_unitNumber)

	building_area = ''
	unit_type = ''

	if unitAsInt < 1000:
		building_area = 'Intracoastal'
	else:
		building_area = 'Lake'

	if str(unitAsInt)[-1] in ('1', '5'):
		unit_type = 'A'
	elif str(unitAsInt)[-1] in ('2', '4'):
		unit_type = 'B'
	elif str(unitAsInt)[-1] == '3':
		unit_type = 'C'

	if str(unitAsInt)[0] == '9':
		if str(unitAsInt)[-1] == '3':
			unit_type = 'B'
		elif str(unitAsInt)[-1] == '4':
			unit_type = 'A'

	return "{0} {1}".format(building_area, unit_type)

def get_unit_from_street(_streetName):
	poundPosition = _streetName.find('#')

	if poundPosition > -1:
		return _streetName[poundPosition + 1:].strip()
	else:
		return ''

	return _streetName[_streetName.find()]

if __name__ == "__main__":
	df = pd.read_csv('cw_2014.txt', sep = '\t')

	df['Sold Date'] = df['Sold Date'].apply(process_date)
	df['Unit Type'] = df['Unit #'].apply(get_unit_type)

	p = ggplot(aes(x = 'Sold Date', y = 'Sold Price', color = 'Unit Type'), data = df) + \
		geom_point() + \
		stat_smooth(span=1, se=False) + \
		scale_y_continuous(labels='comma') + \
		labs(title='Canopy Walk Sales, 2014', x='Date of Sale', y='Sale Price ($)') + \
		theme_seaborn()

	ggsave(p, "cw_2014_sales_trends.jpg")

	p = ggplot(aes(x = 'List Price', y = 'Sold Price', color = 'Unit Type', label = 'Unit #'), data = df) + \
		geom_point() + \
		stat_function(fun=lambda x: x, color = 'black', linetype='dashed') + \
		scale_y_continuous(labels='comma') + \
		scale_x_continuous(labels='comma') + \
		labs(title='Canopy Walk Sales, 2014', x='List Price ($)', y='Sale Price ($)')

	ggsave(p, "cw_2014_list_vs_sale.jpg")

	# all sales data
	df = pd.read_csv('cw_all.txt', sep = '\t')

	df['Sold Date'] = df['Sold Date'].apply(process_date)
	df.loc[df['Unit #'].isnull(), 'Unit #'] = df['Street Name'].apply(get_unit_from_street)
	df['Unit Type'] = df['Unit #'].apply(get_unit_type)

	p = ggplot(aes(x = 'Sold Date', y = 'Sold Price', color = 'Unit Type'), data = df) + \
		geom_point() + \
		stat_smooth(span=1, se=False) + \
		scale_y_continuous(labels='comma') + \
		labs(title='Canopy Walk Sales, All Time', x='Date of Sale', y='Sale Price ($)') + \
		theme_seaborn()

	ggsave(p, "cw_all_sales_trends.jpg")

