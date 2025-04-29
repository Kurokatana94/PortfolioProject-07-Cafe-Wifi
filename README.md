# Cafe & Wifi
### Work-Friendly Café Directory
A Flask-based web application that allows users to discover and share cafés suitable for remote work.

## Project Overview
This platform helps remote workers find cafés that are friendly for working — offering key amenities like Wi-Fi, 
power sockets, and quiet spaces. 
Registered users can post their own café finds, complete with helpful info such as seat availability and coffee pricing.

## Features
- **User Authentication**: Register, log in, and log out securely.

![image](https://github.com/user-attachments/assets/c57dd966-607b-42bb-a8ab-727cc938ec2b)

- **Post Cafés**:
  - Share cafés that allow remote work, including:
  - Number of seats
  - Price of a coffee
  - Availability of Wi-Fi, power sockets, toilets
  - Whether calls are allowed

![cafe_wifi_preview](https://github.com/user-attachments/assets/72ab0c37-e166-4704-ae2e-dee801ec2988)

- **Responsive Directory**:
  - Posts are displayed as Bootstrap cards, styled to show the necessary data.
  - Edit/Delete Controls: Users can modify or delete their own posts. Admins have full control (The admin will be the first user to be created).

![image](https://github.com/user-attachments/assets/d26abec8-03f2-4893-bcdf-037c502c7960)

- **Persistent Storage**:
  - All data is stored in a connected database.

- **Built With**:
  - Flask (Python)
  - HTML & Jinja templates
  - Custom CSS & Bootstrap

## How to Run the Project Locally
This project is not deployed online, but it can be run locally for testing or portfolio review.
1. **Clone the repository**
```
git clone https://github.com/yourusername/cafe-directory.git
cd PortfolioProject-07-Cafe-Wifi
```
2. **Change the line 39 in main.py**
```
app.config['SECRET_KEY'] = "Insert your key here"  <---- It can be anything you want
```
3. **Install the required packages**
```
pip install -r requirements.txt
```
4. **Run the Flask app**
```
python main.py
```
5. **Open in your browser**
```
http://127.0.0.1:5000

```
## **Note**
- The SQLite database is included with sample café data.
- There is just one preloaded — email:`admin@email.com` password:`admin`.

### Thanks for Checking It Out!

Feel free to **download**, **modify**, and **use** this project however you'd like.
Feedback or suggestions are always welcome!
 
