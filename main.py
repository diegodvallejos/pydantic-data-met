import requests
from rich import print

from typing_extensions import Annotated

from pydantic import BaseModel, ValidationError, field_validator
from pydantic.functional_validators import AfterValidator

#Definimos clases para los campos de las features que queremos con dtype
class Variant(BaseModel):
    title: str
    sku: str
    price: str
    grams: int
    

    #Creamos una validacion mediante el uso de field_validator (la docu es bastante clara, para hacer otro tipo de validaciones no deberiamos tener tanto problema)
    @field_validator('sku')
    def check_sku_len(cls, v):
        required_lenght = 10  #validacion para que checkear que sku es deberia tener 10 caracteres
        if len(v) != required_lenght:
            raise ValueError('SKU must be 10 characters long')
        return v
    

class Product(BaseModel): #en este dataset de productos que traigo veo que cada producto tiene un id, titulo y variantes que explican los diferentes productos
    id: int
    title: str
    variants: list[Variant]




def get_data():
    response = requests.get("https://www.allbirds.co.uk/products.json") #Datos en json de internet para testear
    return response.json()['products']

def main():
    products = get_data()
    for product in products:
        item = Product(**product)
        print(item.model_dump()) #model_dump lo pone como diccionario para que sea mas facil de querer mandarlo como json a un endpoint de nuestra app

if __name__ == "__main__":
    main()