from apartment_seeker import ApartmentData


try:
    apt_data = ApartmentData()
    apt_data.enter_data()
except Exception as ex:
    print(ex)
