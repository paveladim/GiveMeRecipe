from Ingredients import get_ingredients
from Recipe import request_recipe


def give_recipe(path_to_image):
    product_list = get_ingredients(path_to_image)
    query = ", ".join(product_list)
    answer = request_recipe(query)
    return answer
