# Currently only works for AllRecipes.com *****

import urllib3
from bs4 import BeautifulSoup
import re  # regular experession import
import recipe_class

urllib3.disable_warnings()  # stops the warnings about not being allowed to take info

# ----------------------------- FUNCTIONS ----------------------------------------------------------


# Function to remove basic tags from a string
def removeTag(text):
    # ex string: <a> b <c> will match the entire string but adding ? after * makes less greedy and will match every instance
    tagRemover = re.compile('<.*?>')
    # matches the tagRemover and replaces that matched text with '' from the string text
    cleanText = re.sub(tagRemover, '', text)
    return cleanText

def createDbId(url):
    info = url.split('/')
    print(info)

# takes the current html in and then finds the ingredients for an ALLRECIPES recipe
def findIngredients(soup):
    # finds all tags containing recipeIngredient (allrecipes tag for an ingredient)
    ingredientList = soup.find_all(attrs={'itemprop': 'recipeIngredient'})
    ingredients = []  # creates empty array
    for ingredient in ingredientList:
        # removes span tag from the ingredient for all recipes and appends to an array of ingredients
        ingredients.append(removeTag(str(ingredient)))
    return ingredients

def findRecipeSteps(soup):
    recipeStepsTag = soup.find_all(attrs={"class": "recipe-directions__list--item"})
    recipeSteps = []  # creates empty array
    for recipeStep in recipeStepsTag:
        # removes tag from the step for all recipes and appends to an array of steps
        recipeSteps.append(removeTag(str(recipeStep)))
    return recipeSteps  # use printList function to print out nicely

def findNutrInfo(soup):
    """
    Nutrition facts
    Time will take
    Servings 
    Calories per serving 
    add time breakdown, nutritional info breakdown
    """
    # finds all tags containing recipeIngredient (allrecipes tag for an ingredient)
    nutrientList = soup.find_all(attrs={'class':'nutrition-summary-facts'}) #grabs one long string on all the tags. ***this is not how I expected it to work
    #servings = soup.find_all(attrs={'class':'ng-binding'})
    nutritionalContents = []  # creates empty array
    for nutrient in nutrientList:
        # removes span tag from the ingredient for all recipes and appends to an array of ingredients
        nutritionalContents.append(removeTag(str(nutrient)))
    return nutritionalContents

def findAuthor(soup):
    authorName = soup.find('p') #use p to get reviews and comments
    return removeTag(str(authorName))

def findDescription(soup): #finds and returns the description of the recipe
    description  = recipeStepsTag = soup.find_all(attrs={"itemprop": "description"})
    return removeTag(str(description))

# prints any list of strings, using for printing ingredients/instructions etc.
def printList(ingredientList):
    for ingredient in ingredientList:
        print(ingredient)


# declaring the url you wish to pull html from
url = 'https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/'

# PoolManager = abstraction for a collection of ConnectionPools
# ConnectionPool =  container for a collection of connections to a specific host -  if need to make requests to same host repeatedly, use HTTPConnectionPool instead
# creates a poolmanger  (default 10 conenctions, can scale up, one per url)
http = urllib3.PoolManager()

# gets the html from the url using the request function, belongs to pool manager class
req = http.request('GET', url)

# soup = variable that contains the html of the page
soup = BeautifulSoup(req.data, 'html.parser')

# ------------------- code for grabing title and where site the recipe is from --------------------------------------

# removes the <title> </title> tags from the string and splits the resulting string on '-'
title = removeTag(str(soup.title)).split('-')
recipeName = title[0]  # grabs the recipe name from the site
# grabs the website recipe is from and removes .com
recipeWebsite = title[1].split('.')[0]
print(recipeName, recipeWebsite)
# ----------------------- -------------------------------------------------------------------------------------------

#-----------------------------------Finding the ingredients and listing them ---------------------------------------
ingredients = findIngredients(soup)
# ---------------------- grabbing instructions -------------------
recipeSteps = findRecipeSteps(soup)
# ------------------------Grabbing Nutrients------------------------------------
nutrients  = findNutrInfo(soup)
#Cant get the number of servings from the site bc it is adjustable? how do i get the default???
author = findAuthor(soup).strip()
description = 'Description: "' + str(findDescription(soup)).split('"')[1] + '"'
'''
print(author)
print(description+"\n")
print("Ingredients: \n")
printList(ingredients)
print('')
print("Steps:")
printList(recipeSteps)
print("Nutritional Information:")
printList(nutrients)
'''
test_recipe = recipe_class.Recipe(title=recipeName,author = author,
    description = description,ingredients = ingredients,
    steps = recipeSteps,nutritionalInformation = nutrients,url = url)

print(test_recipe.title)