import requests

address_of_server = "http://127.0.0.1:8000"

def show_all_products(users_name, users_age):
    my_headers = {"NameOfuser": users_name, "AgeOfUser": users_age}
    server_reply = requests.get(f"{address_of_server}/products", headers=my_headers)
    server_reply.raise_for_status()
    info_from_server = server_reply.json()
    print("\nAvailable Skin Care Products:")
    for one_item in info_from_server["products"]:
        skin_types_text = ", ".join(one_item["skin_types"])
        concerns_text = ", ".join(one_item["concerns"])
        print(f"- #{one_item['id']} {one_item['name']} ({one_item['price']} BDT) [{skin_types_text}] concerns: {concerns_text}")

def get_advice_for_user(users_name, users_age):
    my_skin_type = input("Enter your skin type (dry/oily/normal/combination/sensitive): ").lower()
    my_concern = input("What is your main concern? (e.g. dryness, acne, redness): ").lower()
    my_budget = input("What's your maximum price? (optional, press Enter to skip): ")
    questions_to_send = {"users_skin_type": my_skin_type, "users_concern": my_concern}
    if my_budget:
        try:
            questions_to_send["max_price_user_wants"] = float(my_budget)
        except ValueError:
            print("That's not a number. We will ignore the price.")
    my_headers = {"NameOfuser": users_name, "AgeOfUser": users_age}
    server_reply = requests.get(f"{address_of_server}/recommendations", params=questions_to_send, headers=my_headers)
    server_reply.raise_for_status()
    info_from_server = server_reply.json()
    print("\nRecommended Skin Care Products for You:")
    if not info_from_server["results"]:
        print("Sorry, no products match what you need. Try again.")
        return
    for one_item in info_from_server["results"]:
        concerns_text = ", ".join(one_item["concerns"])
        print(f"* {one_item['name']} ({one_item['price']} BDT) - {one_item['category']} | addresses: {concerns_text}")

def calculate_cart_cost(users_name, users_age):
    ids_text = input("Enter product IDs to add to cart (comma separated, e.g., 1,2,3): ")
    try:
        list_of_ids = [int(x) for x in ids_text.split(",") if x]
    except ValueError:
        print("Please enter only numbers.")
        return
    my_headers = {"NameOfuser": users_name, "AgeOfUser": users_age}
    server_reply = requests.post(f"{address_of_server}/cart", json={"product_ids": list_of_ids}, headers=my_headers)
    server_reply.raise_for_status()
    info_from_server = server_reply.json()
    print("\nYour Shopping Cart:")
    if not info_from_server["selected"]:
        print("Your cart is empty.")
    for one_item in info_from_server["selected"]:
        print(f"- {one_item['name']} ({one_item['price']} BDT)")
    print(f"\nTotal Price: {info_from_server['total']:.2f} BDT")

def add_new_product(users_name, users_age):
    print("\n--- Add New Product ---")
    name = input("Product name: ")
    category = input("Category (e.g., Moisturizer, Cleanser, Serum): ")
    skin_types_input = input("Skin types (comma separated, e.g., dry, oily, normal): ")
    skin_types = [x.lower() for x in skin_types_input.split(",") if x]
    concerns_input = input("Concerns (comma separated, e.g., dryness, acne): ")
    concerns = [x.lower() for x in concerns_input.split(",") if x]
    price_input = input("Price: ")
    try:
        price = float(price_input)
    except ValueError:
        print("Invalid price. Product not added.")
        return
    ingredients_input = input("Ingredients (comma separated, optional): ")
    ingredients = [x for x in ingredients_input.split(",") if x] if ingredients_input else []
    
    new_product = {
        "name": name,
        "category": category,
        "skin_types": skin_types,
        "concerns": concerns,
        "price": price,
        "ingredients": ingredients
    }
    
    my_headers = {"NameOfuser": users_name, "AgeOfUser": users_age}
    server_reply = requests.post(f"{address_of_server}/products/add", json=new_product, headers=my_headers)
    server_reply.raise_for_status()
    info_from_server = server_reply.json()
    print(f"\nProduct added successfully! ID: {info_from_server['id']}")

def delete_product(users_name, users_age):
    product_id = input("\nEnter the product ID to delete: ")
    try:
        product_id = int(product_id)
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return
    
    my_headers = {"NameOfuser": users_name, "AgeOfUser": users_age}
    server_reply = requests.delete(f"{address_of_server}/products/{product_id}", headers=my_headers)
    server_reply.raise_for_status()
    info_from_server = server_reply.json()
    print(f"\n{info_from_server['message']}")

def show_menu():
    print("\n" + "=" * 30)
    print("  Dermatologist recommendation app  ")
    print("=" * 30)
    print("1. View all skin care products")
    print("2. Get personalized recommendations")
    print("3. Calculate cart total")
    print("4. Add new product")
    print("5. Delete a product")
    print("6. Exit")
    print("=" * 30)

def start_program():
    print("Welcome to the Dermatologist recommendation app!")
    name_input = input("Please enter your name: ")
    age_input = input("Please enter your age: ")
    while True:
        show_menu()
        choice = input("Choose an option (1-6): ")
        if choice == "1":
            show_all_products(name_input, age_input)
        elif choice == "2":
            get_advice_for_user(name_input, age_input)
        elif choice == "3":
            calculate_cart_cost(name_input, age_input)
        elif choice == "4":
            add_new_product(name_input, age_input)
        elif choice == "5":
            delete_product(name_input, age_input)
        elif choice == "6":
            print("Thank you for using the Dermatologist recommendation app. Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, 4, 5, or 6.")

if __name__ == "__main__":
    start_program()
