import json

from WebScrappingService import ProductDetails

# How to execute this code
# Step 1 : pip install selenium. pillow, requests
# Step 2 : make sure you have chrome installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# Step 5 : put it inside the same folder of this code

baseUrl = 'https://www.midsouthshooterssupply.com/dept/reloading/primers?currentpage=1'
items = "product"

prodDetails = ProductDetails(baseUrl)
listOfJobObj = []
listOfJobObj += prodDetails.getAllJobsForOneDesignation(baseUrl, items)
#convert to JSON string
jsonStr = json.dumps(listOfJobObj)
print(jsonStr)