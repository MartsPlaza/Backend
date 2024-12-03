import requests

# Login and obtain the token
response = requests.post('http://localhost:8002/api/admin/login', params={
    'email': 'user@gmail.com',
    'password': 'password'
})

data = response.json()
access_token = data['access_token']

# Function to get user profile
def get_user_profile():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    profile_response = requests.get('http://localhost:8002/api/users/profile', headers=headers)
    return profile_response.json()

# Function to get Seller's dashboard if the user role is seller
def get_seller_dashboard():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    profile_response = requests.get('http://localhost:8002/api/users/seller-dashboard', headers=headers)
    return profile_response.json()

def list_users():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    users = requests.get('http://localhost:8002/api/admin/users', headers=headers)
    return users.json()

def view_logs():
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    logs = requests.get('http://localhost:8002/api/admin/logs', headers=headers)
    return logs.json()

profile_data = get_user_profile()
seller_dashboard = get_seller_dashboard()
list_user = list_users()
logs = view_logs()
# print(profile_data)
print(logs)

# print(data)