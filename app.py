from flask import Flask, render_template, jsonify, request, session
import webbrowser
import threading
import os

app = Flask(__name__, static_url_path='', static_folder='.')  # Adjusted to serve static files
app.secret_key = 'your_secret_key'  # Required for session management

# Simulated data for companies
company_data = {
    'google': {
        'employees': [
            {'name': 'John Doe', 'role': 'Software Engineer', 'linkedin': 'https://linkedin.com/johndoe'},
            {'name': 'Jane Smith', 'role': 'Data Scientist', 'linkedin': 'https://linkedin.com/janesmith'}
        ],
        'interview_process': '3 rounds: 1 coding, 1 system design, 1 HR',
        'gfg_links': 'https://www.geeksforgeeks.org/tag/google/',
        'eligibility': 'Minimum 7 CGPA, no active backlogs.',
        'technologies': 'Python, Machine Learning, Distributed Systems'
    },
    'amazon': {
        'employees': [
            {'name': 'Alice Brown', 'role': 'Backend Engineer', 'linkedin': 'https://linkedin.com/alicebrown'},
            {'name': 'Bob White', 'role': 'DevOps Engineer', 'linkedin': 'https://linkedin.com/bobwhite'}
        ],
        'interview_process': '4 rounds: 2 coding, 1 system design, 1 HR',
        'gfg_links': 'https://www.geeksforgeeks.org/tag/amazon/',
        'eligibility': 'Minimum 6.5 CGPA, no active backlogs.',
        'technologies': 'Java, AWS, Microservices'
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/get_response', methods=['POST'])
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get('message').strip().lower()

    # Check if user is asking about a company
    matched_company = None
    for company in company_data:
        if company in user_message:
            matched_company = company
            break

    if matched_company:
        session['selected_company'] = matched_company  # Store selected company in session
        return jsonify({
            'reply': f"Welcome! You asked about {matched_company.capitalize()}.",
            'options': [
                {'text': 'Employees', 'value': '1'},
                {'text': 'Interview Process', 'value': '2'},
                {'text': 'Interview Preparation', 'value': '3'},
                {'text': 'Eligibility Criteria', 'value': '4'},
                {'text': 'Technologies', 'value': '5'}
            ]
        })

    selected_company = session.get('selected_company')
    if selected_company:
        if user_message.startswith('1'):
            employees = company_data[selected_company]['employees']
            employee_names = ', '.join([emp['name'] for emp in employees])
            return jsonify({'reply': f"Employees: {employee_names}. If you need more details, type 'I need [Employee Name] info'."})

        elif user_message.startswith('2'):
            return jsonify({'reply': company_data[selected_company]['interview_process']})

        elif user_message.startswith('3'):
            gfg_link = company_data[selected_company]['gfg_links']
            return jsonify({'reply': f"Here are some interview preparation resources: <a href='{gfg_link}' target='_blank'>Click here</a>."})

        elif user_message.startswith('4'):
            return jsonify({'reply': company_data[selected_company]['eligibility']})

        elif user_message.startswith('5'):
            return jsonify({'reply': company_data[selected_company]['technologies']})

        # Check if the user is asking for specific employee information
        for emp in company_data[selected_company]['employees']:
            if emp['name'].lower() in user_message:
                return jsonify({
                    'reply': f"Employee Name: {emp['name']}\nRole: {emp['role']}\nLinkedIn: <a href='{emp['linkedin']}' target='_blank'>LinkedIn Profile</a>"
                })

        return jsonify({'reply': 'Sorry, I didn\'t understand that option.'})

    return jsonify({'reply': 'Sorry, I didn\'t understand. Please provide a valid company name or option.'})



def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Open browser only if use_reloader is False (to prevent it from opening twice)
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.25, open_browser).start()

    # Run the app
    app.run(debug=True, use_reloader=False)
