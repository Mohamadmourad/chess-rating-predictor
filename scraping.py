import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from oauth2client.service_account import ServiceAccountCredentials
from countriesList import countries

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('chessplayers-d22b78d977b9.json', scope)

client = gspread.authorize(creds)

spreadsheet = client.open('chessPlayers')

sheet = spreadsheet.get_worksheet(0)

driver = webdriver.Chrome()

def get_rating(gender,country):
    data = []
    players = []
    
    if(gender == "M"):
        driver.get(f'https://ratings.fide.com/topfed.phtml?ina=1&country={country}')
    else:
        driver.get(f'https://ratings.fide.com/topfed.phtml?tops=1&ina=1&country={country}')

    tbody = driver.find_element(By.TAG_NAME, "tbody")
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append(cols[0].text)

    lines = data[2].strip().split("\n")
    lines = lines[212:]
    lines = lines[:-2]
    for line in lines:
        temp = line.split(" ")
        rating = 0
        if len(temp) == 15:
            rating = temp[10]
        elif len(temp) == 14:
            rating = temp[9]
        elif len(temp) == 17:
            rating = temp[12]
        else:
            rating = temp[11]
        print(temp)
        age = 0
        if(temp[len(temp) - 1] != ''):
            age = 2024 - int(temp[len(temp) - 1])
        
        players.append([temp[3], rating, age,gender, country])
    print(players)
    sheet.append_rows(players)

for country in countries:
    get_rating("M",country)
    with open(f"logs.txt", "a",encoding="utf-8") as file:
        file.write(f"Boys done {country}\n")
    get_rating("F",country)
    with open(f"logs.txt", "a",encoding="utf-8") as file:
        file.write(f"Girls done {country}\n")



    