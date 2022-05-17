#!/usr/bin/env python
# coding: utf-8

# 
# 
# # Project: Investigate a Dataset - [TMDb movie data]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# >In this data selected from five avialble dataset to finish this project ,The selected one is **TMDb movie data**  this dataset contains data for more than 10000 movie produced in diffrent eras from 1960 to 2015 , The dataset countain information about movies like (idmdb, budget ,revenue,cast,....etc)lets assess ,clean and do some intersting investigations
# 
# 
# ### Question(s) for Analysis
# <li>1)which movie has (higher/lower)budget?</li> 
# <li>2)which movie has(higher /lower )revenue ?</li> 
# <li>3)which are movies has(higher /lower )vote average? </li>  
# <li>4)Do movie with high budget has better rating?</li> 
# <li>5)Do movie calssic movies have  better vote or modern ?</li> 
# <li>6)how much the number of movie production changed over the years?</li> 
# <li>7)what are the most common genres ?</li> 
# <li>8)what is the most prefered run time ?</li>
# <li>9)what is the best month to releas a movie ?</li>
# 

# ## Load important libirary

# In[1]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
#load important libirary 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# #### Functions will use in analysis tp prevent repeted code 
# 

# In[25]:


def column_analysis(column_name):
    #get minemum value in certain column
    low=df[column_name].idxmin()
    #get data of low 
    low_row_data=pd.DataFrame(df.loc[low])
    
    #get minemum value in certain column
    high=df[column_name].idxmax()
    #get data of low 
    high_row_data=pd.DataFrame(df.loc[high])
    all_data=pd.concat([high_row_data,low_row_data],axis=1)
    return all_data
def vote_analysis(column_name):
    #get median of budget 
    
    column_median=df[column_name].median()
    #filter lower than median 
    low=df.query("`column_name` <= @column_median")
    #filter hiegher than median 
    high=df.query("`column_name` > @column_median")
    #check if all sample incuded in analysis
    #get number of rows
    num_sample=df.shape[0]
    #copmare number of rows with sum of to groups
    num_sample == low['vote_average'].count() + high['vote_average'].count()
    #get mean of vote_average for low budget 
    low_mean =low['vote_average'].mean()
    #get mean of vote_average for high budget
    high_mean =high['vote_average'].mean()
    #check if low budget or high budget affect on vote_avrage
    if low > high:
        print ("the movie with lower @column_name has vote average more than movie with higher @column_name ")
    elif low < high:
        print ("the movie with higher @column_name has vote average more than movie with lower @column_name ")
    else:
        print("the @column_name doesn't affect on the vote_average ")


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > In this section data will loaded,assess and clean to make it ready for investigations 

# ## Load data

# In[3]:


#load data from url to datafarame
url="https://d17h27t6h515a5.cloudfront.net/topher/2017/October/59dd1c4c_tmdb-movies/tmdb-movies.csv"
df=pd.read_csv(url)


# ### Assessing data
# >in this part of code we will assessing the data to know exactly important columns for our investigation 

# **1-print data head**

# In[4]:


#set option to see all columns of data 
pd.set_option('display.max_columns',None)
#print few rows of our data
df.head()


# show detailed columns for dataframe to select important columns for investigation 

# **2-check general info about the data**

# In[5]:


#view data type for each cell and missing values 
df.info()


# the data has null value and also need to change datatypes for some columns
# 

# **3-Get the shape of the data**

# In[6]:


#show the shape of our original datafram
df.shape


# shape of our data (rows,columns)

# **4-check duplicates rows in our data**

# In[7]:


#number of duplicated rows in our data 
df.duplicated().sum()


# show number of duplicated rowsin our data

# **5-check count of null values in each column** 

# In[8]:


#count of null value 
df.isnull().sum()


# count of NAN values for each column

# **6-make some statistics for data**

# In[9]:


df.describe()


# there is columns it has analysis althogh it shoudn't, like "id" becouse it is (integer) we should change it to (str) 
# ,also we have 0 values in "run time","budget","revenue" should elemenated 

# ### Assessing discussion
# > after assess our data we this issues in our data and found that 
# <li>1)Extra column not needed in our investigation</li> 
# <li>2)Dublicated rows actully its one row </li> 
# <li>3)Null and zero values </li>  
# <li>4)Invalid values like "runtime =0" and also out of logic range "runtime =900"</li> 

# 
# ### Data Cleaning
# >in this part data will cleaned to insure that the data are ready for analysis
#  

# **1-Remove exrtaneos columns** 

# In[10]:


#drop list of  extraneos columns
#list of erxrtaneos columns 
extra_columns=['imdb_id','homepage','tagline','keywords','production_companies','budget_adj','revenue_adj']
df.drop(columns=extra_columns,inplace=True)
#check columns after drop
df.info()


# Droped extra columns will not used in investigation 

# **2-Drop duplicats rows**

# In[11]:


#delet duplicated rows
df.drop_duplicates(inplace=True)
#check if there are any other duplicated 
df.duplicated().sum()


# drop dubliacte rows and check the data has no other duplicates

# **3-Fill zero value with null**
# >will apply this for "budget" and "revenue" only,and for "runtime" will fill it with avrage   

# In[12]:


#creat list for coulmmns will fill with null
zero_list=['budget','revenue']
#fill null for the list created
df[zero_list]=df[zero_list].replace(0,np.nan)
#check
df.describe()


# all zeros converted to null because we couldn't estimate it then we removed later

# **4-Fill runtime coulmn with mean** 

# In[13]:


#get mean of runtime 
runtime_mean=df.runtime.mean()
runtime_median=df.runtime.median()
#replace 0valu with mean 
df["runtime"]=df['runtime'].replace(0,runtime_mean)
#after eleminate zeros will set all movies less than median to the mean runtime  
df['runtime']=df['runtime'].apply(lambda runtime_value :runtime_mean if runtime_value <=runtime_median  else runtime_value);
df.describe()


# after filling run time zero value with the mean we found another value doesn't make sense i fill it with the median 

# **5-Drop all null**

# In[14]:


#drop all null value 
df.dropna(axis=0,inplace=True)

df.shape


# In[15]:


df.dtypes


# I will change "id"to str to prevent any calcualtion on coulmn ,and 'budget'and "revenue" to int and "releasedate" to dateobject 

# In[16]:


#convert id to str 
df.id=df.id.astype(str)
#conert budget and revenue to int use another way
#creat list of coulum will convert
int_convert_list=['budget','revenue']
#apply change using 
df[int_convert_list]=df[int_convert_list].applymap(np.int64) 
#change releas date to date object
df.release_date=pd.to_datetime(df.release_date)
df.head()


# In[17]:


df.info()


# **7-Add profit column**
# > To add profit column will get defrence between revenue and budget

# In[18]:


#insert profit column
df.insert(4,'profit',df['revenue']-df['budget'])
#check 
df.head()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 
# ### Research Question 1) which are movies has (higher/lower)budget?

# In[19]:


#use column analysis funtion (user function)
column_analysis("budget")


# The Warrior's Way for "Sngmoo Lee"  has maximum budget 425000000 daollars with rate "6.4" ,
# and Lost & Found for "Jeff Pollack" has minmum budget 1 dollar, (don't make sense ) 
# 

# ### Research Question 2) which are movies has(higher /lower )revenue ?

# In[20]:


column_analysis("revenue")


# Avatar for James Cameron has the highest revenue 2781505847	dollars and Shattered Glass for Billy Ray has lowest

# ### Research Question 3) which are movies has(higher /lower )vote average

# In[21]:


column_analysis("vote_average")


# The Shawshank Redemption has highst rate in all data "8.4" and Foodfight!has lowest  "2.2"

# ### Research Question 4) Do movie with high budget has better rating?

# In[26]:


#we need to clasify budget to high and low will use median to do this

vote_analysis("budget")
    


# ooh! its seem right but also don't forget we didn't respect inflation over time in this calculation .

# ### Research Question 5)Do movie calssic movies have  better vote or modern  ?
# > will assume modern year the movies produced befor 1980 is classic 

# In[ ]:


#slpit data frame to modern and classic
classic_movie=df.query("release_year<1980")
modern_movie=df.query("release_year>=1980")
#get mean of avrage of votes per each movie 
classic_mean=classic_movie['vote_average'].mean()
modern_mean=modern_movie['vote_average'].mean()
#visualise the data in bars 
#set variabe of the function 
hights=[classic_mean,modern_mean]
locations=[1,2]
labels=['Classic','Modern']
plt.bar(locations,hights,tick_label=labels,width=.7)
plt.title("calssic and modern vote average")
plt.ylabel("vote average")
plt.xlabel("Movie era");


# The classic movies have higher rating more than modern movie 

# ### Research Question 6)how much the number of movie production changed over the years?

# In[ ]:


#sort years in our data 
years=np.sort(df.release_year.unique())
#visualise in histogram
df.release_year.hist(bins=25,figsize=(8,8));


# we coulde see that our distrebution is left skwed that indecate to number of movies production has raised over the years 

# ### Research Question 7)what are the most common genres ?

# In[ ]:


#genres coulunm come in strig so frist need to seperat them 
genres_type=df.genres.str.cat(sep="|")
genres_type=pd.Series(genres_type.split("|"))
genres_count=genres_type.value_counts()
genres_count.plot(kind="pie",title='Most common genre',figsize=(10,10));


# the gragh show that the drama come in first then comedy and thriller and action take th fourth class in data and tv_movie documentry western come in the tail of our data   

# ### Research Question 8)what is the most prefered run time ?

# In[ ]:


#draw relation betweeen run time and vote average of the movie 
df.plot( x='vote_average',y='runtime',
        kind='scatter',
        figsize=(10,10),
        yticks=np.arange(100,300,20),
        title=('relation between runtime and vote average'),);


# The high voted movie duration between 120:140 min 

# ### Research Question 9)what is the best month to releas a movie ?
# 

# In[ ]:


#group the releasing month and the profit 
g_month_profit_df=df.groupby(df.release_date.dt.month)['profit'].describe()
#draw relation between max profits and releasing month 
g_month_profit_df.plot(y='max',kind="barh",
                       figsize=(10,10),
                       title=('Best releasing month(max)'),)
#draw relation between mean profit and releasing month
g_month_profit_df.plot(y='mean',kind="barh",
                       figsize=(10,10),
                       title=('Best releasing month(mean) '),)
#show describtion 
g_month_profit_df


# max profits is for "Nov&Dec" but i coulde take the result with mean it less risk , so "May&jun" is best month to releas movie   

# <a id='conclusions'></a>
# ## Conclusions
# >From the all analysis done pepole prefered calssic movie more than modern movie, and the movie has the maximum budget was "The Warrior's Way" for"Sngmoo Lee" with rate "6.4"althogh that the movie didn't make high reveneu or vote rate compare with "avater" for "James Cameron" with rate "7.1" that made highest revenu"2781505847"Mellion dollars,let's alos don't forget, the gem of "Frank Darabont" The Shawshank Redemption got the highest rate ever 
# 
# >In the beginnig we coulde imagine that the movie with high budget is better but thats not right at all , actully we realised that the average of movie with low budget has higher rating more than high budget .
# 
# >By calculating the movie released over the years we found that the number of movie production raised year after year and that's indecate to the cinema industey is booming 
# 
# >By checking genres we found drama come in first then comedy and thriller and action take the fourth class in data and tv_movie documentry western come in the tail of our data 
# 
# >After checking runtimes for all movie and avrage rate from pepole , The high voted movie duration between 120:140 min 
# 
# >finally the movie released in month 6 or 5 has profit higher than all , and the worest month to releasin a movie is 9
# 
# 
# ## limitations:
# >one of the most important limitations that we have data doesn't make sense some movie has very low budget,revenue or runtime
# 
# >also alot of missing data (null or zero ) anyway we eleminate it but it more than 50% of our data
# 
# 

# In[ ]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

