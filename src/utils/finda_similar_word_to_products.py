from fuzzywuzzy import fuzz
from typing import List

def find_similar_words_to_get_products(input_text: str, products: List[str], threshold: int = 90) -> List[str]:

    stop_words = {'quero', 'comprar', 'um', 'uma', 'o', 'a', 'me', 'para'}
    
    # Divide o input do usuario em palavras e remove stop words
    input_words = [word.lower() for word in input_text.split() 
                  if word.lower() not in stop_words]
    
    # Divide cada produto em palavras
    product_words = []
    for product in products:
        product_words.extend(product.lower().split())
    
    product_words = list(set(product_words))
    
    similar_words = []
    
    # Compara cada palavra do input com cada palavra dos produtos
    for input_word in input_words:
        for product_word in product_words:
            similarity = fuzz.ratio(input_word, product_word)
            if similarity >= threshold:
                similar_words.append(input_word)
                break
    
    return list(set(similar_words))