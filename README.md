# Technologies et Protocoles pour l’IoT TP

## TP: Lightweight Kubernetes K3s for IoT Edge (Raspberry)

### Noms et prénoms du binôme :
- **Mansour Wajdi** 
- **Bargougui Haykel**
- **Groupe 2**
---

## 1. Installation des deux machines virtuelles Raspberry 64bits :

### a. Une fois les deux machines installées, expliquer le rôle de cette commande :

```bash
getconf LONG_BIT
```

La commande getconf LONG_BIT affiche si le système est en 32 bits ou 64 bits en indiquant la taille des entiers long.


## 2. Installation de K3s avec un seul serveur

Installation de K3s : 

```bash
curl -sfL https://get.k3s.io | sh -
```

### a. Résumé et explication des lignes de configuration de serveur K3s

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVRT...
    server: https://127.0.0.1:6443
  name: default
contexts:
- context:
    cluster: default
    user: default
  name: default
current-context: default
kind: Config
preferences: {}
users:
- name: default
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRV...
    client-key-data: LS0tLS1CRUd...
```

#### Explications :
- **`apiVersion: v1`** : Version de l'API Kubernetes utilisée.
- **`clusters:`** : Infos sur le cluster, incluant l’adresse (`server`) et le certificat pour l’identité (`certificate-authority-data`).
- **`contexts:`** : Associe un utilisateur, un cluster et un namespace. Ici, le contexte `default` utilise le cluster et utilisateur `default`.
- **`users:`** : Identifiants pour accéder au cluster (certificat client et clé privée).
- **`current-context:`** : Contexte actif, ici `default`.


### b. Vérification de l’installation : écrire les commandes de vérification de l’installation correcte du serveur K3s

- **Vérifier le statut du service K3s :**

```bash
sudo systemctl status k3s
```
![image](https://github.com/user-attachments/assets/d18528b0-a808-43da-b90e-d70886b6f157)


### c. Donner le résultat attendu des commandes :
Sortie attendue : une liste contenant des espaces comme default, kube-system, etc.

Résultats attendus des commandes :
Commande :
```bash
sudo kubectl get node
```

La commande est utilisée pour lister tous les nœuds dans le cluster Kubernetes et afficher leurs informations de base. 
Le résultat attendu est une liste des nœuds, accompagnée de détails tels que leur statut, leur rôle et la version de Kubernetes.


Commande :
```bash
sudo kubectl get node -o wide
```

Cette commande liste les nœuds avec des détails supplémentaires. Le résultat attendu inclut les informations de base des nœuds (statut, rôle, version) ainsi que des champs supplémentaires, tels que l'adresse IP interne, le nom de l'hôte et les versions du runtime et du noyau.

### d. Donner la commande ou les commandes qui permettent de redémerrer le serveur K3s :

```bash
sudo systemctl restart k3s
```

## 3. Installation de K3s avec plusieurs nœuds agents

### a. Comment récupérer le token (K3S_TOKEN : variable d’environnement sur le Token) du serveur

```bash
cat /var/lib/rancher/k3s/server/node-token
```

### b. Quelles sont les commandes de configuration d’un nœud agent K3s

```bash
curl -sfL https://get.k3s.io | K3S_TOKEN=<node_token> K3S_URL=https://<IP_DU_MASTER>:6443 sh -
```

### c. Ecrire les commandes de copie du fichier de configuration k3s du serveur (/etc/rancher/k3s/k3s.yaml) dans la machine de l’agent K3s

```bash
scp /etc/rancher/k3s/k3s.yaml iot@<WORKER_IP>:/home/iot/.kube/config
```

### d. On suppose que le serveur a comme adresse IP 192.168.58.135 , proposer la modification nécessaire pour contenir cette adresse dans le fichier de configuration copié dans l’agent :

On doit faire la modification du fichier de configuration pour inclure l'adresse IP du serveur :

```yaml
server: https://192.168.58.135:6443
```

### e. Quel est le rôle de la commande suivante :

```bash
kubectl config view
```

Cette commande affiche la configuration de kubectl sur votre système. Elle permet de visualiser le contenu du fichier de configuration Kubernetes généralement situé dans ~/.kube/config.


### f. Quel est le rôle de la commande suivante :

Rôle de la commande suivante :
```bash
kubectl get pods -A
```

Cette commande liste tous les pods dans tous les namespaces du cluster Kubernetes.


##  4. Installation Helm

### a. Quel est le rôle de Helm

Le rôle de Helm est de gérer les déploiements Kubernetes via des **charts**, qui sont des
modèles préconfigurés pour déployer des applications. Helm facilite :
1. L'installation d'applications complexes.
2. La gestion des versions des déploiements.
3. La personnalisation des configurations avec des fichiers de valeurs (`values.yaml`).


### b. Ecrire les commandes d’installation de Helm
Installation : 
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Vérification :
```bash
helm version
```

### c. Que permet de vérifier cette commande :
```bash
helm list -n kube-system
```

![image](https://github.com/user-attachments/assets/6abd2d74-87da-4d49-967d-b0901056e3e9)

The command `helm list -n kube-system` lists the **Helm releases** deployed in the `kube-system` namespace. Here’s the explanation in French:

- **NAME**: Nom de la release déployée.  
- **NAMESPACE**: Namespace Kubernetes où la release est installée.  
- **REVISION**: Révision ou version de mise à jour de la release.  
- **UPDATED**: Date et heure de la dernière mise à jour de la release.  
- **STATUS**: État de la release (par exemple, "deployed" signifie qu'elle est correctement déployée).  
- **CHART**: Nom de la Helm Chart utilisée pour ce déploiement.  

Dans l’exemple affiché :  
- Deux releases, `traefik` et `traefik-crd`, sont installées dans le namespace `kube-system`, et leur statut est `deployed`.


### d. Expliquer la signification du déploiement de Traefik sur le namespace kube-system

Le déploiement de **Traefik** dans le namespace **kube-system** indique qu'il est configuré comme **ingress controller**, essentiel pour gérer et router le trafic entrant vers les services Kubernetes. Le namespace kube-system reflète son rôle central dans l'infrastructure du cluster.

## 5. Installation de Docker

### a. Donner les lignes de commandes de configuration de Docker

Installation et configuration : 

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

### b. Quel est l’intérêt d’exécuter cette commande :

```bash
sudo docker run hello-world
```

La commande `sudo docker run hello-world` vérifie que Docker est correctement installé et fonctionne. Elle exécute un conteneur simple qui affiche un message de bienvenue, confirmant que Docker peut télécharger des images et exécuter des conteneurs.

## 6. Installation d’application dans le Docker : écrire les configurations et fichier de configuration pour installer une application python dans docker. On suppose que cette application est un traitement au niveau Edge IoT.

- **python app :** 

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated function for processing sensor data
def process_sensor_data(data):
    # Example: calculate the average of sensor values
    sensor_values = data.get("values", [])
    if not sensor_values:
        return {"error": "No sensor values provided"}

    avg_value = sum(sensor_values) / len(sensor_values)
    return {"average": avg_value, "status": "processed"}

@app.route('/process', methods=['POST'])
def process():
    # Get JSON data from the request
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        # Process the data
        result = process_sensor_data(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n--- Edge IoT Simulation App is running ---\n")
    print("Visit http://localhost:5000/process to interact with the app.\n")
    
    # Start the Flask app
    app.run(host="0.0.0.0", port=5000, debug=False)
```

- **Dockerfile :** 
```yaml
# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define the command to run the application
CMD ["python", "edge_iot_simulation.py"]
```

- **requirements.txt :**
```text
Flask==2.0.3
Werkzeug==2.0.3
requests==2.28.2
```


Build et run : 

```bash
sudo docker build -t python-app .
sudo docker run -d -p 5000:5000 python-app
```
![image](https://github.com/user-attachments/assets/35691a5b-c5de-4300-9309-5cce9e4f3e77)



tester l'application 
```bash
curl -X POST -H "Content-Type: application/json" -d '{"values":[10,20,30]}' http://localhost:5000/process
```

![image](https://github.com/user-attachments/assets/af3ee2af-46c5-4a95-9a34-acd12498b168)

## 7. Déploiement du conteneur de l’application de type JS (appelée app-test) dans un pod kubernates.

### a. Ecrire la commande de déploiement

```bash
kubectl apply -f deployment.yaml
```

### b. Quel est le résultat des commandes suivantes :

```bash
Kubectl get deployments
```
- **`kubectl get deployments`** :  
Affiche la liste des déploiements actifs dans le cluster Kubernetes, avec des détails comme le nom, le nombre de réplicas, et l'état actuel.  

```bash
Kubectl get pods
```
- **`kubectl get pods`** :  
Affiche la liste des pods actifs dans le cluster Kubernetes, avec leur statut (Running, Pending, Failed, etc.), leur nom, et d'autres informations.


### c. Ecrire la commande qui permet d’exposer le déploiement du service l’application de l’extérieur :

```bash
kubectl expose deployment app-test --type=NodePort --port=8080 --target-port=8080
```

- --type=NodePort: Permet d'exposer le service à un port disponible sur le nœud.
- --port=8080: Port utilisé par le service.
- --target-port=8080: Port sur lequel le conteneur écoute.

### d. Expliquer la commande suivante :

```bash
Kubectl description service app-test
```

![image](https://github.com/user-attachments/assets/961b076a-1646-40a8-aafa-92a23efb845e)

La commande `kubectl describe service app-test` fournit des détails sur le service Kubernetes nommé **app-test**.  

- **Name, Namespace** : Nom et espace de noms (namespace) du service.  
- **Labels, Selector** : Labels et sélecteurs utilisés pour associer le service aux pods.  
- **Type** : Type de service (ici `NodePort`, permettant l'accès depuis l'extérieur via un port sur les nœuds du cluster).  
- **IP** : Adresse IP interne attribuée au service dans le cluster.  
- **Ports, TargetPort, NodePort** : 
  - Port interne exposé par le service (`8080/TCP`).
  - `NodePort` (31700/TCP) : Port accessible sur les nœuds du cluster.  
- **Endpoints** : IP et port des pods connectés au service (ici `172.17.0.11:8080`).  
- **Events** : Événements récents liés au service (vide ici).  

Cela permet de vérifier la configuration et la connectivité du service.


## 8. Déploiement de contrôleur pour l’application avec fichier manifest Kubernetes définis en YAML. Inspirez vous de la figure suivante pour écrire un fichier YAML pour le déploiement du contrôleur pour avoir deux copies (duplication) de l’application app-test.

### Déploiement du contrôleur
 
- **deployment.yaml :**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-test
  labels:
    app: app-test
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app-test
  template:
    metadata:
      labels:
        app: app-test
    spec:
      nodeSelector:
        node-role.kubernetes.io/worker: "true" 
      containers:
      - name: app-test
        image: wajdimansour/app-test:latest
        ports:
        - containerPort: 8080
        securityContext:
          privileged: true
```

```bash
kubectl apply -f deployment.yaml
```

![image](https://github.com/user-attachments/assets/ac378309-7a3d-4b2e-8683-6dbe6bc411b9)

