import pandas as pd

df = pd.read_csv('./dataset/listings.csv')



""" df = df.drop(['host_about'], axis=1)
 """""" 
 """""" df.to_csv('./dataset/listings.csv', index=False)
 """

host_columns = [
    'host_id', 'host_name', 'host_since', 'host_location',
    'host_response_time', 'host_response_rate', 'host_acceptance_rate',
    'host_is_superhost', 'host_thumbnail_url', 'host_picture_url',
    'host_neighbourhood', 'host_listings_count', 'host_total_listings_count',
    'host_verifications', 'host_has_profile_pic', 'host_identity_verified'
]

listing_columns = [
    'id', 'listing_url', 'name', 'description','neighborhood_overview', 'property_type', 'room_type','accommodates', 'bathrooms','bedrooms', 'amenities'  ,'host_id', 'host_name', 'minimum_nights','maximum_nights', 'price'
]

df_test = df[listing_columns]

df_test.to_csv('./dataset/test_data.csv', index=False)

df_hosts = df[host_columns].drop_duplicates().reset_index(drop=True)

# Guardar o hosts dataset
df_hosts.to_csv('./dataset/hosts_data.csv', index=False)

print("Dataset de hosts criado com sucesso!")
