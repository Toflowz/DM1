import pandas as pd
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, silhouette_samples


data = pd.read_csv('complete_data_minmax_test.csv', index_col=0)

columns_to_average = ['HealthAvailVal_nurse', 'HealthAvailVal_psych', 'FactValueNumeric_alcohol',
                      'suicide_rate', 'HDI', 'Health_Expenditure', 'HomicideRate']
data = data.groupby('SpatialDimValueCode')[columns_to_average].mean().reset_index()

X = data.drop(columns=['SpatialDimValueCode', 'suicide_rate'])


eps = 0.215#0.24
min_samples = 3#4
dbscan = DBSCAN(eps=eps, min_samples=min_samples) 
dbscan.fit(X)


data['cluster'] = dbscan.labels_


print("Number of clusters: ", len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0))
print("Number of noise points: ", list(dbscan.labels_).count(-1))


data.to_csv('dbscan_results_AVG_NOSCD.csv', index=False)

#Dimensionality reduction for visualization (using PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(10, 7))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=dbscan.labels_, cmap='plasma')
plt.title("DBSCAN Clustering Visualization (PCA-reduced dimensions)")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.colorbar(label='Cluster')
plt.show()


neigh = NearestNeighbors(n_neighbors=min_samples)
nbrs = neigh.fit(X)
distances, indices = nbrs.kneighbors(X)

distances = np.sort(distances[:, min_samples-1], axis=0)
plt.plot(distances)
plt.title("k-Distance Graph to find optimal eps")
plt.xlabel("Data points sorted by distance")
plt.ylabel("Nearest Neighbor Distance")
plt.show()


outliers = data[data['cluster'] == -1]
print(outliers[data['SpatialDimValueCode'] == 'BEL'].T)

# Group by cluster and calculate the mean for all relevant features
features_to_average = ['suicide_rate', 'FactValueNumeric_alcohol', 'HDI', 'HomicideRate', 'HealthAvailVal_psych']
cluster_means = data.groupby('cluster')[features_to_average].mean()

# Print the resulting table of means for each cluster
print("Mean values of features for each cluster:")
print(cluster_means)


print("Explained variance by each principal component:", pca.explained_variance_ratio_)

loadings = pd.DataFrame(pca.components_, columns=X.columns)
print("Feature contributions (loadings) to the principal components:")
print(loadings.T)



silhouette_vals = silhouette_samples(X, dbscan.labels_)
outlier_silhouette_vals = silhouette_vals[dbscan.labels_ == -1]
print("Silhouette scores for outliers:")
print(outlier_silhouette_vals)

labels = dbscan.labels_
X_filtered = X[labels != -1]  # Remove noise points
labels_filtered = labels[labels != -1]  # Remove noise labels

# Step 3: Calculate the overall silhouette score (average for all clusters)
sil_score = silhouette_score(X_filtered, labels_filtered)
print(f"Overall Silhouette Score: {sil_score}")