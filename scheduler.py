from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to generate schedule based on tasks, deadlines, and durations
def generate_schedule(tasks):
    # Sort tasks by deadline (earliest first) and then by duration (smallest first)
    sorted_tasks = sorted(tasks, key=lambda x: (x['deadline'], x['duration']))

    # Initialize schedule
    schedule = []

    # Set initial start time
    start_time = datetime.now()

    # Iterate through tasks to calculate schedule
    for task in sorted_tasks:
        task['deadline'] = datetime.strptime(task['deadline'], '%Y-%m-%d')
        # Calculate duration until deadline
        time_until_deadline = task['deadline'] - start_time

        # Calculate the remaining time until deadline after accounting for task duration
        remaining_time_until_deadline = time_until_deadline - timedelta(hours=task['duration'])

        # If there's enough time remaining until the deadline, schedule the task
        if remaining_time_until_deadline >= timedelta(0):
            # Add task to schedule
            schedule.append({
                'task': task['name'],
                'start_time': start_time,
                'end_time': start_time + timedelta(hours=task['duration']),
                'duration': task['duration']
            })

            # Update start time for next task
            start_time += timedelta(hours=task['duration'])

    return schedule

@app.route('/schedule', methods=['POST'])
def schedule_tasks():
    # Get tasks array from request
    tasks = request.json.get('tasks')

    # Generate schedule for the tasks
    schedule = generate_schedule(tasks)

    return jsonify({'schedule': schedule})

if __name__ == '__main__':
    app.run(debug=True)
