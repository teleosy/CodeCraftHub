from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)

# Constants
DATA_FILE = 'courses.json'
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]
REQUIRED_FIELDS = ["name", "description", "target_date", "status"]

# ==========================================
# HELPER FUNCTIONS (Database Simulation)
# ==========================================

def read_courses():
    """Reads course data from the JSON file. Creates it if it doesn't exist."""
    # Check if the file exists; if not, return an empty list
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r') as file:
            # Handle empty files gracefully
            content = file.read()
            if not content.strip():
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        # If the file is corrupted or unreadable, log it and return an empty list or error
        print(f"Error reading {DATA_FILE}: {e}")
        return []

def write_courses(data):
    """Writes the list of courses back to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except IOError as e:
        print(f"Error writing to {DATA_FILE}: {e}")
        return False

# ==========================================
# API ENDPOINTS
# ==========================================

@app.route('/api/courses', methods=['POST'])
def create_course():
    """Creates a new course."""
    new_course = request.get_json()

    # 1. Error Handling: Check for missing payload
    if not new_course:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # 2. Error Handling: Check for missing required fields
    missing_fields = [field for field in REQUIRED_FIELDS if field not in new_course]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    # 3. Error Handling: Validate status value
    if new_course['status'] not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 400

    courses = read_courses()

    # 4. Auto-generate ID and timestamp
    new_id = 1 if len(courses) == 0 else max(course['id'] for course in courses) + 1
    new_course['id'] = new_id
    new_course['created_at'] = datetime.now().isoformat()

    # Save to "database"
    courses.append(new_course)
    if not write_courses(courses):
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify({"message": "Course created successfully", "course": new_course}), 201


@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """Retrieves all courses."""
    courses = read_courses()
    return jsonify(courses), 200


@app.route('/api/courses/stats', methods=['GET'])
def get_course_stats():
    """Returns statistics about all courses."""
    courses = read_courses()
    
    # Initialize the statistics dictionary
    stats = {
        "total_courses": len(courses),
        "status_counts": {
            "Not Started": 0,
            "In Progress": 0,
            "Completed": 0
        }
    }
    
    # Count the courses by status
    for course in courses:
        status = course.get('status')
        # Only increment if the status is one of our valid keys
        if status in stats["status_counts"]:
            stats["status_counts"][status] += 1
            
    return jsonify(stats), 200


@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Retrieves a single course by its ID."""
    courses = read_courses()
    
    # Search for the course
    for course in courses:
        if course['id'] == course_id:
            return jsonify(course), 200
            
    # Error Handling: Course not found
    return jsonify({"error": f"Course with ID {course_id} not found"}), 404


@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Updates an existing course."""
    updated_data = request.get_json()
    
    if not updated_data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Validate status if the user is trying to update it
    if 'status' in updated_data and updated_data['status'] not in VALID_STATUSES:
         return jsonify({"error": f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}"}), 400

    courses = read_courses()
    course_found = False

    # Find the course and apply updates
    for course in courses:
        if course['id'] == course_id:
            course_found = True
            
            # Update fields only if they are present in the request
            course['name'] = updated_data.get('name', course.get('name'))
            course['description'] = updated_data.get('description', course.get('description'))
            course['target_date'] = updated_data.get('target_date', course.get('target_date'))
            course['status'] = updated_data.get('status', course.get('status'))
            
            break # Exit the loop since we found the course

    # Error Handling: Course not found
    if not course_found:
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404

    # Save changes
    if not write_courses(courses):
        return jsonify({"error": "Failed to save updated course data"}), 500

    # Return the updated course
    updated_course = next(c for c in courses if c['id'] == course_id)
    return jsonify({"message": "Course updated successfully", "course": updated_course}), 200


@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Deletes a course by its ID."""
    courses = read_courses()
    
    # Filter the list to keep only the courses that DO NOT match the target ID
    filtered_courses = [course for course in courses if course['id'] != course_id]
    
    # Error Handling: If the lengths are the same, the ID wasn't found
    if len(courses) == len(filtered_courses):
        return jsonify({"error": f"Course with ID {course_id} not found"}), 404
        
    # Save the new list (which no longer contains the deleted course)
    if not write_courses(filtered_courses):
        return jsonify({"error": "Failed to delete course data"}), 500

    return jsonify({"message": f"Course with ID {course_id} deleted successfully"}), 200


# ==========================================
# APP EXECUTION
# ==========================================
if __name__ == '__main__':
    # debug=True allows the server to auto-reload when you make code changes
    app.run(debug=True, port=5000)