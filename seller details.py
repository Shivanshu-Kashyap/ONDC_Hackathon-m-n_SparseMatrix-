from google.colab import files
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Upload the Firebase service account key file
uploaded = files.upload()

# Initialize Firebase Admin with service account credentials
cred = credentials.Certificate('seller.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

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

def add_seller(request):
    """
    Add a new seller with their address and pincode serviceability to Firestore.
    """
    # Extract seller information from request
    shop_name = request.get('shop_name')
    shop_address = request.get('shop_address')
    pincode_serviceability = request.get('pincode_serviceability')

    # Add seller to Firestore
    merchant_ref = db.collection('sellers').document()
    seller_id = merchant_ref.id
    merchant_ref.set({
        'shop_name': shop_name,
        'shop_address': shop_address,
        'id': seller_id
    })

    # Store pincode serviceability using a sparse matrix
    num_merchants = db.collection('sellers').get().size
    num_pincodes = len(pincode_serviceability)
    sparse_matrix = create_sparse_matrix(num_merchants, num_pincodes)

    for merchant_id, pincode_value_list in pincode_serviceability.items():
        merchant_id = int(merchant_id)
        for pincode, value in pincode_value_list.items():
            if value:
                pincode = int(pincode)
                add_serviceability(sparse_matrix, merchant_id, pincode, 1)

    # Save the sparse matrix in Firestore
    merchant_ref.collection('pincode_serviceability').document('matrix').set({
        'matrix': sparse_matrix,
    })

    return 'Seller added successfully'
