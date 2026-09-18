# Blood Donate & Request System

A full-featured Django web application where users can register as blood donors, create blood requests, and search suitable donors based on blood group, location, and availability.

---

## 🌟 Key Features

1. **User Authentication & Authorization**:
   - User Registration, Login, Logout, Profile View, and Profile Update.
   - Built-in Django authentication extended with custom `DonorProfile` models.

2. **Donor Profile (CRUD)**:
   - Donor details including Name, Blood Group, Phone Number, Location, Last Donation Date, Availability Status , Profile Picture, and Short Bio.
   - Restrict updates so logged-in users only modify their own profiles.

3. **Blood Request Management (CRUD)**:
   - Request fields: Patient Name, Blood Group Required, Hospital Name, Location, Required Date, Bags Required, Contact Phone Number, Status , and Description.
   - Requesters can create, view, edit, delete, or update request statuses.

4. **Donor Search & Filter**:
   - Search donors by Blood Group (A+, A-, B+, B-, AB+, AB-, O+, O-), Location (e.g., Feni, Dhaka), and Availability.

5. **Blood Request Listing & Filter**:
   - Filter blood requests by Blood Group, Location, and Request Status.

6. **Form Validation**:
   - Phone number format checking.
   - Positive number enforcement for blood bag quantities.
   - Validation that required dates cannot be in the past.
   - Required input checks.

---

Live link and visit: 
 https://mens-which-damaged-folk.trycloudflare.com

