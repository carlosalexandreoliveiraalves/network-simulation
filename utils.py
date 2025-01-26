#Carregar o GeoJSON
"""
gdf1 = gpd.read_file("mapa_utfpr.geojson")
gdf2 = gpd.read_file("plano_universidade.geojson")

# Verificar o CRS do GeoDataFrame

gdf_combined = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True)) #juntar os poligonos

print("CRS atual:", gdf_combined.crs)

# Garantir que o CRS seja EPSG:4326 para coordenadas geográficas
if gdf_combined.crs is None or gdf_combined.crs.to_string() != "EPSG:4326":
    gdf = gdf_combined.set_crs("EPSG:4326")

# Plotar o GeoDataFrame
ax = gdf_combined.plot(
    figsize=(10, 10),
    alpha=0.7,
    edgecolor="black",
    color="lightblue"
)

# Adicionar título e configurações
ax.set_title("Mapa do Campus UTFPR", fontsize=16)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")+6

# Mostrar o plot
plt.tight_layout()
plt.show()
"""