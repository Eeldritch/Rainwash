"""Creates necessary database files for Rainwash. Must be called before first runtime."""
import shelve
SAVEDATA = shelve.open("save_data")
SAVEDATA["SaveActive"] = False
try:
    EMAIL = SAVEDATA["Email"]
except KeyError:
    SAVEDATA["Email"] = input("Email: ")
    SAVEDATA["Password"] = input("Password: ")
if SAVEDATA["Email"] is None:
    SAVEDATA["Email"] = input("Email: ")
    SAVEDATA["Password"] = input("Password: ")
SAVEDATA.close()
