import requests
address_of_server="http://127.0.0.1:8000"
def show_all_products(users_name, users_age)
	my_headers={"NameOfUser": users_name, "AgeOfUser": users_age}
	server_reply=requests.get.(f"{address_of_server}/products", headers=my_headers)
	server_reply.raise_for_status(
	info_from_server = server_reply.json()

	print("\nAvailable Skin Care Products:")
	for one_item in info_from_server["products"]:/Users/zaryifazfar/Downloads