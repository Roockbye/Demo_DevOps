
# Mise en place d’une pipeline de CI/CD

### 1. Si vous n’en possédez pas déjà un, créez vous un compte Github et lié votre compte via clé SSH à votre ordinateur

https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```
```bash
$ eval "$(ssh-agent -s)"
> Agent pid 59566
```
```bash
ssh-add ~/.ssh/id_ed25519
```
```bash
cat ~/.ssh/id_ed25519.pub
# Then select and copy the contents of the id_ed25519.pub file
# displayed in the terminal to your clipboard
```

- Dans le coin supérieur droit de n’importe quelle page sur GitHub, cliquez sur votre photo de profil, puis sur Paramètres

- Dans la section « Accès » de la barre latérale, cliquez sur Clés SSH et GPG.

- Cliquez sur Nouvelle clé SSH ou Ajouter une clé SSH.

- Dans le champ « Titre », ajoutez une étiquette descriptive pour la nouvelle clé. Par exemple, si vous utilisez un ordinateur portable personnel, vous pouvez nommer cette clé « Ordinateur portable personnel »

- Sélectionnez le type de clé : authentification ou signature.

- Dans le champ « Clé », collez votre clé publique.

- Cliquez sur Ajouter une clé SSH.

- Si vous y êtes invité, confirmez l’accès à votre compte dans GitHub

```
rocky@pacman:~/Documents/DevOps/TP_CI$ ssh -T git@github.com
Hi Roockbye! You've successfully authenticated, but GitHub does not provide shell access.
```
Cette dernière fonctionne correctement

[SSH](./images/ssh.png)

### 2. Tester un premier workflow Github avec l’exemple suivant : https://docs.github.com/fr/actions/quickstart

créer le dossier : **.github/workflows** puis le fichier **github-actions-demo.yml**

voir fichier github-actions-demo.yml: (rajoutez ces lignes)

```yml
name: GitHub Actions Demo
run-name: ${{ github.actor }} is testing out GitHub Actions 🚀
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - run: echo "🎉 The job was automatically triggered by a ${{ github.event_name }} event."
      - run: echo "🐧 This job is now running on a ${{ runner.os }} server hosted by GitHub!"
      - run: echo "🔎 The name of your branch is ${{ github.ref }} and your repository is ${{ github.repository }}."
      - name: Check out repository code
        uses: actions/checkout@v4
      - run: echo "💡 The ${{ github.repository }} repository has been cloned to the runner."
      - run: echo "🖥️ The workflow is now ready to test your code on the runner."
      - name: List files in the repository
        run: |
          ls ${{ github.workspace }}
      - run: echo "🍏 This job's status is ${{ job.status }}."
```
Puis on push :

```bash
rocky@pacman:~/Demo_DevOps$ mkdir -p .github/workflows
rocky@pacman:~/Demo_DevOps$ nano .github/workflows/github-actions-demo.yml
rocky@pacman:~/Demo_DevOps$ git add .
rocky@pacman:~/Demo_DevOps$ git commit -m "test github actions"
[main (commit racine) 2cff819] test github actions
 1 file changed, 18 insertions(+)
 create mode 100644 .github/workflows/github-actions-demo.yml
rocky@pacman:~/Demo_DevOps$ git branch -M main
rocky@pacman:~/Demo_DevOps$ git push -u origin main
Énumération des objets: 5, fait.
Décompte des objets: 100% (5/5), fait.
Compression par delta en utilisant jusqu'à 20 fils d'exécution
Compression des objets: 100% (3/3), fait.
Écriture des objets: 100% (5/5), 756 octets | 756.00 Kio/s, fait.
Total 5 (delta 0), réutilisés 0 (delta 0), réutilisés du pack 0
To https://github.com/Roockbye/Demo_DevOps.git
 * [new branch]      main -> main
la branche 'main' est paramétrée pour suivre 'origin/main'.
```

[test github actions](./images/github_actions.png)

On push et on vérifie dans le repository --> "Actions" si le workflow est bien remonté.

### 3. Créer deux classes python, une classe SimpleMath contenant une fonction statique “addition” prenant deux arguments. Et une classe TestSimpleMath qui hérite de unittest.TestCase et contient une fonction de test unitaire.


fichier simple_maths.py :

```python
class SimpleMath:
    @staticmethod
    def addition(a, b):
        return a + b
```


test_simple_maths.py

```python
import unittest
from simple_maths import SimpleMath

class TestSimpleMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(SimpleMath.addition(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
```

On test que tout fonctionne bien : 
```bash
rocky@pacman:~/Demo_DevOps$ python3 -m unittest test_simple_maths.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```
Tout est ok !

### 4. Pousser votre code sur un nouveau repository Github et avec Github Actions créer un workflow permettant de lancer les tests unitaires de votre application.

github-actions-demo.yml :

```yaml
name: CI Python

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Installer Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Lancer les tests
      run: python3 -m unittest discover
```

On push. Toutes les étapes du workflow sont vertes, tout est passé !

[new workflow](./images/new_workflow.png)

### 5. Créer la fonction soustraction et le test associé. Puis, pousser votre commit. Les tests sont effectués automatiquement via la pipeline.

simple_maths.py :

```python
class SimpleMath:
    @staticmethod
    def addition(a, b):
        return a + b

    @staticmethod
    def soustraction(a, b):
        return a - b
```

test_simple_maths.py : (on ajoute)

```python
def test_soustraction(self):
    self.assertEqual(SimpleMath.soustraction(5, 3), 2)
```
On peut tester localement:
```bash
python3 -m unittest test_simple_maths.py
```
Puis on push et on vérifie que l'action est bien passé. Tout est vert.

### 6. Ajouter une étape de lint (validation statique et syntaxique de votre code source) dans votre workflow. Utiliser pylint.

```bash
pip install pylint
```

```bash
echo "pylint" > requirements.txt
```
Ça permettra d'installer les dépendances nécessaires au projet si quelqu'un d'autres souhaite le reprendre.

Tester pylint localement :

```bash
pylint simple_maths.py test_simple_maths.py
```

```bash
(.venv) rocky@pacman:~/Demo_DevOps$ pylint simple_maths.py test_simple_maths.py
************* Module simple_maths
simple_maths.py:1:0: C0114: Missing module docstring (missing-module-docstring)
simple_maths.py:1:0: C0115: Missing class docstring (missing-class-docstring)
simple_maths.py:3:4: C0116: Missing function or method docstring (missing-function-docstring)
simple_maths.py:7:4: C0116: Missing function or method docstring (missing-function-docstring)
************* Module test_simple_maths
test_simple_maths.py:1:0: C0114: Missing module docstring (missing-module-docstring)
test_simple_maths.py:4:0: C0115: Missing class docstring (missing-class-docstring)
test_simple_maths.py:5:4: C0116: Missing function or method docstring (missing-function-docstring)
test_simple_maths.py:7:4: C0116: Missing function or method docstring (missing-function-docstring)

-----------------------------------
Your code has been rated at 4.29/10
```
Le test fonctionne bien, nous finissons avec une mauvaise note, ce qui est normal dans ce contexte.

On va modifier le workflow :

```yaml
name: CI Python

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Installer Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Installer les dépendances
      run: pip install -r requirements.txt

    - name: Lancer Pylint (analyse statique)
      run: |
        pylint simple_maths.py test_simple_maths.py || true

    - name: Lancer les tests unitaires
      run: python3 -m unittest discover
```
Le || true à la fin de la commande pylint permet de ne pas casser le pipeline même si pylint met une mauvaise note.

[ajout lint](./images/ajout_lint.png)

### 7. Ajouter une étape qui build un conteneur Docker embarquant votre application. La directive CMD de votre Dockerfile doit exécuter les tests unitaires dès le run d’un nouveau conteneur à partir de cette image.

Je teste localement mon Docker file avant de le push
```bash
docker build -t demo-devops .
```
```bash
(.venv) rocky@pacman:~/Demo_DevOps$ docker build -t demo-devops .
[+] Building 6.5s (9/9) FINISHED                                                                                                                                                 docker:default
 => [internal] load build definition from Dockerfile                                                                                                                                       0.0s
 => => transferring dockerfile: 180B                                                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.11-slim                                                                                                                        1.3s
 => [internal] load .dockerignore                                                                                                                                                          0.0s
 => => transferring context: 2B                                                                                                                                                            0.0s
 => [1/4] FROM docker.io/library/python:3.11-slim@sha256:9e1912aab0a30bbd9488eb79063f68f42a68ab0946cbe98fecf197fe5b085506                                                                  1.9s
 => => resolve docker.io/library/python:3.11-slim@sha256:9e1912aab0a30bbd9488eb79063f68f42a68ab0946cbe98fecf197fe5b085506                                                                  0.0s
 => => sha256:9e1912aab0a30bbd9488eb79063f68f42a68ab0946cbe98fecf197fe5b085506 9.13kB / 9.13kB                                                                                             0.0s
 => => sha256:cfa2a40862158178855ab4f7cf6b9341646f826b0467a7b72bdeac68b03986bb 1.75kB / 1.75kB                                                                                             0.0s
 => => sha256:be3324b8ee1a17161c5fa4a20f310d4af42cbb4f22a1e7a32a98ee9196a6defd 5.37kB / 5.37kB                                                                                             0.0s
 => => sha256:dad67da3f26bce15939543965e09c4059533b025f707aad72ed3d3f3a09c66f8 28.23MB / 28.23MB                                                                                           1.1s
 => => sha256:799440a7bae7c08a5fe9d9e5a1ccd72fc3cbf9d85fa4be450e12b8550175c620 3.51MB / 3.51MB                                                                                             0.8s
 => => sha256:9596beeb5a6dc0950529870568799000e8d73fb678969ac2f485005cd5da1087 16.21MB / 16.21MB                                                                                           1.4s
 => => sha256:15658014cd85cd0d8b913d50b4388228aebcf0437d43cfb37e8a5177e8b2bcf8 248B / 248B                                                                                                 1.0s
 => => extracting sha256:dad67da3f26bce15939543965e09c4059533b025f707aad72ed3d3f3a09c66f8                                                                                                  0.4s
 => => extracting sha256:799440a7bae7c08a5fe9d9e5a1ccd72fc3cbf9d85fa4be450e12b8550175c620                                                                                                  0.1s
 => => extracting sha256:9596beeb5a6dc0950529870568799000e8d73fb678969ac2f485005cd5da1087                                                                                                  0.2s
 => => extracting sha256:15658014cd85cd0d8b913d50b4388228aebcf0437d43cfb37e8a5177e8b2bcf8                                                                                                  0.0s
 => [internal] load build context                                                                                                                                                          0.3s
 => => transferring context: 42.79MB                                                                                                                                                       0.3s
 => [2/4] WORKDIR /app                                                                                                                                                                     0.2s
 => [3/4] COPY . .                                                                                                                                                                         0.3s
 => [4/4] RUN pip install --no-cache-dir -r requirements.txt                                                                                                                               2.5s
 => exporting to image                                                                                                                                                                     0.4s
 => => exporting layers                                                                                                                                                                    0.4s
 => => writing image sha256:e1daa7249ef4cf1e1d605b336f8df390f5a69464b1b576d21f45ce5ebed57423                                                                                               0.0s
 => => naming to docker.io/library/demo-devops 
```

```bash
(.venv) rocky@pacman:~/Demo_DevOps$ docker run --rm demo-devops
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```
Tout fonctionne ! Je peux maintenant ajouter mon dockerfile dans mon workflow

on rajoute sur **.github/workflows/github-actions-demo.yml** :

```yaml
    - name: Build Docker image
      run: docker build -t demo-devops .
```

[ajout docker file](./images/ajout_dockerfile.png)

Tout fonctionne !