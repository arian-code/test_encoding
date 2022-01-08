##### Import libraries
import numpy as np
from numpy import random
import random as rnd
import pandas as pd
import six
import sys
#sys.modules['sklearn.externals.six'] = six
#import mlrose                                   #Dirctly import mlrose has a bug
import tsplib95
import math
from matplotlib import pyplot as plt 
from scipy.spatial import distance_matrix
from statistics import mean
import os
import time
import sys
############################################################
#tour_list_organise: Organises tour list		     #
#use help (tour_list_organise)			     #	
############################################################
def tour_list_organise (tour_list):
	'''
	This is help for tour_list_organise function
	========================================================================
	Usage:	from  tsp_my_lib import *  
		tour_list_organise(tour_list)
	========================================================================
	Inputs:
		1. tour_list:
			TSP tour as list
			example:
				[5, 1, 2, 4, 3]
			type (tour_list) is list
	========================================================================
	Returns:
		1. tour_list::
			where:
				tour_list[0]==1
				tour_list[1]<tour_list[-1]
			example:
				[1, 2, 4, 3, 5]
			type (tour_list) is list
	========================================================================
	Dates of revisions:
		12 Sep 2020:	Created
	========================================================================
	END OF HELP: 
	========================================================================
	'''
	while tour_list[0]!=1: 
		tour_list.extend([tour_list.pop(0)]) 
	if tour_list[1]>tour_list[-1]:
		tour_list.reverse()
		tour_list.pop()
		tour_list.insert(0,1) 
	return (tour_list)

############################################################
#tour_length: loads tsp file				     #
#use help (tour_length)					     #	
############################################################
def tour_length(tour_list, tsp_dist_matrix):
	'''
	This is help for tour_length function
	========================================================================
	Usage:	from  tsp_my_lib import *  
		tour_length(tour_list, tsp_dist_matrix)
	========================================================================
	Inputs:
		1. tour_list:
			TSP tour as list
			example:
				[1, 3, 2, 4, 5]
			type (tour_list) is list
		2. tsp_dist_matrix
			TSP distance matrix
			type (tsp_dist_matrix) is  numpy.ndarray
	========================================================================
	Returns:
		1. length::
			length of the tour
			type (length) is numpy.float64
	========================================================================
	Dates of revisions:
		12 Sep 2020:	Created
	========================================================================
	END OF HELP: 
	========================================================================
	'''
	length=0
	for i in range(len(tour_list)):     
		length = length + tsp_dist_matrix[tour_list[i-1]-1, tour_list[i]-1]  
	return (length)

############################################################
#tour_list2matrix:
#use help (tour_list2matrix)					     #	
############################################################
def tour_list2matrix (tour_list):
	'''
	This is help for tour_matrix2list function
	========================================================================
	Usage:	from  tsp_my_lib import *  
		tour_matrix2list (tour_matrix_df)	
	========================================================================
	Inputs:
		1. tour_list:
			TSP tour as list
			example:
				[1, 3, 2, 4, 5]
			type (tour_list) is list
	========================================================================
	Returns:
		1. tour_matrix_df:<lower half only>:
			TSP tour in matrix dataframe
			example:
				   1    2    3    4    5
				1  NaN  NaN  NaN  NaN  NaN
				2  NaN  NaN  NaN  NaN  NaN
				3  1.0  1.0  NaN  NaN  NaN
				4  NaN  1.0  NaN  NaN  NaN
				5  1.0  NaN  NaN  1.0  NaN
			type (tour_matrix_df) is pandas.core.frame.DataFrame

	========================================================================
	Dates of revisions:
		06 Sep 2020:	Created
		14 Seo 2020:    Changed to return lower half of matrix only
	========================================================================
	END OF HELP: 
	========================================================================
	'''
	no_of_cities=len (tour_list)
	tour_matrix_df=pd.DataFrame(data =np.full([no_of_cities, no_of_cities], np.nan) , index = list (range(1,no_of_cities+1)), 	columns = list (range(1,no_of_cities+1))) 
	if (tour_list[len(tour_list)-1]>tour_list[0]):
		tour_matrix_df.loc[tour_list[len(tour_list)-1],tour_list[0]]=1 	    #add last edge
	else:
		tour_matrix_df.loc[tour_list[0], tour_list[len(tour_list)-1]]=1 	#add last edge
	for i in range (1,len(tour_list)): 				#add other edges
		if (tour_list[(i-1)]> tour_list[i]):
			tour_matrix_df.loc[tour_list[(i-1)], tour_list[i]]=1 
		else:
			tour_matrix_df.loc[tour_list[i], tour_list[(i-1)]]=1 
	return (tour_matrix_df)


############################################################
#tour_matrix2list: loads tsp file				     #
#use help (tour_matrix2list)					     #	
############################################################
def tour_matrix2list (tour_matrix_df, start_node=1):
	'''
	This is help for tour_matrix2list function
	========================================================================
	Usage:	from  tsp_my_lib import *  
		tour_matrix2list (tour_matrix_df)	
	========================================================================
	Inputs:
		1. tour_matrix_df::
			TSP tour in matrix dataframe
			example:
				   1    2    3    4    5
				1  NaN  NaN  NaN  NaN  NaN
				2  NaN  NaN  NaN  NaN  NaN
				3  1.0  1.0  NaN  NaN  NaN
				4  NaN  1.0  NaN  NaN  NaN
				5  1.0  NaN  NaN  1.0  NaN
			type (tour_matrix_df) is pandas.core.frame.DataFrame
		2. start_node:
			Node number to start tour list from
	========================================================================
	Returns:
		1. tour_list:
			TSP tour as list
			example:
				[1, 3, 2, 4, 5]
			type (tour_list) is list
		2.  status (int):
			-1 ->Tour has error (repete node) Precedence top
			0 ->Tour is incomplete
			1 ->Tour good and complete
		Note: if return status is -1, the last node in list is the repeated node	
	========================================================================
	Dates of revisions:
		06 Sep 2020:	Created
		14 Seo 2020:    Changed to cater for lower half of matrix only
	========================================================================
	END OF HELP: 
	========================================================================
	'''
	tour_list=[start_node]
	while (len(tour_list)<len(tour_matrix_df)):
		if ((tour_matrix_df.loc[tour_list[len(tour_list)-1],:].sum() + tour_matrix_df.loc[:,tour_list[len(tour_list)-1]].sum())<1):	
			return (tour_list, 0)
		if (tour_matrix_df.loc[tour_list[len(tour_list)-1],:].sum()>0):
			node_to_add=tour_matrix_df.loc[tour_list[len(tour_list)-1],:].idxmax()
			tour_matrix_df.loc[tour_list[len(tour_list)-1], node_to_add]=np.NaN
		else:
			node_to_add=tour_matrix_df.loc[:,tour_list[len(tour_list)-1]].idxmax()
			tour_matrix_df.loc[node_to_add,tour_list[len(tour_list)-1]]=np.NaN
		if node_to_add in tour_list:
			tour_list.append(node_to_add) 
			return (tour_list, -1)						#last edge was dulicated
		else:
			tour_list.append(node_to_add) 
	return (tour_list, 1)								#all good

############################################################
#tsp_load: loads tsp file				     #
#use help (tsp_load)					     #	
############################################################
def tsp_load (filename):
	'''
	This is help for tsp_load function
	========================================================================
	Usage:	from  tsp_my_lib import *  
		tsp_load (filename)	
	========================================================================
	Inputs:
		1. filename::
			str giving path of the tsp file, with full name
			type (filename) is str
	========================================================================
	Returns:
		1. tsp.name:
			This is the name of the problem specified in the .tsp file
		2. tsp_df
			This is pandas.dataframe with
				row index = Name of cities
				colm index= 'xcord', 'ycord'
				data is the->x, y values of points
		3. tsp_dist_matrix
			This is pandas.dataframe with
				Values of D (i,j) <-distance between cities i,j
				This distance is in accordance with TSPLIB library
	========================================================================
	Dates of revisions:
		06 Sep 2020:	Created
	========================================================================
	END OF HELP: 
	========================================================================

	'''
	tsp=tsplib95.load (filename)
	cities = (list(tsp.get_nodes()))            #names of nodes
	no_of_cities=len(cities)
	vertices=[]                                    #xy coord
	tsp_dist_matrix=np.zeros((no_of_cities, no_of_cities), dtype=int)
	for city_1 in range (1,no_of_cities+1):         
		vertices.append(tsp.node_coords[city_1])		#populate x,y coords
		for city_2 in range (city_1+1, no_of_cities+1): #populate tsp_dist_matrix
			tsp_dist_matrix[city_1-1, city_2-1]=tsp_dist_matrix[city_2-1, city_1-1]=tsp.get_weight(city_1, city_2)
	     
	tsp_df = pd.DataFrame(vertices, columns=['xcord', 'ycord'], index=cities)  #make data frame
	return (tsp.name, tsp_df, tsp_dist_matrix)
	
############################################################
#tsp_tour_plot: Used to plot TSP tour			     #
#use help (tsp_tour_plot)				     #	
############################################################
def tsp_tour_plot (xy_cords, tour_1=[], tour_2=[], tour_3=[],name="unknown",addn_points=[], saveplot=False, folder="pictures", comments="", city_names=[]):
	'''
	This is help for tsp_tour_plot function
	========================================================================
	Usage:	from  tsp_my_lib import *  
	
		Simple plot:
		tsp_tour_plot (([37, 49, 52, 20, 40], [52, 49, 64, 26, 30]), [1, 3, 2, 4, 5], saveplot=False)	
		Save plot:
		tsp_tour_plot (([37, 49, 52, 20, 40], [52, 49, 64, 26, 30]), [1, 3, 2, 4, 5])
		Plot with name "test"
		tsp_tour_plot (([37, 49, 52, 20, 40], [52, 49, 64, 26, 30]), [1, 3, 2, 4, 5], name="test", saveplot=False)	
	========================================================================
	Inputs:
		1. xy_cords:
			list of (x, y). example: xy_cords = ([37, 49, 52, 20, 40], [52, 49, 64, 26, 30])
			type (xy_cords) is tuple
		2. tours:
			Can take upto three tours and plots them in different colours
			list of tour to be plotted. example: tour= [1, 3, 2, 4, 5]
			type (tour) is list
		3. name:<optional>
			name is string. It is displayed as title and included in name, if file is saved 
			type (name) is str
		4. addn_points:<optional>
			addn_points are lsit of points to be plotted other than points in TSP problem
			example addn_points=[3,2]
			type (addn_points) is list
		5. saveplot:<optional><default=False>
			Picture is saved if set to True
			if False, plot is displayed
			type (saveplot) is bool
		6. folder:<optional><default=pictures>
			This is the folder in which plots are saved
			type (folder) is str
		7. comments:<optional><default="">
			These comments are displayed in the plot
			type (comments) is str	
		8. city_names:<optional><default=[]>
			List of names of points/ cities used to annotate in graph
			If not sepcified, cities are annotated as 1 to n
	========================================================================
	Plot save location:
		Plots are saved as png file in current directory with path diven below:
			./<folder>/mmdd_HHMM_rrr_<name>.png
			where:
				<folder>: default "pictures", else as specified
				mm:	month ex: Feburary=02
				dd:	day as 03
				HH:	hour as 13 in 24 hours
				MM:	is minutes
				rrr:	random
				<name>: default "unknown", else as specified
	========================================================================
	Dates of revisions:
		06 Sep 2020:	Created
		15 Sep 2020:	Modified to accept upto three tours
		19 Sep 2020:	Saving default set to 0, grid and comments added
	========================================================================
	END OF HELP: 
	========================================================================
	'''
	plt.figure(rnd.randint(1,1000))
	(x, y)=xy_cords
#Plot points
	plt.scatter(x,y) 
#Plot points names (annotate)
	for i in (list (range (0, len (xy_cords[0])))):
		if (len(city_names) == len (xy_cords[0])):
			plt.annotate(city_names[i], (x[i],y[i]))
		else:
			plt.annotate(str(i+1), (x[i],y[i]))
	#do for all three tours
	for i in list (range(1,4)):
		tour=tour_1
		color='r'
		width=4
		mark='D'
		leb="Tour 1"
		if i==2:
			tour=tour_2
			color='b'
			width=2
			mark='h'
			leb="Tour 2"
		elif i==3:
			tour=tour_3
			color='g--'
			width=1
			mark=''
			leb="Tour 3"
#Arrange tour
		if (len(tour)>1):
			x_tour=[]
			y_tour=[]
			for i in range (0,len(tour)):        #arrange x, y as tour
				x_tour.append(x[tour[i]-1])
				y_tour.append(y[tour[i]-1])
#plot tour
			plt.plot(x_tour, y_tour, color, linewidth=width, marker=mark, label=leb)	
			plt.plot([x_tour[len(x_tour)-1],x_tour[0]],[y_tour[len(y_tour)-1],y_tour[0]], color, linewidth=width, marker=mark) #connect last two points
#print title, tour and comments
	plt.title(name)
	plt.xlabel("X")
	plt.ylabel("Y")
	plt.legend(loc='upper right') 
	plt.grid(True) 
#plot additional points	
	if (len(addn_points)>0):
		[avg_x, avg_y]=addn_points
		plt.scatter(avg_x, avg_y)
	plt.text(0, 0.1, comments, fontsize=8, transform=plt.gcf().transFigure, wrap=True) 
#save or show plots
	if (saveplot):
		if not os.path.exists(folder):
		    os.makedirs(folder)
		file_name=(folder + "/" + (time.strftime('%m%d')) + "_"+ (time.strftime('%H%M')) +"_"+ str((time.time()))[-3:] + "_" + name + ".png")
		plt.savefig (file_name, bbox_inches='tight')
	else:
		plt.show()
	plt.close()


############################################################
#tspOptLength: loads tsp file				     #
#use help (tspOptLength)					     #	
############################################################
def tspOptLength (file_path, tsp_dist_matrix):
	'''
	This is help for tspOptLength function
	========================================================================
	Usage:	from  tspOptLength import *  
		tspOptLength (file_path, tsp_dist_matrix)	
	========================================================================
	Inputs:
		1. file_path::
			str giving path of the tsp file, with full name
			type (filename) is str
			example:	'../tsp_probs/my_tsp_probs/ulysses16.tsp'
		2. tsp_dist_matrix
			This is pandas.dataframe with
				Values of D (i,j) <-distance between cities i,j
	========================================================================
	Returns:
		1. length:
			Length of optimal tour based on tsplib
			Example:
				if input is 		'../tsp_probs/my_tsp_probs/ulysses16.tsp'
				length of tour in 	'../tsp_probs/my_tsp_probs/ulysses16.opt.tour' is returned
	========================================================================
	Dates of revisions:
		02 Oct 2020:	Created
	========================================================================
	END OF HELP: 
	========================================================================

	'''
	tsp_opt_tour_file = file_path[:-3] + 'opt.tour'
	if not (os.path.isfile(tsp_opt_tour_file)):
		return -1
	tsp_opt=tsplib95.load (tsp_opt_tour_file)
	return tour_length(tsp_opt.tours[0], tsp_dist_matrix)
