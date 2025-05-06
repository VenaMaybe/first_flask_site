from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

bp = Blueprint('tt', __name__)
last_state_time = datetime.now()

### Time tracker
@bp.route('/')
def time_tracker():
	return render_template('time-tracker.html')

@bp.route('/state', methods=['POST'])
def time_tracker_state_update():
	global last_state_time

	state = request.get_json().get('state')
	current_state_time = datetime.now()

	difference_state_time = current_state_time - last_state_time;

	# Extract hours, minutes, and seconds from the timedelta
	total_seconds = difference_state_time.total_seconds()
	hours, remainder = divmod(total_seconds, 3600)
	minutes, seconds = divmod(remainder, 60)

	# Format the difference as HH:MM:SS
	formatted_difference = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

	print(state, datetime.now().strftime("%I:%M:%S %p"), ' difference: ', formatted_difference)

	last_state_time = datetime.now()
	return jsonify({"status": "state changed", "time_difference": formatted_difference})
