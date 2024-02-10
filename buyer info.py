import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import math
from geopy.geocoders import Nominatim

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('seller.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points given their latitude and longitude using the Haversine formula.
    """
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def create_sparse_matrix(num_merchants, num_pincodes):
    """
    Create a sparse matrix with dimensions (num_merchants x num_pincodes) initialized with zeros.
    """
    return [[0 for _ in range(num_pincodes)] for _ in range(num_merchants)]

def add_serviceability(sparse_matrix, merchant_id, pincode, value):
    """
    Add serviceability value for a specific merchant and pincode in the sparse matrix.
    """
    sparse_matrix[merchant_id][pincode] = value

def get_serviceability(sparse_matrix, merchant_id, pincode):
    """
    Get serviceability value for a specific merchant and pincode from the sparse matrix.
    """
    return sparse_matrix[merchant_id][pincode]

def get_pincode_from_address(address):
    """
    Get the pincode from the address using a geocoding service.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.raw['address'].get('postcode')
    else:
        return None

def get_latitude_from_address(address):
    """
    Get the latitude from the address using a geocoding service.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.latitude
    else:
        return None

def get_longitude_from_address(address):
    """
    Get the longitude from the address using a geocoding service.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    if location:
        return location.longitude
    else:
        return None

def get_item_price_from_seller(seller_id, item_type):
    """
    Get the price of an item type from a seller.
    """
    sellers_data = {
        'seller1': {
            'item1': 10,
            'item2': 20,
        },
        'seller2': {
            'item1': 15,
            'item2': 25,
        },
    }
    if seller_id in sellers_data and item_type in sellers_data[seller_id]:
        return sellers_data[seller_id][item_type]
    else:
        return None

def get_seller_rating(seller_id):
    """
    Get the rating of a seller.
    """
    seller_ratings = {
        'seller1': 4.5,
        'seller2': 3.8,
    }
    return seller_ratings.get(seller_id)

def get_buyer_current_address():
    """
    Get the current address of the buyer (manually entered).
    """
    return input("Enter your current address: ")

def get_sellers_by_item_type(item_type, buyer_lat, buyer_lon):
    """
    Get sellers sorted by distance, price, and rating for a specific item type.
    """
    sellers = db.collection('sellers').get()
    sellers_by_item_type = []

    for seller in sellers:
        shop_name = seller.get('shop_name')
        shop_address = seller.get('shop_address')
        pincode = get_pincode_from_address(shop_address)
        pincode_serviceability = seller.get('pincode_serviceability')
        price = get_item_price_from_seller(seller.id, item_type)
        rating = get_seller_rating(seller.id)

        if pincode in pincode_serviceability and pincode_serviceability[pincode]:
            sellers_by_item_type.append((calculate_distance(buyer_lat, buyer_lon, get_latitude_from_address(shop_address), get_longitude_from_address(shop_address)), shop_name, price, rating))

    return sorted(sellers_by_item_type, key=lambda x: (x[0], x[2], x[3]))

def buyer_request(buyer_lat, buyer_lon, item_type):
    """
    Process buyer's request by finding relevant sellers for the item type.
    """
    buyer_pincode = get_pincode_from_address(get_buyer_current_address())
    sellers = get_sellers_by_item_type(item_type, buyer_lat, buyer_lon)
    
    for distance, shop_name, price, rating in sellers:
        print(f"Shop: {shop_name}, Distance: {distance} km, Price: {price}, Rating: {rating}")


