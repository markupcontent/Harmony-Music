import requests
import json
import re
from termcolor import colored
import functions

def searchSongs():
  song = input(colored("Add songs to the Queue ", 'cyan', attrs=['bold']) + colored("(P)lay, (S)how Queue, (B)ack, (Q)uit: ", 'red'))

  if re.match(functions.YOUTUBE_REGEX, song):
    return functions.youtubeLink(), functions.playTracksURL(song), searchSongs()

  elif re.match(functions.URL_REGEX, song):
    return functions.urlLink(), functions.playTracksURL(song), searchSongs()

  elif re.match(functions.PLAYLIST_REGEX, song):
    return functions.playlistLink(), searchSongs()

  if song.isnumeric() == True and song != "e" and song != "E" and song != "p" and song != "P":
    return functions.invalidString(), searchSongs()
    
  elif song == "q" or song == "Q":
    return functions.exitProgram()

  elif song == "b" or song == "B":
    return functions.emptyQueue(), functions.chooseOption()
      
  elif song == "p" or song == "P":
    return functions.playTracks(functions.item_list, functions.queue_list), functions.emptyQueue(), searchSongs()
      
  elif song == "s" or song == "S":
    return functions.showQueue(functions.item_list), searchSongs()
      
  return listTracks(song)
  
def listTracks(song):
  search_results = functions.getSongs(song)
  
  if re.match(functions.YOUTUBE_REGEX, song):
    return functions.youtubeLink(), functions.playTracksURL(song), searchSongs()

  elif re.match(functions.URL_REGEX, song):
    return functions.urlLink(), functions.playTracksURL(song), searchSongs()
  
  if len(search_results['items']) == 0:
    return functions.noResults(song), searchSongs()
    
  return functions.showResults(song, search_results), pickTrack(search_results, song)

def pickTrack(json, song):
  option = input(colored("\nPick an option", 'cyan', attrs=['bold']) + colored(f" [0:19, (B)ack]: ", 'red'))

  if option.isnumeric() == False and option != "b" and option != "B":
    return functions.invalidInteger(), pickTrack(json, song)
    
  elif option == "b" or option == "B":
    return print("\n"), searchSongs()

  if int(option) >= 19:
    return functions.invalidRange(), pickTrack(json, song)

  videoid = json['items'][int(option)]['url']
  title = colored(json['items'][int(option)]['title'], 'red')
  author = colored(json['items'][int(option)]['uploaderName'], 'cyan')
  return functions.addItems(videoid, title, author), searchSongs()
