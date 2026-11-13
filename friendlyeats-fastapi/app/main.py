from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.v1.restaurants import router as restaurants_router
from app.services.restaurant_service import RestaurantService

app = FastAPI(title="FriendlyEats FastAPI")

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Instancia del servicio de restaurantes
service = RestaurantService()

# Endpoint de salud (S1-04)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Vista principal HTML con filtros dinámicos (S1-18 / HU-02)
@app.get("/")
async def home(
    request: Request,
    category: str | None = None,
    city: str | None = None,
    # Aceptamos int, str (para capturar "") o None
    price: Union[int, str, None] = None
):
    # Si viene como cadena vacía "" o espacio, lo convertimos a None
    parsed_price: int | None = None
    if price is not None and price != "":
        try:
            parsed_price = int(price)
        except ValueError:
            parsed_price = None

    # Limpiamos cadenas vacías si venían en la query para categoría y ciudad
    clean_category = category if category != "" else None
    clean_city = city if city != "" else None

    # Obtener restaurantes filtrados con la combinación de parámetros limpios
    restaurants = service.list(
        category=clean_category, 
        city=clean_city, 
        price=parsed_price
    )
    
    # Obtener todos los restaurantes para extraer ciudades y categorías únicas dinámicamente
    all_restaurants = service.list(limit=100)
    cities = sorted(list({r["city"] for r in all_restaurants if r.get("city")}))
    categories = sorted(list({r["category"] for r in all_restaurants if r.get("category")}))

    return templates.TemplateResponse(
        request=request,
        name="restaurants.html",
        context={
            "restaurants": restaurants,
            "cities": cities,
            "categories": categories,
            "selected_category": clean_category or "",
            "selected_city": clean_city or "",
            "selected_price": parsed_price or ""
        }
    )

# Vista Formulario Nuevo Restaurante (S1-20 / HU-01)
@app.get("/restaurants/new")
async def new_restaurant_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={"restaurant": None}
    )

# Vista Detalle del Restaurante (S1-19 / HU-03)
@app.get("/restaurants/{restaurant_id}")
async def restaurant_detail(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(
        request=request,
        name="restaurant_detail.html",
        context={"restaurant": restaurant}
    )

# Vista Formulario Editar Restaurante (S1-20 / HU-04)
@app.get("/restaurants/{restaurant_id}/edit")
async def edit_restaurant_form(request: Request, restaurant_id: str):
    restaurant = service.get(restaurant_id)
    return templates.TemplateResponse(
        request=request,
        name="restaurant_form.html",
        context={"restaurant": restaurant}
    )

# Rutas de la API v1
app.include_router(restaurants_router, prefix="/api/v1")