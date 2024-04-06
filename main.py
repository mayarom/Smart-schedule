from urllib.parse import unquote_plus

from flask import Flask, render_template, request, redirect, url_for
from Class import Class  # Make sure this import is correct
import json

app = Flask(__name__)

teachers = []
classes = []  # This will now hold instances of Class

# Define available subjects here
available_subjects = ["מתמטיקה", "פיזיקה", "כימיה", "ביולוגיה", "היסטוריה", "ספרות", "אומנות", "מדעי המחשב"]
available_days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי"]

@app.route('/')
def index():
    # Convert each Class instance into a dictionary for easier handling in the template
    classes_for_template = [
        {
            'name': class_instance.name,
            'subjects_hours': class_instance.subjects_hours_fixed  # Assuming you want to display this
            # You can add more fields as needed
        }
        for class_instance in classes
    ]
    return render_template('index.html', teachers=teachers, classes=classes_for_template,
                           available_subjects=available_subjects, available_days=available_days)



@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form.get('name')
    # במקום .split(',') נשתמש ב-getlist כדי לקבל את הבחירות מהטופס
    subjects = request.form.getlist('subjects')
    weekly_hours = int(request.form.get('weekly_hours'))
    free_day = request.form.get('free_day')
    teachers.append({'name': name, 'subjects': subjects, 'weekly_hours': weekly_hours, 'free_day': free_day})
    return redirect(url_for('index'))


@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    class_name = request.form['class_name']  # Assuming class_name is passed in the body of a POST request

    # Find the class object by name
    class_obj = next((c for c in classes if c.name == class_name), None)
    if class_obj is None:
        return 'Class not found', 404

    # Attempt to generate the schedule
    success = class_obj.build_schedule_for_class()
    if success:
        return 'Schedule generated successfully', 200
    else:
        return 'Failed to generate schedule', 500


@app.route('/add_class', methods=['POST'])
def add_class():
    name = request.form.get('name')
    # Dictionary to hold subjects and their weekly hours
    subjects_hours = {}

    # Iterate over available subjects to see if they were included in the form submission
    for subject in available_subjects:
        hours = request.form.get(subject)
        if hours:  # If hours were entered for this subject
            # Convert the string input to an integer
            subjects_hours[subject] = int(hours)

    # Create a new Class object with the provided name and subjects_hours
    new_class = Class(name, subjects_hours)

    # Add the new class to the global classes list
    classes.append(new_class)

    # Redirect the user back to the homepage after adding the class
    return redirect(url_for('index'))


@app.route('/class_schedule/<class_name>')
def class_schedule(class_name):
    class_name = unquote_plus(class_name)
    class_obj = next((c for c in classes if c.name == class_name), None)
    if class_obj is None:
        return f"Class {class_name} not found.", 404
    schedule = class_obj.get_schedule_as_list()
    # Get the transposed schedule
    transposed_schedule = class_obj.get_transposed_schedule()

    # Render the template with the transposed schedule
    return render_template('class_schedule.html', class_name=class_name, transposed_schedule=transposed_schedule)


if __name__ == '__main__':
    app.run(debug=True)
