from apartment_seeker import ApartmentData
from tkinter import messagebox

try:
    apt_data = ApartmentData()
    apt_data.enter_data()
except Exception as ex:
    messagebox.showwarning(message=ex)
    apt_data.driver.quit()
