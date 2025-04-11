import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path
import mimetypes
import uuid
import strings

def AdminConnect():
    #Connect to Database
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    #Get login information
    print("This is the Admin access, please enter your username and password.")
    email = input("Email: ")
    password = input("Password: ")

    #Try sign in
    try:
        auth_response = supabase.auth.sign_in_with_password({"email":email, "password":password})
        user = auth_response.user

        if user is not None:
            print(f"\nLogged in as {user.email}")
            admin_actions(supabase)
        else:
            print("Login values incorrect")
    except Exception as e:
        print(f"Exception error: {e}")

def admin_actions(supabase: Client):
    print("\nAvailable admin actions:")
    while True:
        print(strings.adminActions)
        choice = input("Select an option: ")

        match choice.lower():
            case "1":
                view_all_reservations(supabase)
            case "2":
                view_all_equipment(supabase)
            case "3":
                add_equipment(supabase)
            case "4":
                add_equipment_type(supabase)
            case "l":
                print("Logged out.")
                break
            case _:
                print(" Invalid choice.")

def view_all_reservations(supabase):
    res = supabase.table("reservations").select("*").execute()
    for r in res.data:
        print(r)

def view_all_equipment(supabase):
    eq = supabase.table("equipment").select("*").execute()
    for e in eq.data:
        print(e)

def add_equipment(supabase: Client):
    print("\nAdd New Equipment")
    while True:
        #output current types and offices
        print("These are the types: ")
        types = supabase.table("equipment_type").select("*").execute().data
        for t in types:
            print(f"    {t['equipment_type_key']}: {t['json_description']}")

        print("\nThese are the Offices: ")
        offices = supabase.table("office").select("*").execute().data
        for o in offices:
            print(f"    {o['office_id']}: {o['officeName']}")
        try:
            type_key = input("Equipment Type Key: ")
            location_id = int(input("Location ID: "))
            response = supabase.table("equipment").insert({
                "equipment_type": type_key,
                "location_id": location_id
            }).execute()
        except:
            print("Add failed, try again")
        cont = input("Add More?[y][other]: ")
        if(cont.lower() != "y"):
            break
    

def add_equipment_type(supabase: Client):
    print("\n** Add New Equipment Type **")
    
    type_key = str(uuid.uuid4())
    description = input("Enter a Name: ")
    cost = float(input("Enter cost to rent: "))
    image_path = input("Path to image file (e.g., './images/camera.jpg'): ")

    # Check if file exists
    if not os.path.isfile(image_path):
        print("File does not exist.")
        return

    # File details
    file_name = Path(image_path).name
    storage_path = f"equipment/{file_name}"
    mime_type, _ = mimetypes.guess_type(image_path)

    # Read file
    with open(image_path, "rb") as f:
        file_data = f.read()

    try:
        # Upload to storage bucket
        bucket = "equipment-images"
        supabase.storage.from_(bucket).upload(path=f"/equipment/{file_name}",file=file_data)
        
        # Build public URL
        base_url = os.environ.get("SUPABASE_URL")
        public_url = f"{base_url}/storage/v1/object/public/{bucket}/{storage_path}"

        # Insert into equipment_type table
        response = supabase.table("equipment_type").insert({
            "json_description": description,
            "picture": public_url,
            "cost": cost
        }).execute()

        print("Equipment type successfully added.")
        print(f"Image URL: {public_url}")
    except Exception as e:
        print(f"Error during upload or insert: {e}")

if __name__ == "__main__":
    AdminConnect()