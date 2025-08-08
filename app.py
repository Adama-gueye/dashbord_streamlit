import streamlit as st
import pandas as pd ##Exploiration des données
import matplotlib.pyplot as plt  ## Graphiques
import numpy as np 
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


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


    # state_mapping = {
    #     'AL': 'Alabama',
    #     'AK': 'Alaska',
    #     'AZ': 'Arizona',
    #     'AR': 'Arkansas',
    #     'CA': 'California',
    #     'CO': 'Colorado',
    #     'CT': 'Connecticut',
    #     'DE': 'Delaware',
    #     'FL': 'Florida',
    #     'GA': 'Georgia',
    #     'HI': 'Hawaii',
    #     'ID': 'Idaho',
    #     'IL': 'Illinois',
    #     'IN': 'Indiana',
    #     'IA': 'Iowa',
    #     'KS': 'Kansas',
    #     'KY': 'Kentucky',
    #     'LA': 'Louisiana',
    #     'ME': 'Maine',
    #     'MD': 'Maryland',
    #     'MA': 'Massachusetts',
    #     'MI': 'Michigan',
    #     'MN': 'Minnesota',
    #     'MS': 'Mississippi',
    #     'MO': 'Missouri',
    #     'MT': 'Montana',
    #     'NE': 'Nebraska',
    #     'NV': 'Nevada',
    #     'NH': 'New Hampshire',
    #     'NJ': 'New Jersey',
    #     'NM': 'New Mexico',
    #     'NY': 'New York',
    #     'NC': 'North Carolina',
    #     'ND': 'North Dakota',
    #     'OH': 'Ohio',
    #     'OK': 'Oklahoma',
    #     'OR': 'Oregon',
    #     'PA': 'Pennsylvania',
    #     'RI': 'Rhode Island',
    #     'SC': 'South Carolina',
    #     'SD': 'South Dakota',
    #     'TN': 'Tennessee',
    #     'TX': 'Texas',
    #     'UT': 'Utah',
    #     'VT': 'Vermont',
    #     'VA': 'Virginia',
    #     'WA': 'Washington',
    #     'WV': 'West Virginia',
    #     'WI': 'Wisconsin',
    #     'WY': 'Wyoming'
    # }
    state_mapping = {
        'AL': {'name': 'Alabama', 'lat': 32.806671, 'lon': -86.791130},
        'AK': {'name': 'Alaska', 'lat': 61.370716, 'lon': -152.404419},
        'AZ': {'name': 'Arizona', 'lat': 33.729759, 'lon': -111.431221},
        'AR': {'name': 'Arkansas', 'lat': 34.969704, 'lon': -92.373123},
        'CA': {'name': 'California', 'lat': 36.116203, 'lon': -119.681564},
        'CO': {'name': 'Colorado', 'lat': 39.059811, 'lon': -105.311104},
        'CT': {'name': 'Connecticut', 'lat': 41.597782, 'lon': -72.755371},
        'DE': {'name': 'Delaware', 'lat': 39.318523, 'lon': -75.507141},
        'FL': {'name': 'Florida', 'lat': 27.766279, 'lon': -81.686783},
        'GA': {'name': 'Georgia', 'lat': 33.040619, 'lon': -83.643074},
        'HI': {'name': 'Hawaii', 'lat': 21.094318, 'lon': -157.498337},
        'ID': {'name': 'Idaho', 'lat': 44.240459, 'lon': -114.478828},
        'IL': {'name': 'Illinois', 'lat': 40.349457, 'lon': -88.986137},
        'IN': {'name': 'Indiana', 'lat': 39.849426, 'lon': -86.258278},
        'IA': {'name': 'Iowa', 'lat': 42.011539, 'lon': -93.210526},
        'KS': {'name': 'Kansas', 'lat': 38.526600, 'lon': -96.726486},
        'KY': {'name': 'Kentucky', 'lat': 37.668140, 'lon': -84.670067},
        'LA': {'name': 'Louisiana', 'lat': 31.169546, 'lon': -91.867805},
        'ME': {'name': 'Maine', 'lat': 44.693947, 'lon': -69.381927},
        'MD': {'name': 'Maryland', 'lat': 39.063946, 'lon': -76.802101},
        'MA': {'name': 'Massachusetts', 'lat': 42.230171, 'lon': -71.530106},
        'MI': {'name': 'Michigan', 'lat': 43.326618, 'lon': -84.536095},
        'MN': {'name': 'Minnesota', 'lat': 45.694454, 'lon': -93.900192},
        'MS': {'name': 'Mississippi', 'lat': 32.741646, 'lon': -89.678696},
        'MO': {'name': 'Missouri', 'lat': 38.456085, 'lon': -92.288368},
        'MT': {'name': 'Montana', 'lat': 46.921925, 'lon': -110.454353},
        'NE': {'name': 'Nebraska', 'lat': 41.125370, 'lon': -98.268082},
        'NV': {'name': 'Nevada', 'lat': 38.313515, 'lon': -117.055374},
        'NH': {'name': 'New Hampshire', 'lat': 43.452492, 'lon': -71.563896},
        'NJ': {'name': 'New Jersey', 'lat': 40.298904, 'lon': -74.521011},
        'NM': {'name': 'New Mexico', 'lat': 34.840515, 'lon': -106.248482},
        'NY': {'name': 'New York', 'lat': 42.165726, 'lon': -74.948051},
        'NC': {'name': 'North Carolina', 'lat': 35.630066, 'lon': -79.806419},
        'ND': {'name': 'North Dakota', 'lat': 47.528912, 'lon': -99.784012},
        'OH': {'name': 'Ohio', 'lat': 40.388783, 'lon': -82.764915},
        'OK': {'name': 'Oklahoma', 'lat': 35.565342, 'lon': -96.928917},
        'OR': {'name': 'Oregon', 'lat': 44.572021, 'lon': -122.070938},
        'PA': {'name': 'Pennsylvania', 'lat': 40.590752, 'lon': -77.209755},
        'RI': {'name': 'Rhode Island', 'lat': 41.680893, 'lon': -71.511780},
        'SC': {'name': 'South Carolina', 'lat': 33.856892, 'lon': -80.945007},
        'SD': {'name': 'South Dakota', 'lat': 44.299782, 'lon': -99.438828},
        'TN': {'name': 'Tennessee', 'lat': 35.747845, 'lon': -86.692345},
        'TX': {'name': 'Texas', 'lat': 31.054487, 'lon': -97.563461},
        'UT': {'name': 'Utah', 'lat': 40.150032, 'lon': -111.862434},
        'VT': {'name': 'Vermont', 'lat': 44.045876, 'lon': -72.710686},
        'VA': {'name': 'Virginia', 'lat': 37.769337, 'lon': -78.169968},
        'WA': {'name': 'Washington', 'lat': 47.400902, 'lon': -121.490494},
        'WV': {'name': 'West Virginia', 'lat': 38.491226, 'lon': -80.954453},
        'WI': {'name': 'Wisconsin', 'lat': 44.268543, 'lon': -89.616508},
        'WY': {'name': 'Wyoming', 'lat': 42.755966, 'lon': -107.302490}
    }
    sales['StateComplete'] = sales['State'].map(lambda x: state_mapping.get(x, {}).get('name', x))


    st.dataframe(sales.head())

    statut = st.sidebar.multiselect("Statut", sales["status"].unique())

    if statut:
        filtered_sales = sales[sales["status"].isin(statut)]
    else:
        filtered_sales = sales

    val1, val2, val3 = st.columns(3)
    st.markdown("## 📊 Indicateurs Clés")

    ca = (filtered_sales["price"] * filtered_sales["qty_ordered"]).sum()
    val1.metric("Chiffre d'affaire", f"{ca:,.0f} $")

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

    st.subheader("Carte des Ventes par État")
    
    # Calcul du chiffre d'affaires (prix * quantité) pour chaque ligne
    filtered_sales['total_sale'] = filtered_sales['price'] * filtered_sales['qty_ordered']
    
    # Préparation des données
    state_sales_data = filtered_sales.groupby('State')['total_sale'].sum().reset_index()
    
    # Créer un DataFrame avec tous les états
    all_states = pd.DataFrame({
        'State': list(state_mapping.keys()),
        'State Name': [state_mapping[state]['name'] for state in state_mapping],
        'lat': [state_mapping[state]['lat'] for state in state_mapping],
        'lon': [state_mapping[state]['lon'] for state in state_mapping]
    })
    
    # Fusionner avec les données de vente
    state_sales = pd.merge(all_states, state_sales_data, on='State', how='left')
    state_sales['total_sale'] = state_sales['total_sale'].fillna(0)
    
    # Créer la carte choroplèthe
    fig_map = px.choropleth(
        state_sales,
        locations='State',
        locationmode='USA-states',
        color='total_sale',
        scope='usa',
        hover_name='State Name',
        hover_data={'total_sale': ':$,.2f', 'State': True},
        color_continuous_scale=px.colors.sequential.Plasma,
        title='Ventes par État',
        labels={'total_sale': 'Chiffre d\'affaires'}
    )
    
    # Ajouter les annotations d'état
    for i, row in state_sales.iterrows():
        fig_map.add_trace(
            go.Scattergeo(
                lon=[row['lon']],
                lat=[row['lat']],
                text=[row['State']],
                mode='text',
                textfont=dict(size=10, color='black', family='Arial, bold'),
                showlegend=False,
                hoverinfo='none'
            )
        )
    
    # Personnaliser la mise en page
    fig_map.update_layout(
        height=600,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        geo=dict(
            lakecolor='rgb(255, 255, 255)',
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)",
            showlakes=True,
            showsubunits=True,
            showcountries=True,
            bgcolor='rgba(0,0,0,0)'
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    ### Affichage du tableau des états
    st.subheader("Tableau des États Américains avec Ventes")
    
    # Préparation des données pour le tableau
    table_data = state_sales[['State', 'State Name', 'total_sale']].copy()
    table_data.rename(columns={
        'State': 'Abréviation',
        'State Name': 'État',
        'total_sale': 'Chiffre d\'affaires'
    }, inplace=True)
    
    # Formatage du chiffre d'affaires
    table_data['Chiffre d\'affaires'] = table_data['Chiffre d\'affaires'].apply(lambda x: f"${x:,.2f}")
    
    # Tri par chiffre d'affaires décroissant
    table_data = table_data.sort_values(by='Chiffre d\'affaires', ascending=False, key=lambda x: x.str.replace('$', '').str.replace(',', '').astype(float))
    
    st.dataframe(table_data)

if __name__=='__main__':
    main()