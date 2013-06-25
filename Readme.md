Movie Recommendation Engine Based on the MovieLens Database 
====

The Data Set
----
We use the archival 1 million MovieLens movie rating data set from Grouplens Research.

Data Wrangling
----

Cleaning, filtering, joining, etc of data sets were done using the Pandas Python library by Wes McKinney. 
The iPython notebook used in the project can be viewed here


Algorithm
----

I used item-based collaborative filtering for recommending movies based on the ratings provided by the website visitor. We use the adjusted cosine similarity function from Sarwar et. al , which has been tested to provide the lowest MAE among several correlation measures explored by the authors. 
To build the smilarity matrix, we used Numpy and Scipy along with Pandas. The simiilarity table was built with distributed computing to minimize run time. For easily querying the table, so that instant recoomendations could be generated the table is stored in a MongoDB database .

The app
---- 

I used the python based Flask framework to build the app. Rating stars were renedered with the raty javascript plugin. I used Jinja2 templating combined with Twitter Bootstrap to style the pages. (I rewrote the Python recommendation function in the notebook to run off of the MongoDB database rather than a python pickle file.) 

Visit the app at:

http://movie-lens-recommend.herokuapp.com/
