import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def prepare_features(rfm: pd.DataFrame) -> np.ndarray:
    """Log-transform and scale RFM features for clustering."""
    features = rfm[["Recency", "Frequency", "Monetary"]].copy()
    features = np.log1p(features)
    scaler = StandardScaler()
    return scaler.fit_transform(features)


def find_optimal_k(features_scaled: np.ndarray, 
                   k_range: range = range(2, 11)) -> dict:
    """Compute inertia and silhouette scores for each K."""
    results = {}
    for k in k_range:
        kmeans = KMeans(n_clusters=k, init="k-means++",
                        n_init=10, random_state=42)
        labels = kmeans.fit_predict(features_scaled)
        results[k] = {
            "inertia": kmeans.inertia_,
            "silhouette": silhouette_score(features_scaled, labels)
        }
    return results


def fit_kmeans(features_scaled: np.ndarray, 
               n_clusters: int = 4) -> KMeans:
    """Fit final K-Means model."""
    kmeans = KMeans(n_clusters=n_clusters, init="k-means++",
                    n_init=10, max_iter=300, random_state=42)
    kmeans.fit(features_scaled)
    return kmeans


def assign_cluster_labels(rfm: pd.DataFrame,
                          cluster_labels: dict) -> pd.DataFrame:
    """Map cluster numbers to business labels."""
    rfm = rfm.copy()
    rfm["Cluster_Label"] = rfm["Cluster"].map(cluster_labels)
    return rfm
