import requests
import json
import re
from termcolor import colored
import functions

def searchPlaylists():
  playlist = input(colored("\nAdd playlists to the Queue ", 'cyan', attrs=['bold']) + colored("(P)lay, (S)how Queue, (B)ack, (Q)uit: ", 'red'))

  if re.match(functions.URL_REGEX, playlist):
    return functions.playlistLink(), searchPlaylists()

  if playlist.isnumeric() == True:
    return functions.invalidInput(), searchPlaylists()
    
  elif playlist == "q" or playlist == "Q":
    return functions.exitProgram()

  elif playlist == "b" or playlist == "B":
    return functions.emptyQueue(), functions.chooseOption()
      
  elif playlist == "p" or playlist == "P":
    return functions.playTracks(functions.item_list, functions.queue_list), functions.emptyQueue(), searchPlaylists()
      
  elif playlist == "s" or playlist == "S":
    return functions.showQueue(functions.item_list), searchPlaylists()
      
  return listPlaylists(playlist)
  
def listPlaylists(playlist):
  search_results = functions.getPlaylists(playlist)
  
  if re.match(functions.URL_REGEX, playlist):
    return functions.playlistLink(), searchPlaylists()
  
  if len(search_results['items']) == 0:
    return functions.noResults(playlist), searchPlaylists()
    
  return functions.showResultsAlbumsPlaylists(playlist, search_results), pickPlaylist(search_results, playlist)

def pickPlaylist(json, playlist):
  item_length = len(json['items'])
  option = input(colored("\nPick an option", 'cyan', attrs=['bold']) + colored(f" [1:{item_length}, (B)ack, (Q)uit]: ", 'red'))

  if option.isnumeric() == False and option != "b" and option != "B" and option != "q" and option != "Q":
    return functions.invalidInput(), pickPlaylist(json, playlist)
    
  elif option == "b" or option == "B":
    return searchPlaylists()

  elif option == "q" or option == "Q":
    return functions.exitProgram()

  if int(option) > item_length or int(option) < 1:
    return functions.invalidRange(), pickPlaylist(json, playlist)

  videoid = json['items'][int(option) - 1]['url']
  title = colored(json['items'][int(option) - 1]['name'], 'red')
  author = colored(json['items'][int(option) - 1]['uploaderName'], 'cyan')
  return functions.addItems(videoid, title, author), searchPlaylists()