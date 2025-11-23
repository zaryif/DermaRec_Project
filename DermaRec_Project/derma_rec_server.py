from typing import List
from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from derma_rec_data import PRODUCTS

my_app = FastAPI(title="Dermatologist recommendation app API", version="1.0.0")
NAME_OF_LOG_FILE = "derma_log.txt"

def write_to_log_book(endpoint_name: str, data_we_got: dict, name_of_user: str, age_of_user: str):
    note_to_write = f"{endpoint_name} | {data_we_got} | User: {name_of_user} (Age: {age_of_user})\n"
    with open(NAME_OF_LOG_FILE, "a", encoding="utf-8") as my_file:
        my_file.write(note_to_write)

class ShoppingCartList(BaseModel):
    product_ids: List[int]

class NewProduct(BaseModel):
    name: str
    category: str
    skin_types: List[str]
    concerns: List[str]
    price: float
    ingredients: List[str] = []

@my_app.get("/products")
def show_list_of_products(request: Request):
    user_name = request.headers.get("NameOfuser", "Unknown")
    user_age = request.headers.get("AgeOfUser", "Unknown")
    write_to_log_book("/products", {}, user_name, user_age)
    return {"products": PRODUCTS}

@my_app.get("/recommendations")
def give_advice_on_products(
    request: Request,
    users_skin_type: str = Query(..., description="dry/oily/normal/combination/sensitive"),
    users_concern: str = Query(..., description="e.g. dryness, acne, redness"),
    max_price_user_wants: float | None = Query(None, description="Maximum price (optional)"),
):
    user_name = request.headers.get("NameOfuser", "Unknown")
    user_age = request.headers.get("AgeOfUser", "Unknown")
    what_user_wants = {
        "skin_type": users_skin_type,
        "concern": users_concern,
        "max_price": max_price_user_wants
    }
    write_to_log_book("/recommendations", what_user_wants, user_name, user_age)
    good_products_for_user = []
    for one_product in PRODUCTS:
        if users_skin_type not in one_product["skin_types"]:
            continue
        if users_concern not in one_product["concerns"]:
            continue
        if max_price_user_wants is not None and one_product["price"] > max_price_user_wants:
            continue
        good_products_for_user.append(one_product)
    return {"filters": what_user_wants, "results": good_products_for_user}

@my_app.post("/cart")
def calculate_total_cost(cart_info: ShoppingCartList, request: Request):
    user_name = request.headers.get("NameOfuser", "Unknown")
    user_age = request.headers.get("AgeOfUser", "Unknown")
    try:
        cart_data_simple = cart_info.model_dump()
    except AttributeError:
        cart_data_simple = cart_info.dict()
    write_to_log_book("/cart", cart_data_simple, user_name, user_age)
    items_in_cart = []
    for one_product in PRODUCTS:
        if one_product["id"] in cart_info.product_ids:
            items_in_cart.append(one_product)
    total_money = 0
    for item in items_in_cart:
        total_money = total_money + item["price"]
    return {"selected": items_in_cart, "total": round(total_money, 2)}

@my_app.post("/products/add")
def add_product(product_data: NewProduct, request: Request):
    user_name = request.headers.get("NameOfuser", "Unknown")
    user_age = request.headers.get("AgeOfUser", "Unknown")
    try:
        product_dict = product_data.model_dump()
    except AttributeError:
        product_dict = product_data.dict()
    write_to_log_book("/products/add", product_dict, user_name, user_age)
    new_id = max([p["id"] for p in PRODUCTS]) + 1 if PRODUCTS else 1
    new_product = {"id": new_id, **product_dict}
    PRODUCTS.append(new_product)
    return {"message": "Product added successfully", "id": new_id, "product": new_product}

@my_app.delete("/products/{product_id}")
def delete_product(product_id: int, request: Request):
    user_name = request.headers.get("NameOfuser", "Unknown")
    user_age = request.headers.get("AgeOfUser", "Unknown")
    write_to_log_book(f"/products/{product_id}", {"action": "delete"}, user_name, user_age)
    for i, product in enumerate(PRODUCTS):
        if product["id"] == product_id:
            deleted_product = PRODUCTS.pop(i)
            return {"message": f"Product '{deleted_product['name']}' deleted successfully", "deleted": deleted_product}
    return {"message": f"Product with ID {product_id} not found", "deleted": None}
