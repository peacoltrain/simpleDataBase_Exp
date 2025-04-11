# simpleDataBase_Exp
A brief proof of concept experiementation of implementing a database in supabase.
----------------------------------------------------------------------------------------------

For this database, I modeled a simple reservation application, that allows users to create reservations and admins to manipulate what equipment is avaiable and other info.

This database was created with supabase. In order to expand my abilities I decided to include stored images as well utilizes some of supabase's built in functionality.

This is the visualization of the end schema. 
![supabase-schema-vwhwmxddbceqgklmqvrp](https://github.com/user-attachments/assets/5176302e-546e-4f4c-8e15-f38581a33fb5)

I will now go over each of the tables in this database, along with an functions and policies in place.

  **Table: Office**
    This was a simple table with just its primary key and name of the office. A more fully implemented version would have had a mailing address or something akin to it.             However, I kept it simple for this project. This table had a 'Admin Full Access Policy' which allowed an authenticated user to read, write, delete etc. I didn't experiment with roles in this project so all 'Admin' are simply people who have a user account. However, you cannot make an account except someone adds you in the supabase interface, so it is relativly secure.

   **Table: Equipment_type**
   This is also and Admin table. *NOTE: json_description is not a accurate descriptor of the type of data contained. I just forgot to go back and change it.* The picture column simply contained a link to a supabase bucket where is stored the images as public allowing anyone to view them so long as they have the link. There was also a 'Guest Read' policy in place allowing customers to see exactly what equipment was being provided.

   **Table: Equipment**
   This table ties the previous two tables together. It is simply the type and where it is stored. This table has a 'Admin All' and 'Guest Read policy.' Because I set equipment_type foregin key to not be null it is important to add the new type prior to adding the individual equipemnt it this table.

   **Table: Reservation_equipment**
   This tables purpose is to help facilitate the many-many relationship between reservations and equipment. One event can have many pieces of equipment and one piece of equipment can have many reservations (While not at the same time. We get to that later.). This had an 'Admin All' policy allowing an admin to retroactively alter orders. It was also supposed to have a 'insert only policy' but that had some issues.

   **Table: Reservations**
   This is where the guest users could insert their orders. *Note: This is a rough idea of what that would look like. An official version would include details such as billing information, but As I don't have any equipment in the first place. I figured that was an unneeded future addition.* There is nothing super special about this Table. Standard 'Admin Acces' and an guest 'insert only policy'

   **Functions**
   I only started experimenting with functions after I failed to get the 'insert only policy to work'. Apparently supabase has a really hard time allowing guest users to only insert (not read) a table. After a few hours of struggling I discovered supabases function capablities. After some quick learning I created a function that would allow me to do the same thing as my 'insert only policy'. Looking retrospectavly, I wish I had implemented more of these supabase function. They allow for much cleaner code and better table comparisons.

# Application Code

I have the most experience with terminal run software so it may look ruff around the edges. I have my string file which contains some of the strings that I would use. I also have UserConnection and AdminConnection. User connection uses my .env file(Not included in this repository) to connect to supabase. It then has the options view and reserve. View simple allows the guest to view what types of equipment we have as well as its cost and event what they look like. Reserve allows a user to reserve a piece of equipment. This function also contains the logic to evalue if reservations overlap and if the input times make sense. In the future this logic would be moved into a supabase function.

Admin Connection asks for a email and password to establish an authorized connection with supabase. There are then a few premade functions that help the admin view the reservations, equipment table, add equipment, and equipment type. More helper function could could also be created.


# Future Plans:
There are so many things that I would like to implement. I would first and formost, like to move most of the logic into the supabase functions for cleaner code. I would also like to better flush out the application code to hunt for bugs and edge cases. I realized if you were doing an order for multiple pieces of equipment you would actually end up with mutiple lines in the reservation table, instead of having mutiple pieces of equipment under one order number. I also think it would be really cool if I could made inputing information easier. It occured to me while trying to figure out why my insert policy wasn't working that typeing in things like datatime is a real pain. I also think that using the piece of equipment not in use closest to the reservations address would also be most optimal. If you thing of something that would thing would be great to see implemented let me know.
   
