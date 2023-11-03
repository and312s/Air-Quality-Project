import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# membuat helper function

def create_demograph(df): 
    return df.groupby(["station", "year"])["PM2.5"].mean().reset_index()


def create_station_ranking(df):
    return df.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index() 

def create_pollutant_ranking(df):
    pollutant_ranking_df = df.agg({"PM2.5": "mean", "PM10": "mean", "SO2": "mean", "NO2": "mean", "CO": "mean", "O3": "mean"}).sort_values(ascending=False).reset_index()
    pollutant_ranking_df = pollutant_ranking_df.rename(columns={"index": "Pollutant", 0: "Mean"})
    return pollutant_ranking_df

def create_pollutant_comparisson(df):
    selected_columns = ["No", "year", "month", "day", "hour", "station", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    pollutant_comparisson_df = df[selected_columns]
    return pollutant_comparisson_df

def create_season_regretion(df):
    season_regretion = df.groupby(by="month").agg({
    "season" : "first",
    "PM2.5" : "mean",
    "PM10" : "mean",
    "SO2" : "mean",
    "NO2" : "mean",
    "CO" : "mean",
    "O3" : "mean",
    })
    season_regretion = season_regretion.reset_index()

    return season_regretion

def create_pres_regretion(df):
    selected_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    all_df_pres = df.groupby("pres_q")[selected_columns].mean().reset_index() 
    all_df_pres["pres_q"] = all_df_pres["pres_q"].astype(str)
    all_df_pres["pres_q"] = all_df_pres["pres_q"].str.replace('%', '').astype(int)
    
    return all_df_pres

def create_temp_regretion(df):
    selected_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    all_df_temp = df.groupby("temp_q")[selected_columns].mean().reset_index() 
    all_df_temp["temp_q"] = all_df_temp["temp_q"].astype(str)
    all_df_temp["temp_q"] = all_df_temp["temp_q"].str.replace('%', '').astype(int)

    return all_df_temp

def create_rain_regretion(df):
    selected_columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    all_df_rain = df.groupby("rain_q")[selected_columns].mean().reset_index() 
    
    all_df_rain["rain_q"] = all_df_rain["rain_q"].astype(str)
    all_df_rain["rain_q"] = all_df_rain["rain_q"].str.replace('%', '').astype(int)

    return all_df_rain

def create_pollutant_classification(df):
    selected_columns = ["No", "year", "month", "day", "hour", "station", "PM2.5", "aqi (by PM2.5)"]
    pollutant_classification_df = df[selected_columns]
    return pollutant_classification_df

def create_pollutant_ranking_each_station(df):
    selected_columns = ["No", "station", "PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    pollutant_ranking_each_station_df = df[selected_columns].groupby(by="station").agg({
        "PM2.5" : ["mean"],
        "PM10" : ["mean"],
        "SO2" : ["mean"],
        "NO2" : ["mean"],
        "CO" : ["mean"],
        "O3" : ["mean"],
    })

    return pollutant_ranking_each_station_df

def station(x):
    selected_station = pollutant_ranking_each_station_df.iloc[x]
    values = [float(x) for x in selected_station[0:]]  
    return values

def fmt(x):
    total = sum(station(x))
    percentages = [(size / total) * 100 for size in pollutant_ranking_each_station_df.iloc[x]]

    # Format label dengan persentase bentuk dari keseluruhan pie chart
    label_fmt = ["{} ({:.1f}%)".format(label, percentage) for label, percentage in zip(Pollutants, percentages)]
    return label_fmt

# menyiapkan dataframe
url = "https://drive.google.com/uc?export=download&id=1AQBBAoW0t_B27sKrrVRqSg2PO1mn-BTu"
all_df = pd.read_csv(url)

demograph_df = create_demograph(all_df)
pollutant_classification_df = create_pollutant_classification(all_df)
pollutant_comparisson_df = create_pollutant_comparisson(all_df)
station_ranking_df = create_station_ranking(all_df)
pollutant_ranking_df = create_pollutant_ranking(all_df)
pres_regretion_df = create_pres_regretion(all_df)
temp_regretion_df = create_temp_regretion(all_df)
season_regretion_df = create_season_regretion(all_df)
rain_regretion_df = create_rain_regretion(all_df)
pollutant_ranking_each_station_df = create_pollutant_ranking_each_station(all_df)


# membuat dashboard
st.set_page_config(layout="wide")

st.markdown('<style>' + open('color_background.css').read() + '</style>', unsafe_allow_html=True)

st.header("Air Quality Dashboard :cloud:")
st.write("\n\n")


tab1, tab2, tab3 = st.tabs(["Overview", "Aqi in Station", "Pollutant's Regretion"])

with tab1:
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        avg_PM2_5 = round(all_df["PM2.5"].mean(), 1)
        st.metric("Average PM2.5", value=avg_PM2_5)
    
    with col2:
        avg_PM10 = round(all_df["PM10"].mean(), 1)
        st.metric("Average PM10", value=avg_PM10)
    
    with col3:
        avg_SO2 = round(all_df["SO2"].mean(), 1)
        st.metric("Average SO2", value=avg_SO2)
    
    with col4:
        avg_NO2 = round(all_df["NO2"].mean(), 1)
        st.metric("Average PM2.5", value=avg_NO2)
    
    with col5:
        avg_CO = round(all_df["CO"].mean(), 1)
        st.metric("Average CO", value=avg_CO)
    
    with col6:
        avg_O3 = round(all_df["O3"].mean(), 1)
        st.metric("Average O3", value=avg_O3)
    
    st.write("\n\n\n")



    col1, col2 = st.columns([18, 8.3])

    # Menambahkan konten ke masing-masing kolom
    with col1:
        color = ["#4477CE", "#35155D", "#E84A5F", "#FFAC33", "#94D82D"]
        fig, ax = plt.subplots(figsize=(16.5, 5.4))
        
        sns.barplot(x="station", y="PM2.5", hue="year", palette=color, data=demograph_df)
        plt.xlabel("station", color="white")
        plt.ylabel("PM2.5", color="white")
        plt.legend(loc="upper center", ncol=5, )
        plt.title("Air Quality Demograph", fontsize=20, color="white")
        plt.gcf().set_facecolor("#232D3F")
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        st.pyplot(fig)
        
        dict = "PM2.5"
        category_names = station_ranking_df.station.to_list()
        results = { "" : station_ranking_df[dict].to_list()}    
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.colormaps['YlGnBu_r'](
            np.linspace(0.15, 0.85, data.shape[1]))
        
        fig, ax = plt.subplots(figsize=(16.45, 0.4))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())    
        
        set_color = ["#4477CE", "#35155D", "#E84A5F", "#6BB9CC", "#FFAC33", "#94D82D", "#D37BA6", "#00A896", "#F9F871", "#926C42", "#875F9A", "#FF686B"]
        
        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
            label=colname, color=set_color[i])
            
            ax.bar_label(rects, label_type='center', color=set_color[i])
        ax.legend(ncols=len(category_names), bbox_to_anchor=(0, -1),
                  loc='lower left', fontsize='small')
        plt.title("Station Pollution Order : Highest to Lowest", fontsize=10, color="white")
        plt.gcf().set_facecolor("#232D3F")
        st.pyplot(fig)
    
    with col2:
        
        # Data yang dibutuhkan untuk plot pie
        pollutant_data = pollutant_ranking_df.head(6)
        labels = pollutant_data["Pollutant"]
        sizes = pollutant_data["Mean"]
            
        # Membuat plot pie
        fig, ax = plt.subplots(figsize=(10, 20))
        
        
        colors = ["#4477CE", "#35155D", "#E84A5F", "#FFAC33", "#94D82D", "#F9F871"]
        
        wedges, _ = ax.pie(sizes, startangle=140, colors=colors)
        
        # Menghitung persentase dari masing-masing komponen pie
        total = sum(sizes)
        percentages = [(size / total) * 100 for size in sizes]
        
        # Format label dengan persentase bentuk dari keseluruhan pie chart
        label_fmt = ["{} ({:.1f}%)".format(label, percentage) for label, percentage in zip(labels, percentages)]
        
        plt.gcf().set_facecolor("#232D3F")
        # Menambahkan label di luar pie chart
        ax.legend(wedges, label_fmt, title="Pollutants", ncol=6, loc="lower center")
        plt.title("\n Most Pollutant in All Station \n", loc="center", fontsize=20, color="white")
        st.pyplot(fig)
    
    
    
    
    station_list = st.multiselect("Station", ["Aotizhongxin", 
                                                  "Changping", 
                                                  "Dingling", 
                                                  "Dongsi", 
                                                  "Guanyuan", 
                                                  "Gucheng", 
                                                  "Huairou", 
                                                  "Nongzhanguan", 
                                                  "Shunyi", 
                                                  "Tiantan", 
                                                  "Wanliu", 
                                                  "Wanshouxigong"], label_visibility="hidden", default=["Aotizhongxin", "Changping"])
        
       # membuat dropdown
    col1, col2, col3, col4 = st.columns(4)
    with col1:
       pollutant_terpilih = st.selectbox("Pollutant", ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"], key="comparrisson")
    
    with col2:
       hari_terpilih = st.selectbox("Date", list(range(1, 32)), index=3)
   
    with col3:
       bulan_terpilih = st.selectbox("Month", list(range(1, 13)), index=2)
   
    with col4:
       tahun_terpilih = st.selectbox("Year", list(range(2013,2018)), index=2)
    
        # membuat visualisasi data
    fig, ax = plt.subplots(figsize=(24,6))
    
    # plot menggunakan Seaborn
    sns.set_style("whitegrid")
    
    # daftar warna garis
    colors = ["#4477CE", "#35155D", "#E84A5F", "#6BB9CC", "#FFAC33", "#94D82D", "#D37BA6", "#00A896", "#F9F871", "#926C42", "#875F9A", "#FF686B"]
    

    # data terpilih
    selected_data = pollutant_comparisson_df[
        (pollutant_comparisson_df["day"] == hari_terpilih) & 
        (pollutant_comparisson_df["month"] == bulan_terpilih) & 
        (pollutant_comparisson_df["year"] == tahun_terpilih) & 
        (pollutant_comparisson_df["hour"] < 24)]
    selected_data = selected_data[selected_data["station"].isin(station_list)]
    # Menggunakan seaborn lineplot 
    # membuat data perbandingan PM2.5
    sns.lineplot(data=selected_data, x="hour", y=pollutant_terpilih, hue="station", legend=False, palette=colors, linewidth=1.5)
    ax.set_xlabel("hour")
    ax.set_ylabel(pollutant_terpilih)
    ax.set_xticklabels(ax.get_xticklabels(), color="white")
    ax.set_yticklabels(ax.get_yticklabels(), color="white")
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)
    plt.gcf().set_facecolor("#232D3F")
    plt.suptitle(f"\n{pollutant_terpilih} Comparison In Selected Station\n\n", fontsize=20, color="white")
    fig.legend(station_list, loc="lower center", ncol=12)
    st.pyplot(fig)
    


with tab2:
    station_names = ["Aotizhongxin", "Changping", "Dingling", "Dongsi", "Guanyuan", "Gucheng", "Huairou", "Nongzhanguan", "Shunyi", "Tiantan", "Wanliu", "Wanshouxigong"]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
       stasiun_terpilih = st.selectbox("Station", station_names)
    with col2:
       hari_terpilih = st.selectbox("Date", list(range(1, 32)), index=3, key="Date_class")
    
    with col3:
       bulan_terpilih = st.selectbox("Month", list(range(1, 13)), index=2, key="Month_class")
    
    with col4:
       tahun_terpilih = st.selectbox("Year", list(range(2013,2018)), index=2, key="Year_class")
    
    # data terpilih
    selected_data = pollutant_classification_df[(pollutant_classification_df["day"] == hari_terpilih) & (pollutant_classification_df["month"] == bulan_terpilih) & (pollutant_classification_df["year"] == tahun_terpilih) & (pollutant_classification_df["hour"] < 24) & (pollutant_classification_df["station"] == stasiun_terpilih)]
    
    station_dict = {0 : "Aotizhongxin", 
                    1 : "Changping", 
                    2 : "Dingling", 
                    3 : "Dongsi", 
                    4 : "Guanyuan", 
                    5 : "Gucheng", 
                    6 : "Huairou", 
                    7 : "Nongzhanguan", 
                    8 : "Shunyi", 
                    9 : "Tiantan", 
                    10 : "Wanliu", 
                    11 : "Wanshouxigong"}
    
    selected_station = station_names.index(stasiun_terpilih)

        # Daftar warna berdasarkan AQI
    colors = {
        "Good": "#008000",
        "Moderate": "#FFFF00",
        "Unhealty for Sensitive Groups": "#FFA500",
        "Unhealty": "#FF0000",
        "Very Unhealty": "#800080",
        "Hazardous": "#8B4513"
    }

    
    # membuat dropdown
    col5, col6 = st.columns([16, 8.3])
        
    with col5:
        fig, ax = plt.subplots(figsize=(16.5, 5.4))   
        sns.barplot(data=selected_data, y="PM2.5", x="hour", palette=colors, hue="aqi (by PM2.5)", ax=ax)
        ax.set_xlabel("Hour", color="white")
        ax.set_ylabel("PM2.5", color="white")
        ax.set_title(f"Air Quality Index (AQI) in {stasiun_terpilih}", loc="center", fontsize=20, color="white")
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        plt.gcf().set_facecolor("#232D3F")
        
        st.pyplot(fig)

    with col6:
        # Data yang dibutuhkan untuk plot pie
        Pollutants = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
        colors = ["#4477CE", "#35155D", "#E84A5F", "#FFAC33", "#F9F871", "#94D82D"]
        
        
        # Membuat plot pie untuk semua stasiun
        fig, ax = plt.subplots(figsize=(14.5, 7.28))
        
        ax.pie(station(selected_station), startangle=0, colors=colors)
        ax.set_title(f'\nMost Pollutant in {stasiun_terpilih} Station', fontsize= 20, color="white")
        plt.gcf().set_facecolor("#232D3F")
        ax.legend(fmt(selected_station), title='Pollutants', loc='lower center', ncols=6)

        st.pyplot(fig)
            
        
        
        
with tab3:
    selected_pollutant = st.selectbox("Pollutant", ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"], key="Regretion")
    
    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(6,4))
        
        sns.regplot(data=season_regretion_df, y=selected_pollutant, x="month")

        ax.set_xlabel("month", color="white")
        ax.set_ylabel(selected_pollutant, color="white")
        ax.set_xlim(0, 13)
        ax.set_title(f"Season vs {selected_pollutant}", loc="center", fontsize=20, color="white")
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        plt.gcf().set_facecolor("#232D3F")

        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(6,4))

        # Menggunakan seaborn regplot 
        # membuat data perbandingan pressure dan PM2.5
        sns.regplot(data=pres_regretion_df, x=selected_pollutant, y="pres_q")
        ax.set_xlabel(selected_pollutant, color="white")
        ax.set_ylabel("% Pressure", color="white")
        ax.set_ylim(0, 110)
        ax.set_title(f"Pressure vs {selected_pollutant}", loc="center", fontsize=20, color="white")
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        plt.gcf().set_facecolor("#232D3F")
        st.pyplot(fig)
    
    st.write("\n")

    col3, col4 = st.columns(2)

    with col3:
    
                # membuat scatterplot perbandingan antara temperatur dengan pollutant
        fig, ax = plt.subplots(figsize=(6,4))
        
        # Menggunakan seaborn regplot 
        # membuat data perbandingan temperatur dan pollutant
        sns.regplot(data=temp_regretion_df, x=selected_pollutant, y="temp_q")
        ax.set_xlabel(selected_pollutant, color="white")
        ax.set_ylabel("% Temperature", color="white")
        ax.set_ylim(0, 110)
        ax.set_title(f"Temperatur vs {selected_pollutant}", loc="center", fontsize=20, color="white")
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        plt.gcf().set_facecolor("#232D3F")
        st.pyplot(fig)

    with col4:
        fig, ax = plt.subplots(figsize=(6,4))

        # Menggunakan seaborn regplot 
        # membuat data perbandingan Rain dan PM2.5
        sns.regplot(data=rain_regretion_df, x=selected_pollutant, y="rain_q")
        ax.set_xlabel(selected_pollutant, color="white")
        ax.set_ylabel("% Rain", color="white")
        ax.set_title(f"Rain vs {selected_pollutant}", loc="center", fontsize=20, color="white")
        ax.tick_params(axis="x", labelsize=12)
        ax.tick_params(axis="y", labelsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), color="white")
        ax.set_yticklabels(ax.get_yticklabels(), color="white")
        plt.gcf().set_facecolor("#232D3F")
        st.pyplot(fig)
    
    
