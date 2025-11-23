import FastAPI
import Products

my_app= FastAPI()
@my_app.get("/products")#all item show
@my_app.get("/recommendations")
@my_app.post("/cart")
