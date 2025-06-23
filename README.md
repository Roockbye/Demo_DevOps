
# Mise en place d’une pipeline de CI/CD

### 1. Si vous n’en possédez pas déjà un, créez vous un compte Github et lié votre compte via clé SSH à votre ordinateur

https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account

https://docs.github.com/fr/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```
```
$ eval "$(ssh-agent -s)"
> Agent pid 59566
```
```
ssh-add ~/.ssh/id_ed25519
```
```
cat ~/.ssh/id_ed25519.pub
# Then select and copy the contents of the id_ed25519.pub file
# displayed in the terminal to your clipboard
```

- Dans le coin supérieur droit de n’importe quelle page sur GitHub, cliquez sur votre photo de profil, puis sur Paramètres

- Dans la section « Accès » de la barre latérale, cliquez sur Clés SSH et GPG.

- Cliquez sur Nouvelle clé SSH ou Ajouter une clé SSH.

- Dans le champ « Titre », ajoutez une étiquette descriptive pour la nouvelle clé. Par exemple, si vous utilisez un ordinateur portable personnel, vous pouvez nommer cette clé « Ordinateur portable personnel »

- Sélectionnez le type de clé : authentification ou signature. Pour plus d’informations sur la signature de commit, consultez À propos de la vérification des signatures de commit.

- Dans le champ « Clé », collez votre clé publique.

- Cliquez sur Ajouter une clé SSH.

- Si vous y êtes invité, confirmez l’accès à votre compte dans GitHub

```
rocky@pacman:~/Documents/DevOps/TP_CI$ ssh -T git@github.com
Hi Roockbye! You've successfully authenticated, but GitHub does not provide shell access.
```

[ssh](./images/ssh.png)

### 2. Tester un premier workflow Github avec l’exemple suivant : https://docs.github.com/fr/actions/quickstart

voir fichier github-actions-demo.yml:

```
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

```
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

On push et on vérifie dans "Actions" si le workflow est bien remonté.

### 3. Créer deux classes python, une classe SimpleMath contenant une fonction statique “addition” prenant deux arguments. Et une classe TestSimpleMath qui hérite de unittest.TestCase et contient une fonction de test unitaire.


Voir fichier simple_maths.py et test_simple_maths.py

On test que tout fonctionne bien : 
```
rocky@pacman:~/Demo_DevOps$ python3 -m unittest test_simple_maths.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### 4. Pousser votre code sur un nouveau repository Github et avec Github Actions créer un workflow permettant de lancer les tests unitaires de votre application.

github-actions-demo.yml :

```
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

```
class SimpleMath:
    @staticmethod
    def addition(a, b):
        return a + b

    @staticmethod
    def soustraction(a, b):
        return a - b
```

test_simple_maths.py : (on ajoute)

```
def test_soustraction(self):
    self.assertEqual(SimpleMath.soustraction(5, 3), 2)
```
On peut tester localement:
```
python3 -m unittest test_simple_math.py
```
Puis on push et on vérifie que l'action est bien passé

### 6. Ajouter une étape de lint (validation statique et syntaxique de votre code source) dans votre workflow. Utiliser pylint.

```
pip install pylint
```

```
echo "pylint" > requirements.txt
```
Ça permettra d'installer les dépendances nécessaires au projet si quelqu'un d'autres souhaite le reprendre.

Tester pylint localement :

```
pylint simple_maths.py test_simple_maths.py
```

```
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

```
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
        pylint simple_math.py test_simple_math.py || true

    - name: Lancer les tests unitaires
      run: python3 -m unittest discover
```
Le || true à la fin de la commande pylint permet de ne pas casser le pipeline même si pylint met une mauvaise note.

### 7. Ajouter une étape qui build un conteneur Docker embarquant votre application. La directive CMD de votre Dockerfile doit exécuter les tests unitaires dès le run d’un nouveau conteneur à partir de cette image.

