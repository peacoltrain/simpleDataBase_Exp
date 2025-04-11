import os
from dotenv import load_dotenv
from supabase import create_client, Client
import strings
from datetime import datetime
import webbrowser

def get_valid_datetime(prompt: str) -> datetime:
    while True:
        time_input = input(prompt)
        try:
            return datetime.strptime(time_input, "%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid format. Please use YYYY-MM-DD HH:MM (24-hour clock).")

def getTimes():
    while (True):
        start_dt = get_valid_datetime("Enter the start time (YYYY-MM-DD HH:MM): ")
        end_dt = get_valid_datetime("Enter the end time (YYYY-MM-DD HH:MM): ")

        if start_dt >= end_dt:
            print("Start time must be before end time")
            continue

        return start_dt, end_dt

def reservation(supabase: Client):
    print("**RESERVATION MAKER**")

    #Personal Information
    firstName = input("Enter First Name: ")
    lastName = input("Enter Last Name: ")
    email = input("Email: ")
    phoneNumber = input("Phone: ")

    #Event info
    location = input("Enter an address: ")
    start, end = getTimes()

    #Get equipment
    equipment_types = None
    try:
        equipment_types = supabase.table("equipment_type").select("*").execute().data
    except Exception as ex:
        print(f"Error: {ex}")
    
    print("Available Equipment Types:")
    for et in equipment_types:
        print(f"{et['equipment_type_key']}: {et['json_description']}")
    eq_type = input("Enter the equipment_type_key you'd like to reserve: ")

    all_equipment = supabase.table("equipment").select("id").eq("equipment_type", eq_type).execute().data
    reserved_ids = supabase.table("reservations_equipment").select("equipment_id").execute().data
    reserved_ids_set = {r['equipment_id'] for r in reserved_ids}

    available = []
    for eq in all_equipment:
        eq_id = eq["id"]

        # Get reservations for this equipment
        res_links = supabase.table("reservations_equipment").select("reservation_id").eq("equipment_id", eq_id).execute().data
        if not res_links:
            available.append(eq)
            continue

        reservation_ids = [r["reservation_id"] for r in res_links]

        # Get reservation details for those IDs
        existing_res = supabase.table("reservations").select("event_start", "event_end", "reservation_number").in_("reservation_number", reservation_ids).execute().data

        overlap = False
        for res in existing_res:
            res_start = datetime.fromisoformat(res["event_start"])
            res_end = datetime.fromisoformat(res["event_end"])

            if not (end <= res_start or start >= res_end):  # overlap exists
                overlap = True
                break

        if not overlap:
            available.append(eq)
    
    if not available:
        print("No available equipment of this type for the selected time window.")
        return
    
    #Get additional notes
    notes = input("Do you have any specific notes you would like to add?\nEx. Drop of time, Style choices etc.\n")

    #Get First available
    equipment_id = available[0]['id'] 

    #Create Reservation
    
    reservation_id = supabase.rpc("insert_reservation_with_equipment", {
        "first_name": firstName,
        "last_name": lastName,
        "email": email,
        "phone": phoneNumber,
        "event_start": start.isoformat(),
        "event_end": end.isoformat(),
        "equipment_id": equipment_id
    }).execute()

    if reservation_id != None: print(f"Reservation confirmed! Your reservation ID is {reservation_id}")
    else: print("Something must have gone wrong; Please try again in a moment")
    

def view_items(supabase: Client):
    print("**AVAILABLE EQUIPMENT TYPES**")
    response = supabase.table("equipment_type").select("*").execute()
    for item in response.data:
        print(f"{item['equipment_type_key']}: {item['json_description']} (Cost: ${item['cost']})")

    tmp = input("If you would like to see the pictures say [more]: ")
    if(tmp.lower() != 'more'): return
    print(strings.moreDetails)
    value = input("Input: ")
    try:
        result = supabase.table("equipment_type").select("picture").eq("equipment_type_key", value).execute()
        webbrowser.open(result.data[0]['picture'])
    except:
        print("There seems to be an error")

def connection():
    #Print Application welcome
    print(strings.welcomeStr)
    
    #Connect to Database
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    #Get user input until quit
    while True:
        print("-------------------------------------------------------------------")
        request = input(strings.reqCom)
        match request:
            case "reserve": reservation(supabase)
            case "view": view_items(supabase)
            case "quit": break
            case _: print(strings.help)

    print(strings.farwell)
            

if __name__ == "__main__":
    connection()
