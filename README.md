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
   This tables purpose is to help facilitate the many-many relationship between reservations and equipment. One event can have many pieces of equipment and one piece of equipment can have many reservations(While not at the same time. We get to that later.)
