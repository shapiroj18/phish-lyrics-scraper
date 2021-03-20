import json
import httpx
from bs4 import BeautifulSoup


def _get_links():
	main_songs_url = "https://phish.net/song"

	with httpx.Client() as client:

		page = client.get(url = main_songs_url)
	
	soup = BeautifulSoup(page.content, 'html.parser')
 
	songs = soup.find(id="song-list")
 
	original_songs = songs.find_all('tr', class_="all originals")
 
	links = []
	for song in original_songs:
		cols = song.findAll('td')
		print("\n")
		a_tag = cols[0].a
  
		links.append(a_tag.get('href'))

	
	return links

def _get_lyrics(endpoint):
    
    song_url = "https://phish.net" + endpoint + "/lyrics"
    
    with httpx.Client() as client:
        page = client.get(url = song_url)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    try: 
    	song_name = soup.find(id="song_title_header").string
    	lyrics = soup.find_all('blockquote')[0].get_text()
     
    except IndexError:
        song_name = None
        lyrics = None
    
    return {
		'song_name': song_name,
		'lyrics': lyrics
	}
    
def get_all_lyrics() -> None:
    
    links = _get_links()
    
    lyrics_obj = []
    for link in links:
        lyrics_obj.append(_get_lyrics(link))
        
    # write to file
    with open('phish_lyrics.json', 'w') as outfile:
        json.dump(lyrics_obj, outfile)
        
def get_codey_lyrics(word_input):
    with open('phish_lyrics.json') as lyrics_file:
        data = json.load(lyrics_file)
        
        for song in data:
            if song['song_name']:
                if word_input in song['lyrics'].lower():
                    print(song['song_name'])


def main():
	# get_all_lyrics()
	get_codey_lyrics('condition')
 
if __name__ == "__main__":
	main()
