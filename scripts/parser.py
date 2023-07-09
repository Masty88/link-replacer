import csv
from bs4 import BeautifulSoup
import re

# Open the HTML file and parse it
with open('group_leader.html', 'r') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Open a new CSV file for writing
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Find all <tr> tags
    trs = soup.find_all('tr')

    # For each <tr> tag, find the corresponding <td> tags
    for tr in trs:
        tds = tr.find_all('td')

        # Initialize the row
        row = [''] * 4

        for td in tds:
            # Check for 'checkbox' and get its value /node/value
            if 'views-field-entity-browser-select' in td.get('class', []):
                checkbox = td.find('input', type='checkbox')
                if checkbox:
                    node_value = checkbox.get('value')
                    if node_value:
                        row[0] = '/node/' + node_value.split(':')[1]

            # Check for 'views-field-title' and write its <a> content
            if 'views-field-title' in td.get('class', []):
                link = td.find('a')
                if link:
                    row[1] = link.text

            # Check for 'views-field-field-group-leader' and write its content
            if 'views-field-field-group-leader' in td.get('class', []):
                row[2] = td.text.strip()

            # Check for 'views-field-field-city' and write its <a> content
            if 'views-field-field-city' in td.get('class', []):
                link = td.find('a')
                if link:
                    row[3] = link.text

        # Write the row to CSV
        writer.writerow(row)
