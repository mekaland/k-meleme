import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans,AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.cluster.hierarchy import linkage,dendrogram


sonuc=pd.read_csv("C:/Users/hp/OneDrive/Masaüstü/bist30_sonuclar.csv")
ms = MinMaxScaler()
X=ms.fit_transform(sonuc.iloc[:,[1,2]])
X=pd.DataFrame(X,columns=["Gelir","Oynaklık"])

model = AgglomerativeClustering(n_clusters=4,linkage="single")
tahmin =model.fit_predict(X)
labels= model.labels_

sonuc["Labels"]=labels
sns.scatterplot(x="Labels",y="Hisse",data=sonuc,hue="Labels",palette="deep")
plt.show()  
#kmodel = KMeans(random_state=0)
#kfit=kmodel.fit(X)
#labels=kfit.labels_

sns.scatterplot(x="Gelir",y="Oynaklık",data=X,hue=labels,palette="deep")
plt.show()