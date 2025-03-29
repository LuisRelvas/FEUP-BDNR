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

availabilty_columns = [
    'id','has_availability', 'availability_30', 'availability_60', 'availability_90', 'availability_365'
]

# booking_columns = [
#     'id'
# ]
# guest_columns = [
    
# ]



# LISTINGS DATASET
df_listings = df[listing_columns]

df_listings.to_csv('./dataset/listingTable.csv', index=False)

# HOSTS DATASET
df_hosts = df[host_columns].drop_duplicates().reset_index(drop=True)

df_hosts.to_csv('./dataset/hostTable.csv', index=False)


# AVAILABILITY DATASET
df_availability = df[availabilty_columns]

df_availability.to_csv('./dataset/availabilityTable.csv', index=False)

# # BOOKING DATASET
# df_booking = df[booking_columns] 

# df_booking.to_csv('./dataset/bookingTable.csv', index=False)


# # GUESTS DATASET
# df_guests = df[guest_columns].drop_duplicates().reset_index(drop=True)

# df_guests.to_csv('./dataset/guestTable.csv', index=False)


print("Dataset de hosts criado com sucesso!")
