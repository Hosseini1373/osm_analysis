# Data Analysis and Statistics on OpenStreetMap Data (Amenities)

For more Information on the requirements of the project, please refer to **introduction.pdf**

# What the project does
We take OSM amneity nodes which are contained in osm-output.json as our dataset. The statistics that we created are included in 3 Tabs:

	• Tab1: Two Blocks for the city of Zurich; Block 1: Shows the amenities with the largest distance to each other in Zurich. Here we can again choose among the list of amenities. Five other blocks : Number of instances of amnenities in Zurich.
	• Tab2: A Barplot of the distribution of religions in Switzerland.
	• Tab3: The coordinates of amnenities on the map. The amenity can be chosen from a Drop-down list.







# How users can get started with the project
To start the project, we need to start the Flask server. Additionally we must run the mongoDB database. And lastly we must run the NodeJs server. The whole setup only works locally via localhost. 







# Files and Folders
The project is divided into multiple Files and Folder:



### osm-output.json 
This File is our Dataset.


### Frontend
This folder contains the UI elements. This is an Node project. 


### Backend
This Folder contains the backend Logic. This is based on Flask. The database that we use is MongoDB, which holds our dataset. Additionally we enrich this dataset with other information. We use the positionstack Webservice which gives us city for each coordinate-pair in Zurich. 

#### APIs

	• **/bar** is a get method, which returns a necessary JSON data for the barplot in Tab 2.
	• **/map/<amenity>** is a post method, which returns a necessary JSON data for the map in Tab 3for an input amenity.
	• **/amenities** is a get method, which returns a necessary JSON data for the Drop-down list.
	• **/city_amen** is a get method, which returns a necessary JSON data for the Block 1 of Tab 1.
	• **/distance/<amenity>** is a Post method, which returns a necessary JSON data for the Block 2-6 of Tab 1.





# Where users can get help with your project
To get more infos on the Project please email us: hossesay@students.zhaw.ch
# Who maintains and contributes to the project
The Collaborators on this Project are:
Sayyed Ahmad Hosseini,
Yves Bahler
