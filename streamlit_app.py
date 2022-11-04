import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

## Pandas section

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

## Requests section - New Section to display fruityvice API response

def getFruityViceData (this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information!")
  else:
    back_from_function = getFruityViceData(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

## Snowflake connector section

streamlit.header("The fruit load list contains:")

# Snowflake related functions
def getFruitLoadList():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = getFruitLoadList()
  streamlit.dataframe(my_data_rows)

# Allow end user to add fruits to the list
def insertRowSnowflake(newFruit):
    with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")
      return "Thanks for adding " + newFruit
  
addMyFruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  backFromFunction = insertRowSnowflake(addMyFruit)
  streamlit.text(backFromFunction)
