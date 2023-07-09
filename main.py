# import tkinter as tk
# from tkinter import scrolledtext, filedialog
# import pandas as pd
# from bs4 import BeautifulSoup
# import re
#
# df = pd.DataFrame()  # Inizializza il DataFrame
#
#
# def load_csv():
#     global df
#     filepath = filedialog.askopenfilename()
#     df = pd.read_csv(filepath)
#     df = pd.read_csv(filepath)
#     df['Joomla Link'] = df['Joomla Link'].str.strip()
#     if filepath:
#         try:
#             df = pd.read_csv(filepath)
#             print("File loaded successfully")
#             print(f"Loaded file: {filepath}")
#         except Exception as e:
#             print(f"An error occurred: {e}")
#
#
# def show_text():
#     global df
#     if df.empty:
#         print("Il file CSV non è stato caricato.")
#         return
#     original_html = text_area1.get('1.0', tk.END)
#     soup = BeautifulSoup(original_html, 'html.parser')
#     missing_links = []
#     changed_links = []
#     for a in soup.find_all('a', href=True):
#         href = a['href']
#         if href.startswith('https://www.sib.swiss'):
#             link_parts = href.split('https://www.sib.swiss')
#             if len(link_parts) > 1:
#                 joomla_link = 'https://www.sib.swiss' + link_parts[1]  # Prendi il secondo elemento della lista
#                 print(f"Looking for: {joomla_link}")  # Aggiungi questa riga
#                 if joomla_link in df['Joomla Link'].values:
#                     new_link = df.loc[df['Joomla Link'] == joomla_link, 'Node'].values[0]
#                     changed_links.append(f'{href} -> {new_link}')
#                     a['href'] = new_link
#                 else:
#                     missing_links.append(href)
#                     missing_links.append(href)
#     if missing_links:
#         text_area2.insert('1.0', 'NOT FOUND:\n')
#         for link in missing_links:
#             text_area2.insert(tk.END, f'{link}\n')
#     for link in changed_links:
#         text_area3.insert(tk.END, f'{link}\n')
#     text_area3.insert(tk.END, str(soup))
#
#
# def close_window():
#     root.destroy()
#
#
# root = tk.Tk()
# root.geometry('800x680')
# root.title("HTML Input")
#
# root.protocol("WM_DELETE_WINDOW", close_window)
#
# # Create frame for first editor
# frame1 = tk.Frame(root)
# frame1.pack(side='top', padx=10, pady=5, fill='x')
#
# # Create label
# label1 = tk.Label(frame1, text="Original HTML")
# label1.pack()
#
# # Create text area
# text_area1 = scrolledtext.ScrolledText(frame1, height=10)
# text_area1.pack(fill='x', expand=True)
#
# # Create frame for second editor
# frame2 = tk.Frame(root)
# frame2.pack(side='top', padx=10, pady=5, fill='x')
#
# # Create label
# label2 = tk.Label(frame2, text="NOT FOUND")
# label2.pack()
#
# # Create text area
# text_area2 = scrolledtext.ScrolledText(frame2, height=10)
# text_area2.pack(fill='x', expand=True)
#
# # Create frame for third editor
# frame3 = tk.Frame(root)
# frame3.pack(side='top', padx=10, pady=5, fill='x')
#
# # Create label
# label3 = tk.Label(frame3, text="Changed links")
# label3.pack()
#
# # Create text area
# text_area3 = scrolledtext.ScrolledText(frame3, height=10)
# text_area3.pack(fill='x', expand=True)
#
# # Create frame for buttons
# frame_buttons = tk.Frame(root)
# frame_buttons.pack(side='top', pady=10)
#
# # Create button
# load_button = tk.Button(frame_buttons, text="Load CSV", command=load_csv)
# load_button.pack(side='left', padx=3)
#
# # Create button
# show_button = tk.Button(frame_buttons, text="Show Text", command=show_text)
# show_button.pack(pady=5)
#
# root.mainloop()

import tkinter as tk
from tkinter import scrolledtext, filedialog
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

df = pd.DataFrame()  # Inizializza il DataFrame


def load_csv():
    global df
    filepath = filedialog.askopenfilename()
    if filepath:
        try:
            df = pd.read_csv(filepath)
            df['Joomla Link'] = df['Joomla Link'].str.strip()
            print("File loaded successfully")
            print(f"Loaded file: {filepath}")
        except Exception as e:
            print(f"An error occurred: {e}")


def show_text():
    global df
    if df.empty:
        print("Il file CSV non è stato caricato.")
        return
    original_html = text_area1.get('1.0', tk.END)
    soup = BeautifulSoup(original_html, 'html.parser')
    missing_links = []
    changed_links = []
    checked_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('https://www.sib.swiss'):
            link_parts = href.split('https://www.sib.swiss')
            if len(link_parts) > 1:
                joomla_link = 'https://www.sib.swiss' + link_parts[1]  # Prendi il secondo elemento della lista
                print(f"Looking for: {joomla_link}")  # Aggiungi questa riga
                if joomla_link in df['Joomla Link'].values:
                    new_link = df.loc[df['Joomla Link'] == joomla_link, 'Node'].values[0]
                    changed_links.append(f'{href} -> {new_link}')
                    a['href'] = new_link
                else:
                    missing_links.append(href)
        else:
            print("cecking")
            try:
                response = requests.get(href)
                checked_links.append(f'{href} -> {response.status_code}')
                print(f'Checked link: {href} -> {response.status_code}')
            except requests.exceptions.RequestException as e:
                checked_links.append(f'{href} -> Error: {e}')
                print(f'Checked link: {href} -> Error: {e}')

    text_area1.delete('1.0', tk.END)  # Svuota la finestra di testo 1
    text_area1.insert(tk.END, str(soup))

    text_area2.delete('1.0', tk.END)  # Svuota la finestra di testo 2
    if missing_links:
        text_area2.insert('1.0', 'NOT FOUND:\n')
        for link in missing_links:
            text_area2.insert(tk.END, f'{link}\n')

    text_area3.delete('1.0', tk.END)  # Svuota la finestra di testo 3
    for link in changed_links:
        text_area3.insert(tk.END, f'{link}\n')

    text_area4.delete('1.0', tk.END)  # Svuota la finestra di testo 4
    for link in checked_links:
        text_area4.insert(tk.END, f'{link}\n')


def close_window():
    root.destroy()


root = tk.Tk()
root.geometry('850x750')
root.title("HTML Input")

root.protocol("WM_DELETE_WINDOW", close_window)

label1 = tk.Label(root, text="Original HTML")
label1.grid(row=0, column=0)
text_area1 = scrolledtext.ScrolledText(root, height=20, width=50)
text_area1.grid(row=1, column=0)

label2 = tk.Label(root, text="NOT FOUND")
label2.grid(row=0, column=1)
text_area2 = scrolledtext.ScrolledText(root, height=20, width=50)
text_area2.grid(row=1, column=1)

label3 = tk.Label(root, text="Changed links")
label3.grid(row=2, column=0)
text_area3 = scrolledtext.ScrolledText(root, height=20, width=50)
text_area3.grid(row=3, column=0)

label4 = tk.Label(root, text="Checked links")
label4.grid(row=2, column=1)
text_area4 = scrolledtext.ScrolledText(root, height=20, width=50)
text_area4.grid(row=3, column=1)

frame_buttons = tk.Frame(root)
frame_buttons.grid(row=4, column=0, columnspan=2)

load_button = tk.Button(frame_buttons, text="Load CSV", command=load_csv)
load_button.pack(side='left', padx=5, pady=10)

show_button = tk.Button(frame_buttons, text="Show Text", command=show_text)
show_button.pack(side='right', padx=5, pady=10)

root.mainloop()
