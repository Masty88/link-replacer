# import pandas as pd
#
# # Leggi entrambi i file CSV
# df1 = pd.read_csv('groups_joomla_complete_2.csv')
# df2 = pd.read_csv('output.csv')
#
# # Crea una nuova colonna 'Drupal link' in df1, inizialmente vuota
# df1['Drupal link'] = ''
#
# # Estrai l'ultimo elemento dall'URL di Joomla come nome del leader del gruppo
# df1['Group Leader'] = df1['Joomla Link'].str.split('/').str[-1]
#
# # Rimuovi la parola 'group' da 'Group Leader'
# df1['Group Leader'] = df1['Group Leader'].str.replace('-group', '')
#
# # Sostituisci i trattini con gli spazi
# df1['Group Leader'] = df1['Group Leader'].str.replace('-', ' ')
#
# # Rimuovi spazi bianchi in eccesso
# df1['Group Leader'] = df1['Group Leader'].str.strip()
# df2['Group Leader'] = df2['Group Leader'].str.strip()
#
# # Converti i nomi dei leader del gruppo in minuscolo per una migliore corrispondenza
# df1['Group Leader'] = df1['Group Leader'].str.lower()
# df2['Group Leader'] = df2['Group Leader'].str.lower()
#
# # Per ogni riga in df1, cerca una corrispondenza in df2
# for i, row in df1.iterrows():
#     # Trova una riga corrispondente in df2
#     match = df2[df2['Group Leader'] == row['Group Leader']]
#
#     # Se esiste una corrispondenza, inserisci il valore del nodo nella colonna 'Drupal link'
#     if not match.empty:
#         print(f"Match found for {row['Group Leader']}: {match['Node'].values[0]}")
#         df1.at[i, 'Drupal link'] = match['Node'].values[0]
#
# # Scrive il DataFrame modificato in un nuovo file CSV
# df1.to_csv('merged_groups.csv', index=False)

import pandas as pd

# Leggi entrambi i file CSV
df1 = pd.read_csv('groups_joomla_complete_2.csv')
df2 = pd.read_csv('output.csv')

# Crea una nuova colonna 'Joomla link' in df2, inizialmente vuota
df2['Joomla link'] = ''

# Estrai l'ultimo elemento dall'URL di Joomla come nome del leader del gruppo
df1['Group Leader'] = df1['Joomla Link'].str.split('/').str[-1]

# Sostituisci '-group' con '' e '-group' con ''
df1['Group Leader'] = df1['Group Leader'].str.replace('-group', '')

# Sostituisci i trattini con gli spazi
df1['Group Leader'] = df1['Group Leader'].str.replace('-', ' ')

# Converti i nomi dei leader del gruppo in minuscolo per una migliore corrispondenza
df1['Group Leader'] = df1['Group Leader'].str.lower().str.strip()
df2['Group Leader'] = df2['Group Leader'].str.lower().str.strip()

# Per ogni riga in df2, cerca una corrispondenza in df1
for i, row in df2.iterrows():
    # Trova una riga corrispondente in df1
    match = df1[df1['Group Leader'] == row['Group Leader']]

    # Se esiste una corrispondenza, inserisci il valore del link di Joomla nella colonna 'Joomla link'
    if not match.empty:
        df2.at[i, 'Joomla Link'] = match['Joomla Link'].values[0]
        print(f"Match found for {row['Group Leader']}: {match['Joomla Link'].values[0]}")

# A questo punto, df2 ha i dati aggiornati nella colonna 'Joomla link'
# Puoi utilizzarlo per ulteriori operazioni o salvarlo in un file CSV se necessario
df2.to_csv('output_with_joomla_links.csv', index=False)

