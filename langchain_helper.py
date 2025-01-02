from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from secret_key import openapi_key
from openai import RateLimitError

import os

os.environ['OPENAI_API_KEY'] = openapi_key

llm = OpenAI(temperature=0.7)


def generate_restaurant_name_and_items(cuisine):
    # Chain 1: Restaurant Name
    prompt_template_name = PromptTemplate(
        input_variables=['cuisine'],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this."
    )

    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")

    # Chain 2: Menu Items
    prompt_template_items = PromptTemplate(
        input_variables=['restaurant_name'],
        template="""Suggest some menu items for {restaurant_name}. Return it as a comma separated string"""
    )

    food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

    chain = SequentialChain(
        chains=[name_chain, food_items_chain],
        input_variables=['cuisine'],
        output_variables=['restaurant_name', "menu_items"]
    )

    try:
        response = chain({'cuisine': cuisine})
        print("API response:", response)  # Debugging: print full response
        return response
    except RateLimitError as e:
        print("Rate limit exceeded. Unable to process the request. Please check your API quota.")
        return {"error": str(e)}
    except Exception as e:
        print("An unexpected error occurred:", str(e))
        return {"error": str(e)}


def validate_response(response):
    """Validate if the response contains the required keys."""
    required_keys = ['restaurant_name', 'menu_items']
    for key in required_keys:
        if key not in response:
            print(f"Missing key in response: {key}")
            return False
    return True


if __name__ == "__main__":
    response = generate_restaurant_name_and_items("Italian")
    if validate_response(response):
        # Safely access the keys
        restaurant_name = response.get('restaurant_name', "No name returned").strip()
        menu_items = response.get('menu_items', "No items returned").strip()

        # Use the safely retrieved values
        print("Restaurant Name:", restaurant_name)
        print("Menu Items:", menu_items)
    else:
        print("The response is invalid.")

