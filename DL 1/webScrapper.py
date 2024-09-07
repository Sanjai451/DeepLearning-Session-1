import requests
from bs4 import BeautifulSoup
import re 
import csv

url = "https://www.wikihow.com/Special:Randomizer"

response = requests.get(url)

html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
article_title = soup.find('title').text.strip()
print(article_title)

for count in range(4000):
    url = "https://www.wikihow.com/Special:Randomizer"

    response = requests.get(url)
 
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    article_title = soup.find('title').text.strip()
    print(article_title+" "+str(count))

    subheadings = []
    paragraphs = []
    steps = soup.find_all('div' , {'class':'step'})
    for step in steps:
        subheading_elements = step.find('b')
        if(subheading_elements is not None):
          subheading_text = subheading_elements.text.strip().replace('\n','')
          subheading_text = subheading_text.encode('ascii',errors = 'ignore').decode()
          subheading_text = re.sub(r'','',subheading_text)
          subheadings.append(subheading_text)
          subheading_elements.extract()
          for span_tag in step.find_all('span'):
              span_tag.extract()
          
          paragraph_text = step.text.strip().replace('\n','').replace(' ', ' ')
          paragraph_text = paragraph_text.encode('ascii',errors = 'ignore').decode()
          paragraph_text = re.sub(r'','',paragraph_text)
          paragraphs.append(paragraph_text)

    if(len(subheadings)):
        with open('/content/wikiHow.csv', mode='a',newline='',encoding='utf-8') as csv_file:
             writer = csv.writer(csv_file)
             for i in range(len(subheadings)):
                   writer.writerow([article_title,subheadings[i],paragraphs[i]])