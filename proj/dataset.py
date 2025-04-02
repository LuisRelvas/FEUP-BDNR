import pandas as pd

df = pd.read_csv('./dataset/listings.csv')


host_columns = [
    'host_id','id', 'host_name', 'host_location','host_about','host_response_time','host_picture_url'
]

listing_columns = [
    'id', 'name', 'description', 'neighborhood_overview','neighbourhood_cleansed', 'neighbourhood_group_cleansed', 'amenities','property_type','price','bedrooms','bathrooms','review_scores_rating', 'host_id','host_name','host_location','host_response_time','picture_url'
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
