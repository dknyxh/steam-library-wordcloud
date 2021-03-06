from wordcloud import WordCloud
import settings
import requests
import random

api_key = settings.api_key
user_name = settings.user_name
font_path = settings.font_path

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 60)

resolve_name_request = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}".format(api_key, user_name))

# try:
steam_id = resolve_name_request.json()["response"]["steamid"]
owned_game_request = requests.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&include_appinfo=1".format(api_key, steam_id))
print(owned_game_request.text)
owned_game_request_json = owned_game_request.json()
games_owned = owned_game_request_json['response']['game_count']
games = owned_game_request_json['response']['games']

games_playtime = {}
for each_game in games:
	if 'name' in each_game:
		games_playtime[each_game['name']] = each_game['playtime_forever']

wordcloud = WordCloud(font_path = font_path, color_func=grey_color_func, width = 4096,height = 3072, max_words = 1000, min_font_size = 10, background_color = 'white').generate_from_frequencies(games_playtime)
wordcloud.to_file('output.png')
# except Exception as e:
# 	print(e)




