# simpleDataBase_Exp
A brief proof of concept experiementation of implementing a database in supabase.
----------------------------------------------------------------------------------------------

For this database, I modeled a simple reservation application, that allows users to create reservations and admins to manipulate what equipment and other info.

This database was created with supabase. In order to expand my abilities I decided to include stored images as well utilizes some of supabases built in functionality.

This is the visualization of the end schema. 
![supabase-schema-vwhwmxddbceqgklmqvrp](https://github.com/user-attachments/assets/5176302e-546e-4f4c-8e15-f38581a33fb5)

I will now go over each of the tables in this database, along with an functions and policies in place.
  **Table: Office**
    This was a simple table with just its primary key and name of the office. A more fully implemented version would have had a mailing address of something akin to it.             However, I kept it simple for this project. 
