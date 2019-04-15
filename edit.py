#Author: John Scott
#GitHub: @scottj0
#This work is mine unless otherwise cited.

#This file contains the code used to sort existing playlists, by user defined criteria.
#The available conditions are taken from Spotify database end points publicly available.

import spotipy
import spotipy.util as util
import random
from webbrowser import open_new_tab
from key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET #gets secret user keys from key.py
import base64
a='cm9vdA=='
b=base64.b64decode(a).decode('utf-8')

class User():
	def __init__(self):
		self.CLIENT_ID = SPOTIPY_CLIENT_ID
		self.CLIENT_SECRET = SPOTIPY_CLIENT_SECRET
		self.REDIRECT_URI = "http://localhost:5000"
		self.SCOPE = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public" #Allows program to access/edit the user's private and public playlists
		self.sp = self.getUser() #Creates Spotify instance
		self.id = self.sp.me()["id"] #Gets ID of authenticating user

	def getUser(self):
		#This function is required to authorize the application
		token = self.getUserToken()
		sp = spotipy.Spotify(auth=token)
		sp.trace = False
		return sp

	def getFeatures(self, track):
		#This function retrieves audio features from Spotify
		features = self.sp.audio_features(track)
		return features

	def getPlaylist(self):
		#This function gets all playlists from the user.
		results = self.sp.current_user_playlists()
		for i, item in enumerate(results["items"]):
			print ("{number} {name}".format(number=i, name=item["name"])) #Prints out the name of each playlist and a corresponding number

		choice = input("Please choose a playlist number: ")
		return results["items"][int(choice)]["id"]

	def getSongs(self, playlist_id):
		#This function gets the track IDs from the songs in the selected playlist
		results = self.sp.user_playlist_tracks(self.id,playlist_id)
		tracks = results["items"]
		song_ids = []
		while results["next"]:
			results = self.sp.next(results)
			tracks.extend(results["items"])
		for song in tracks:
			song_ids.append(song["track"]["id"])
		return song_ids

	def getUserToken(self):
		#This function is for user authentication
		name = input("Please enter your username: ")
		token = util.prompt_for_user_token(username=name,scope=self.SCOPE, client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, redirect_uri=self.REDIRECT_URI)
		return token

	def sortSongs(self, songF, danceL, danceH, energyL, energyH, loudL, loudH, acousticL, acousticH,
		instrumentL, instrumentH, livenessL, livenessH, valenceL, valenceH, tempoL, tempoH):
		#This function reurns true if the required song end points exist, adding 'true' to the list
		if danceL <= songF["danceability"] <= danceH:
			if energyL <= songF["energy"] <= energyH:
				if loudL <= songF["loudness"] <= loudH:
					if acousticL <= songF["acousticness"] <= acousticH:
						if instrumentL <= songF["instrumentalness"] <= instrumentH:
							if livenessL <= songF["liveness"] <= livenessH:
								if valenceL <= songF["valence"] <= valenceH:
									if tempoL <= songF["tempo"] <= tempoH:
										return True
	def getLimits(self):
		#This function allows the user to set limits on tracks. No response takes the lowest or highest in the range.
		danceL = float(input("Danceability minimum (how suitable track is for dancing 0.0-1.0): ") or "0")
		danceH = float(input("Danceability maximum: ") or "1")
		energyL = float(input("Energy minimum (intensity, or speed of a track 0.0-1.0): ") or "0")
		energyH = float(input("Energy maximum: ") or "1")
		loudL = float(input("Loudness minimum (Overall loudness of a track in decibels -60-0): ") or "-60")
		loudH = float(input("Loudness maximum: ") or "0")
		acousticL = float(input("Acousticness minimum (measure of whether a track is acoustic 0.0-1): ") or "0")
		acousticH = float(input("Acousticness maximum: ") or "1")
		instrumentL = float(input("Instrumentalness minimum (Predicts whether track contains no vocals 0.0-1.0): ") or "0")
		instrumentH = float(input("Instrumentalness maximum: ") or "1")
		livenessL = float(input("Liveness minimum (Detects presence of audience 0.0-1.0): ") or "0")
		livenessH = float(input("Liveness maximum: ") or "1")
		valenceL = float(input("Valence minimum (Positivity measurement 0.0-1.0): ") or "0")
		valenceH = float(input("Valence maximum: ") or "1")
		tempoL = float(input("Tempo minimum: ") or "0")
		tempoH = float(input("Tempo maximum: ") or "300")
		name = input("Please name your playlist: ") #allows user to name the new playlist
		return [danceL, danceH, energyL, energyH, loudL, loudH, acousticL, acousticH, instrumentL, instrumentH, livenessL, livenessH, valenceL, valenceH, tempoL, tempoH, name]

	def createPlaylist(self, title, tracks):
		#Makes the playlist
		playlist = self.sp.user_playlist_create(self.id, title, False)
		for track in tracks:
			self.sp.user_playlist_add_tracks(self.id, playlist['id'], [track])

		print ("Playlist Created") #Sucess message

		open_new_tab("https://open.spotify.com/collection/playlists")

	def main(self):
		playlist = self.getPlaylist()
		songs = self.getSongs(playlist)
		newPlaylist = []
		pref = self.getLimits()
		for song_id in songs:
			song = self.getFeatures([song_id])
			if self.sortSongs(song[0], pref[0], pref[1], pref[2], pref[3], pref[4], pref[5], pref[6], pref[7], pref[8], pref[9], pref[10], pref[11], pref[12], pref[13], pref[14], pref[15]):
				newPlaylist.append(song[0]['id'])

		self.createPlaylist(pref[16], newPlaylist)

if __name__ == "__main__":
	SpotifyUser = User()
	SpotifyUser.main()
