# simpleDataBase_Exp
A brief proof of concept experiementation of implementing a database in supabase.
----------------------------------------------------------------------------------------------

For this database, I modeled a simple reservation application, that allows users to create reservations and admins to manipulate what equipment and other info.

This database was created with supabase. In order to expand my abilities I decided to include stored images as well utilizes some of supabases built in functionality.

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
   This tables purpose is to help facilitate the many-many relationship between reservations and equipment. One event can have many pieces of equipment and one piece of equipment can have many reservations (While not at the same time. We get to that later.). This had an 'Admin All' policy allowing an adimin to retroactilvy alter orders. It was also supposed to have a 'insert only policy' but that had some issues.

   **Table: Reservations**
   This is where the guest users could insert their orders. *Note: This is a rough idea of what that would look like. An official version would include details such as billing information, but As I don't have any equipment in the first place. I figured that was an unneeded future addition.* There is nothing super special about this Table. Standard 'Admin Acces' and an guest 'insert only policy'

   **Functions**
   I only started experimenting with functions after I failed to get the 'insert only policy to work'. Apparently supabase has a really hard time allowing guest users to only insert (not read) a table. After a few hours of struggling I discovered supabases function capablities. After some quick learning I created a function that would allow me to do the same thing as my 'insert only policy'. Looking retrospectavly, I wish I had implemented more of these supabase function. They allow for much cleaner code and better table comparisons.

*Access code
   
