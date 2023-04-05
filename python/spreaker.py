import sys
import requests
from pydub import AudioSegment
import tempfile

if len(sys.argv) < 2:
    print("Usage: python script.py <starting_show_id>")
    sys.exit(1)

show_id = int(sys.argv[1])
found = False

while not found:
    url = f'https://api.spreaker.com/v2/shows/{show_id}/episodes'
    response = requests.get(url)

    if response.status_code == 200:
        json_response = response.json()

        if len(json_response['response']['items']) >= 3:
            first_item_download_url = json_response['response']['items'][0]['download_url']

            # Download the audio file
            print("Downloading the first episode...")
            audio_response = requests.get(first_item_download_url)

            # Save the downloaded file to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(audio_response.content)
                temp_file.flush()

            # Load the audio file
            audio = AudioSegment.from_file(temp_file.name, format="mp3")
            audio_length_minutes = audio.duration_seconds / 60

            if audio_length_minutes > 60:
                found = True
                print(f"Show ID {show_id} has at least 3 episodes:")
                print(f"First episode's length: {audio_length_minutes:.2f} minutes")
                print(f"URL used: {url}")
            else:
                print(f"{show_id}: Short episode.")
                show_id += 1
        else:
            print(f"{show_id}: Less than 3 episodes.")
            show_id += 1
    else:
        print(f"{show_id}: N/A.")
        show_id += 1

