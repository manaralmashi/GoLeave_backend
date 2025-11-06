# GoLeave Backend

## 🏢 Capstone Project: Leave Management System

### 📘 Project Description
**GoLeave** is a full-featured **Leave Management System** designed to automate and simplify the leave request process within organizations.  
This repository contains the **backend part**, built with **Django REST Framework**, which provides secure and scalable APIs for the frontend.

The system supports:
- Two types of users: **Employees** and **Admins**.  
- **Employees** can submit and track their leave requests.  
- **Admins** can approve or reject requests and manage employee data.

The project’s goal is to **digitize traditional HR leave workflows** and offer organizations an efficient, centralized platform.

---

## 🔗 Related Repositories
➡️ [Frontend Repository](https://github.com/manaralmashi/GoLeave_frontend)

➡️ **Deployed Site:** (to be added after deployment)

---

## 🔷 Main Features
- Full CRUD functionality for managing employees and leave requests.  
- Automated leave balance calculation for each employee and leave type.
- Warning thresholds for low leave balances.  
- Role-based access control (Employee/Admin).  
- RESTful API endpoints for integration with frontend.  

---

## 🔷 Tech Stack
- **Django** – Backend framework  
- **Django REST Framework (DRF)** – API development  
- **SQLite / PostgreSQL** – Database  
- **CORS Headers** – Cross-origin support  
- **Cloudinary / Storage** – (optional for future use)

---

## 🔷 ERD Diagram
The diagram below shows all the main models and relationships:

<img width="1470" height="719" alt="Screenshot 2025-11-06 at 8 19 57 AM" src="https://github.com/user-attachments/assets/00d62b46-1779-46f9-9326-2bf062039665" />

---

## 🔷 Routing Table (Backend)
| Method | URL Pattern | Handler | Action |
|--------|-------------|---------|--------|
| GET | `/` | `Home` | Test page |
| GET | `/users/` | `UserListView` | List all users |
| GET | `/users/<int:user_id>/` | `UserDetailView` | Display user details |
| GET, POST | `/employees/` | `EmployeeListCreateView` | List all employees & Create new employee |
| GET | `/employees/<int:employee_id>/` | `EmployeeDetailView` | View specific employee |
| PUT | `/employees/<int:employee_id>/edit/` | `EmployeeUpdateView` | Update employee info |
| DELETE | `/employees/<int:employee_id>/delete/` | `EmployeeDeleteView` | Delete employee |
| GET | `/leave-types/` | `LeaveTypeListView` | List all leave types |
| PUT | `/leave-types/<int:leave_type_id>/edit/` | `LeaveTypeUpdateView` | Update leave types |
| GET, POST | `/leave-requests/` | `LeaveRequestListCreateView` | List all leave requests & Create new leave request |
| GET | `/leave-requests/<int:leave_request_id>/` | `LeaveRequestDetailView` | View leave request details |
| PUT | `/leave-requests/<int:leave_request_id>/edit/` | `LeaveRequestUpdateView` | Update leave request |
| DELETE | `/leave-requests/<int:leave_request_id>/delete/` | `LeaveRequestDeleteView` | Delete leave request |
| PATCH | `/leave-requests/<int:leave_request_id>/approve/` | `ApproveLeaveRequestView` | Approve leave request |
| PATCH | `/leave-requests/<int:leave_request_id>/reject/` | `RejectLeaveRequestView` | Reject leave request |
| PATCH | `/leave-requests/<int:leave_request_id>/pending/` | `PendingLeaveRequestView` | Pending leave request |
| GET | `/leave-balances/` | `LeaveBalanceListView` | Display all balances |
| GET | `/leave-balances/<int:employee_id>/` | `LeaveBalanceByEmployeeView` | Display employee leave balances |
| POST | `/signup/` | `SignupUserView` | User registration |
| POST | `/login/` | `TokenObtainPairView` | User login |
| POST | `/token/refresh/` | `TokenRefreshView` | Refresh access token |

---

## 🔷 IceBox Features (Future Enhancements)
**In the short term:**
- Apply **CRUD operations** to all models through the admin panel.  
- Add **updated and detailed leave balances** for all leave types and exceptions.  
- Add **interactive components** like a calendar to display each employee’s leave period.

**In the long term:**
- Expand the system to include **Human Resources management**, then **Finance management**, and later evolve into a full **ERP system**.  
- Integrate **Artificial Intelligence** to improve performance and user experience.

---

## 💻 Author
Developed by **(Manar Al Mashi)**
