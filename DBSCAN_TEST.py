import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Load the CSV file
data = pd.read_csv('complete_data_minmax_test.csv', index_col=0)

# Step 2: Drop non-numeric columns that you don't want to cluster on
# (e.g., 'SpatialDimValueCode' for country and 'Period' for time, if you don't want to include time)
X = data.drop(columns=['SpatialDimValueCode', 'Period'])

# Step 3: Run DBSCAN
dbscan = DBSCAN(eps=0.13, min_samples=8)  # Adjust eps and min_samples according to your data
dbscan.fit(X)

# Step 4: Add cluster labels to the original data
data['cluster'] = dbscan.labels_

# Optional: Check the number of clusters and noise points (-1 indicates noise)
print("Number of clusters: ", len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0))
print("Number of noise points: ", list(dbscan.labels_).count(-1))

# Save the results with cluster labels
data.to_csv('dbscan_results.csv', index=False)

# Step 5: Dimensionality reduction for visualization (using PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Step 6: Plot the clusters
plt.figure(figsize=(10, 7))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=dbscan.labels_, cmap='plasma')
plt.title("DBSCAN Clustering Visualization (PCA-reduced dimensions)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label='Cluster')
plt.show()

# Step 7: Plot the k-distance graph to tune `eps`
neigh = NearestNeighbors(n_neighbors=8)
nbrs = neigh.fit(X)
distances, indices = nbrs.kneighbors(X)

# Sort distances and plot them to find the "elbow"
distances = np.sort(distances[:, 7], axis=0)
#plt.plot(distances)
#plt.title("k-Distance Graph to find optimal eps")
#plt.xlabel("Data points sorted by distance")
#plt.ylabel("5th Nearest Neighbor Distance")
#plt.show()

# Group the data by the 'cluster' column and count unique countries in each cluster
country_cluster_count = data.groupby('cluster')['SpatialDimValueCode'].nunique()
country_cluster_count.plot(kind='bar', figsize=(10, 6))
plt.title("Number of Unique Countries in Each Cluster")
plt.xlabel("Cluster")
plt.ylabel("Number of Countries")
plt.show()

# Filter the data for outliers (cluster label = -1)
outliers = data[data['cluster'] == -1]

# Print the outliers
print(outliers)

# Print only the unique countries that are classified as outliers
outlier_countries = outliers['SpatialDimValueCode'].unique()

print("Outlier countries:", outlier_countries)