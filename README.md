# CodeCraftHub ??

CodeCraftHub is a simple, personalized learning platform API where developers can track the courses they want to learn. It is built using Python and the Flask framework.

This project is specifically designed for beginners who are learning how to build and interact with REST APIs for the very first time. Instead of using a complex database, it stores all data in a simple text file (`courses.json`), making it incredibly easy to set up and understand.

---

## ?? Features

* **Complete REST API:** Includes all basic CRUD (Create, Read, Update, Delete) operations.
* **Database-Free Storage:** Uses a simple `courses.json` file to store data.
* **Auto-Generating IDs:** Automatically assigns unique IDs to new courses.
* **Input Validation:** Ensures required fields are provided and checks for valid course statuses.
* **Error Handling:** Returns clear, beginner-friendly error messages (e.g., if a course isn't found).
* **Zero Authentication Required:** Focus purely on how APIs send and receive data.

---

## ?? Project Structure

Here is how the files in this project are organized:

```text
CodeCraftHub/
+-- app.py             # The main Python file containing the Flask server and API routes
+-- courses.json       # Your local "database" (auto-generated when you add your first course)
+-- requirements.txt   # (Optional) Lists the Python packages needed to run the app
+-- README.md          # This documentation file