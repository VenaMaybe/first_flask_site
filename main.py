#
# GET RID OF THIS IN DEVELOPMENT!!!! STUPID
 
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

###

from app import socketio, create_app

app = create_app()

if __name__ == "__main__":
	socketio.run(app, debug=True, host='0.0.0.0', port=5000)

