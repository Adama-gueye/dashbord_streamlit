import streamlit as st
import pandas as pd ##Exploiration des données
import matplotlib.pyplot as plt  ## Graphiques
import numpy as np 
import seaborn as sns
import plotly.express as px


def main():
    st.set_page_config(page_title="Dashboard des ventes", layout="wide")
    st.markdown("""
        <style>
            .main {
                background-color: #f9f9f9;
            }
            .block-container {
                padding-top: 2rem;
            }
            .stMetric { text-align: center; }
        </style>
    """, unsafe_allow_html=True)

    #######partie 1 : Exploration de notre Dataset 
    sales=pd.read_csv('donnees_ventes_etudiants.csv', dtype={'order_id': str})
    st.title("📊 Dashboard Interactif des Ventes USA")
    # st.title("Exploration des données de ventes")
    left_column, right_column = st.columns(2)
    max_date = sales['order_date'].max()
    min_date = sales['order_date'].min()
    left_column.date_input("Start Date", value=min_date, min_value=min_date)
    right_column.date_input("End Date", value=max_date, max_value=max_date)

    st.sidebar.header("🔎 Filtres")
    region = st.sidebar.multiselect("Région", sales['Region'].unique())
    state = st.sidebar.multiselect("État", sales[sales['Region'].isin(region)]['State'].unique())
    county = st.sidebar.multiselect("County", sales[sales['State'].isin(state)]['County'].unique())
    st.sidebar.multiselect("City", sales[sales['County'].isin(county)]['City'].unique())


    state_mapping = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }
    sales['StateComplete'] = sales['State'].map(state_mapping)

    st.dataframe(sales.head())

    statut = st.sidebar.multiselect("Statut", sales["status"].unique())

    if statut:
        filtered_sales = sales[sales["status"].isin(statut)]
    else:
        filtered_sales = sales

    val1, val2, val3 = st.columns(3)
    st.markdown("## 📊 Indicateurs Clés")

    ca = (filtered_sales["price"] * filtered_sales["qty_ordered"]).sum()
    val1.metric("Chiffre d'affaire", f"{ca:,.0f} FCFA")

    clients = filtered_sales["cust_id"].nunique()
    val2.metric("Nombre de clients", clients)

    commandes = filtered_sales["order_id"].nunique()
    val3.metric("Nombre de commandes", commandes)

    sales_by_category = sales.groupby('category')['order_id'].count().reset_index()
    sales_by_category.rename(columns={'order_id': 'nb_ventes'}, inplace=True)
    st.markdown("## 🔹 Ventes par catégorie et par région")

    fig_category_sales = px.bar(
        sales_by_category,
        y='nb_ventes',
        x='category',
        orientation='v',
        title="<b>Nombre total de ventes par catégorie</b>",
        color_discrete_sequence=["#000CB8"],
        template="plotly_white"
    )

    fig_category_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    sales_by_region = sales.groupby('Region')['order_id'].count().reset_index()
    sales_by_region.rename(columns={'order_id': 'nb_ventes'}, inplace=True)

    fig_region_pie = px.pie(
        sales_by_region,
        names='Region',
        values='nb_ventes',
        title="<b>Répartition des ventes par région</b>",
        template="plotly_white"
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig_category_sales, use_container_width=True)
    col2.plotly_chart(fig_region_pie, use_container_width=True)
    st.markdown("## 🔝 Top 10 meilleurs clients")

    top_10_meilleurs_clients  = (
    sales.assign(total_value=sales["price"] * sales["qty_ordered"])
         .groupby("full_name")["total_value"]
         .sum()
         .sort_values(ascending=False)
         .head(10)
         .reset_index()
    )
    # st.dataframe(top_10_meilleurs_clients )
    fig = px.bar(top_10_meilleurs_clients , x='full_name', y='total_value', title="<b>Top 10 des meilleurs clients</b>",
                 color='total_value', color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

    fig, ax = plt.subplots()
    st.write(sns.countplot(x=sales["Gender"], data=sales, palette="Set2"))
    st.pyplot(fig)

    gender_counts = sales['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    total = gender_counts['Count'].sum()
    gender_counts['Pourcentage'] = round((gender_counts['Count'] / total) * 100, 2)
    st.markdown("## 👥 Répartition par Genre")

    fig_gender = px.bar(
        gender_counts,
        x='Gender',
        y='Count',
        text='Pourcentage',
        color='Gender',
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="<b>Répartition des clients par Genre</b>",
        template='plotly_white'
    )

    fig_gender.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_gender.update_layout(yaxis_title="Nombre de clients", xaxis_title="Genre")

    st.plotly_chart(fig_gender, use_container_width=True)
    st.markdown("## 📆 Ventes par mois")

    sales_by_category = sales.groupby('month')['total'].count().reset_index()
    fig, ax=plt.subplots()
    sns.lineplot(x='month', y='total', data=sales_by_category, ax=ax)
    ax.set_title("Nombre de ventes par mois")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # STATE_INFO # 8. Carte des ventes par état (Bonus)
    # st.subheader("Carte des Ventes par État")
    
    # # Préparation des données pour la carte
    # state_sales_data = filtered_sales.groupby('State')['price'].sum().reset_index()
    
    # # Créer un DataFrame avec tous les états pour s'assurer qu'ils sont tous inclus
    # all_states = pd.DataFrame({
    #     'State': list(STATE_INFO.keys()),
    #     'State Name': [STATE_INFO[state]['name'] for state in STATE_INFO],
    #     'Admission Date': [STATE_INFO[state]['admission'] for state in STATE_INFO],
    #     'lat': [STATE_INFO[state]['lat'] for state in STATE_INFO],
    #     'lon': [STATE_INFO[state]['lon'] for state in STATE_INFO]
    # })
    
    # # Fusionner avec les données de vente
    # state_sales = pd.merge(all_states, state_sales_data[['State', 'price']], on='State', how='left')
    # state_sales['price'] = state_sales['price'].fillna(0)
    
    # if not state_sales.empty:
    #     # Créer la carte choroplèthe de base
    #     fig_map = px.choropleth(
    #         state_sales,
    #         locations='State',  # Abréviations des états
    #         locationmode='USA-states',  # Mode de localisation pour les états américains
    #         color='price',  # Valeur à représenter
    #         scope='usa',  # Limite à la zone géographique des États-Unis
    #         hover_name='State Name',
    #         hover_data={
    #             'State': True,  # Affiche l'abréviation
    #             'Admission Date': True,
    #             'price': ':$,.2f'  # Format monétaire
    #         },
    #         color_continuous_scale=px.colors.sequential.Plasma,
    #         title='Ventes par État',
    #         labels={'price': 'Chiffre d\'affaires'}
    #     )
        
    #     # Ajouter les abréviations d'état comme annotations
    #     for i, row in state_sales.iterrows():
    #         fig_map.add_trace(
    #             go.Scattergeo(
    #                 lon=[row['lon']],
    #                 lat=[row['lat']],
    #                 text=[row['State']],
    #                 mode='text',
    #                 textfont=dict(
    #                     size=10,
    #                     color='black',
    #                     family='Arial, bold'
    #                 ),
    #                 showlegend=False,
    #                 hoverinfo='skip'
    #             )
    #         )
        
    #     # Personnalisation des info-bulles
    #     fig_map.update_traces(
    #         hovertemplate=(
    #             "<b>%{hovertext}</b><br>"
    #             "Abréviation: %{location}<br>"
    #             "CA: %{z:$,.2f}<br>"
    #             "Admission: %{customdata[1]}<extra></extra>"
    #         )
    #     )
        
    #     ### Personnalisation de la mise en page
    #     fig_map.update_layout(
    #         height=600,
    #         margin={"r": 0, "t": 40, "l": 0, "b": 0},
    #         geo=dict(
    #             lakecolor='rgb(255, 255, 255)',
    #             subunitcolor="rgb(255, 255, 255)",
    #             countrycolor="rgb(255, 255, 255)",
    #             showlakes=True,
    #             showsubunits=True,
    #             showcountries=True,
    #             bgcolor='rgba(0,0,0,0)'  # Fond transparent
    #         )
    #     )
        
    #     st.plotly_chart(fig_map, use_container_width=True)
    # else:
    #     st.warning("Aucune donnée disponible pour la carte")
    
    # ### Affichage du tableau des états avec toutes les informations
    # st.subheader("Tableau des États Américains avec Ventes")
    
    # if not state_sales.empty:
    #     ### Préparation des données pour le tableau
    #     table_data = state_sales[['State', 'State Name', 'Admission Date', 'price']].copy()
    #     table_data.rename(columns={
    #         'State': 'Abréviation',
    #         'State Name': 'État',
    #         'Admission Date': 'Date d\'admission',
    #         'price': 'Chiffre d\'affaires'
    #     }, inplace=True)
        
    #     ### Formatage du chiffre d'affaires
    #     table_data['Chiffre d\'affaires'] = table_data['Chiffre d\'affaires'].apply(lambda x: f"${x:,.2f}")
        
    #     ### Tri par chiffre d'affaires décroissant
    #     table_data = table_data.sort_values(by='Chiffre d\'affaires', ascending=False)
        
    #     ### Affichage du tableau avec tous les états
    #     st.dataframe(table_data)
    # else:
    #     st.warning("Aucune donnée disponible pour le tableau")


if __name__=='__main__':
    main()