import pandas as pd
from datetime import datetime
from ggplot import *

def process_date(_date):
	dt_list = _date.split("/")
	
	return datetime(int(dt_list[2]), int(dt_list[0]), int(dt_list[1]))

def get_unit_type(_unitNumber):
	building_area = ''
	unit_type = ''

	if int(_unitNumber) < 1000:
		building_area = 'Intracoastal'
	else:
		building_area = 'Lake'

	if str(_unitNumber)[-1] in ('1', '5'):
		unit_type = 'A'
	elif str(_unitNumber)[-1] in ('2', '4'):
		unit_type = 'B'
	elif str(_unitNumber)[-1] == '3':
		unit_type = 'C'

	if str(_unitNumber)[0] == '9':
		if str(_unitNumber)[-1] == '3':
			unit_type = 'B'
		elif str(_unitNumber)[-1] == '4':
			unit_type = 'A'

	return "{0} {1}".format(building_area, unit_type)

if __name__ == "__main__":
	df = pd.read_csv('cw_2014.txt', sep = '\t')

	df['Sold Date'] = df['Sold Date'].apply(process_date)
	df['Unit Type'] = df['Unit #'].apply(get_unit_type)

	p = ggplot(aes(x = 'Sold Date', y = 'Sold Price', color = 'Unit Type'), data = df) + \
		geom_point() + \
		stat_smooth(span=1, se=False) + \
		scale_y_continuous(labels='comma') + \
		labs(title='Canopy Walk Sales, 2014', x='Date of Sale', y='Sale Price ($)')

	# fig = p.draw()
	# fig.show()
	# ax = fig.axes[0]
	# offbox = ax.artists[0]
	# offbox.set_bbox_to_anchor((1, 0.5), ax.transAxes)	

	ggsave(p, "scatter.jpg")