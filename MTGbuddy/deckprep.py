import os
import time
import re
from requests import get
from json import loads
from shutil import copyfileobj

# Parses deck list in MTGO format (moxfield) and returns an array of each unique card
def parseDeckList(deckList):
    # Split the input data into lines
    lines = deckList.strip().split('\n')

    # Initialize an empty card list
    cards = []

    # Iterate over each line and parse the card name
    for line in lines:
        if line.strip():
            # Remove leading numbers and any following spaces
            card_name = re.sub(r'^\d+\s+', '', line)
            cards.append(card_name)

    return cards

# Uses the scryfall API to get an image of the desired card
def getCardImg(cardName):
    # Get card date
    response = get(f"https://api.scryfall.com/cards/search?q={cardName}")

    if response.status_code != 200:
        print(f"request failed with status code: {response.status_code}")

    card = loads(response.text)

    if 'data' not in card:
        print("No 'data' key found in the response.")
        return
    card_data = card['data'][0]
    if 'image_uris' in card_data:
        img_url = card['data'][0]['image_uris']['normal']
    elif 'card_faces' in card_data: # Special case of double-faced cards, get the first face
        img_url = card_data['card_faces'][0]['image_uris']['normal']
    else:
        print("No 'image_uris' found in the card data")
        return
    
    # Save the image
    fileName = f"{cardName}.jpeg"
    dirPath = 'C:/Users/aeggs/Documents/personalProjs/MTGbuddy/cardquery'
    filePath = os.path.join(dirPath, fileName)
    with open(filePath, 'wb') as out_file:
        copyfileobj(get(img_url, stream = True).raw, out_file)
    time.sleep(0.075)    # Add a 50-100 ms delay paer request

def saveDeckImgs(deckList):
    for card in deckList:
        getCardImg(card)

test_list = """ 1 Academy Manufactor
1 Apex of Power
1 Arcane Signet
1 Bag of Devouring
1 Bedevil
1 Birgi, God of Storytelling
1 Bituminous Blast
1 Bojuka Bog
1 Bonecrusher Giant
1 Chandra, Torch of Defiance
1 Chaos Channeler
1 Chaos Wand
1 Chaos Warp
1 Command Tower
1 Commander's Sphere
1 Commune with Lava
1 Consuming Vapors
1 Danse Macabre
1 Dark-Dweller Oracle
1 Dead Man's Chest
1 Dire Fleet Daredevil
1 Disciple of the Vault
1 Disrupt Decorum
1 Dream Devourer
1 Dual Strike
1 Ebony Fly
1 Etali, Primal Storm
1 Exotic Orchard
1 Fellwar Stone
1 Fevered Suspicion
1 Fiend of the Shadows
1 Foreboding Ruins
1 Gonti, Lord of Luxury
1 Grim Hireling
1 Hurl Through Hell
1 Ignite the Future
1 Light Up the Stage
1 Lorcan, Warlock Collector
1 Loyal Apprentice
1 Marionette Master
1 Mind Stone
1 Mortuary Mire
13 Mountain
1 Murderous Rider
1 Nadier's Nightblade
1 Orazca Relic
1 Outpost Siege
1 Poison the Cup
1 Rakdos Carnarium
1 Rakdos Charm
1 Rakdos Signet
1 Reckless Fireweaver
1 Rise of the Dread Marn
1 Shadowblood Ridge
1 Smoldering Marsh
1 Sol Ring
1 Spinerock Knoll
14 Swamp
1 Tainted Peak
1 Talisman of Indulgence
1 Tectonic Giant
1 Terminate
1 Theater of Horrors
1 Throes of Chaos
1 Underdark Rift
1 Unstable Obelisk
1 Valakut Exploration
1 Valki, God of Lies
1 Vandalblast
1 Warlock Class
1 Wild-Magic Sorcerer
1 Xorn
1 You Find Some Prisoners
1 Zhalfirin Void

1 Prosper, Tome-Bound """

# getCardImg('Birgi God of Storytelling')

cards = parseDeckList(test_list)
print(cards)
saveDeckImgs(cards)