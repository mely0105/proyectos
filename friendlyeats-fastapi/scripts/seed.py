from app.core.firebase import db

# S1-23: Script con 10 restaurantes de prueba según la especificación del Sprint 1
restaurants = [
    {
        "name": "La Abuela",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Pizza Central",
        "category": "Pizza",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1513104890138-7c749659a591",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Tacos El Pastor",
        "category": "Mexicana",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Sushi Roll",
        "category": "Japonesa",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Burger Haven",
        "category": "Hamburguesas",
        "city": "Guadalajara",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Trattoria Bella",
        "category": "Italiana",
        "city": "CDMX",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Café del Centro",
        "category": "Cafetería",
        "city": "Puebla",
        "price": 1,
        "photoUrl": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Mariscos El Jarocho",
        "category": "Mariscos",
        "city": "Veracruz",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "El Asador Real",
        "category": "Cortes",
        "city": "Monterrey",
        "price": 3,
        "photoUrl": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "avgRating": 0.0,
        "numRatings": 0,
    },
    {
        "name": "Green Salad Bar",
        "category": "Saludable",
        "city": "Guadalajara",
        "price": 2,
        "photoUrl": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "avgRating": 0.0,
        "numRatings": 0,
    },
]


def run_seed():
    print("Limpiando/Insertando datos semilla en Firestore...")
    for restaurant in restaurants:
        # Generar la referencia con ID automático e incluir el ID en el documento
        doc_ref = db.collection("restaurants").document()
        data = restaurant.copy()
        data["id"] = doc_ref.id
        doc_ref.set(data)

    print("¡10 datos semilla creados con éxito!")


if __name__ == "__main__":
    run_seed()