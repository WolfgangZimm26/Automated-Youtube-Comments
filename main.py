from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
#Garrett Zimmerman
# Set up the YouTube API
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secret.json'  # Path to your client_secret.json file
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    credentials = None
    # Token.pickle stores the user's credentials from previously successful logins
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def post_comment(youtube, video_id, text):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": text
                    }
                }
            }
        }
    )
    response = request.execute()
    print(response)

if __name__ == "__main__":
    youtube = get_authenticated_service()
    video_id = "YOUR_VIDEO_ID"  # Replace with the video ID you want to comment on
    comment_text = comment_text = """
Chat with this episode and more [for FREE]: https://chat-jre.vercel.app/

Built by youtube.com/@ai-cowboy

Want a professional private chatbot: @ crestone.ai
"""  # Replace with your comment text
    post_comment(youtube, video_id, comment_text)