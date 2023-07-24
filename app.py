from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)
slack_token = "YOUR_SLACK_API_TOKEN"
slack_client = WebClient(token=slack_token)

@app.route('/create_channel', methods=['POST'])
def create_channel():
    channel_name = request.json.get('channel_name')
    try:
        response = slack_client.conversations_create(name=channel_name)
        return jsonify({"channel_id": response["channel"]["id"]}), 200
    except SlackApiError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    channel_id = request.json.get('channel_id')
    message = request.json.get('message')
    try:
        slack_client.chat_postMessage(channel=channel_id, text=message)
        return jsonify({"message": "Message sent successfully"}), 200
    except SlackApiError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
