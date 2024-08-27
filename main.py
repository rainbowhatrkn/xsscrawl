import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urlsplit
import os
import colorama
from colorama import Fore
import questionary
from banner.ban import *
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import json
import subprocess

colorama.init(autoreset=True)

# Fonction pour lire les payloads depuis un fichier
def load_payloads(file_path='payloads.txt'):
    if not os.path.exists(file_path):
        print(Fore.RED + f"Le fichier de payloads '{file_path}' est introuvable.")
        return []
    
    with open(file_path, 'r') as file:
        payloads = [line.strip() for line in file if line.strip()]
    return payloads

# Fonction pour tester un payload
def test_payload(url, payload):
    try:
        response = requests.get(url + payload)
        if response.status_code == 200:
            # Modifier cette condition selon les indices de vulnérabilité que vous attendez
            if 'xss' in response.text.lower():
                return payload
    except Exception as e:
        print(Fore.YELLOW + f"Erreur lors de la requête: {e}")
    return None

# Fonction pour tester les payloads avec un thread pool
def test_payloads(url, payloads, results):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(test_payload, url, payload): payload for payload in payloads}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Testing Payloads"):
            result = future.result()
            if result:
                results.add((url, result))

# Fonction pour crawler les pages avec un thread pool
def crawl(url, visited, payloads, results):
    if url in visited:
        return
    visited.add(url)
    
    print(Fore.CYAN + f"Crawling {url}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return
        
        # Test des payloads
        test_payloads(url, payloads, results)
    except Exception as e:
        print(Fore.YELLOW + f"Erreur lors du crawling: {e}")
    
    # Crawler les liens internes
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]
    
    # Enlever les fragments des URLs (partie après le #)
    links = [urlsplit(link_url)._replace(fragment='').geturl() for link_url in links]
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(crawl, link_url, visited, payloads, results): link_url for link_url in links if urlparse(link_url).netloc == urlparse(url).netloc}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Crawling Links"):
            future.result()

# Fonction pour sauvegarder les résultats dans un fichier texte
def save_results(results, file_name='vulnerable_results.txt'):
    with open(file_name, 'w') as f:
        for url, payload in results:
            f.write(f"URL: {url} - Payload: {payload}\n")
    print(Fore.GREEN + f"Les résultats ont été sauvegardés dans '{file_name}'.")

# Fonction pour sauvegarder les résultats dans un fichier CSV
def save_results_csv(results, file_name='vulnerable_results.csv'):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Payload'])
        writer.writerows(results)
    print(Fore.GREEN + f"Les résultats ont été sauvegardés dans '{file_name}'.")

# Fonction pour sauvegarder les résultats dans un fichier JSON
def save_results_json(results, file_name='vulnerable_results.json'):
    results_list = [{'url': url, 'payload': payload} for url, payload in results]
    with open(file_name, 'w') as f:
        json.dump(results_list, f, indent=4)
    print(Fore.GREEN + f"Les résultats ont été sauvegardés dans '{file_name}'.")

# Fonction pour afficher un résultat vulnérable avec un style
def display_vulnerable_result(results):
    if results:
        url, payload = next(iter(results))  # Afficher un seul résultat pour la démonstration
        message = f"Résultat vulnérable trouvé!\nURL: {url}\nPayload: {payload}"
        try:
            # Afficher le message avec cowsay
            cowsay_process = subprocess.Popen(
                ['cowsay', '-f', 'fox', message],
                stdout=subprocess.PIPE
            )
            # Passer la sortie de cowsay à lolcat
            subprocess.run(
                ['lolcat', '-a'],
                stdin=cowsay_process.stdout,
                check=True
            )
            # Assurer la fermeture du flux stdout de cowsay
            cowsay_process.stdout.close()
        except FileNotFoundError:
            print(Fore.RED + "Erreur: Les outils nécessaires ne sont pas installés.")
    else:
        print(Fore.YELLOW + "Aucun résultat vulnérable trouvé.")

# Point d'entrée principal
def main():
    # Afficher un banner
    fun_prompt()

    target_url = questionary.text("Entrez l'URL cible:", default="http://www.alsetex.fr/index.php").ask()
    payload_file = questionary.text("Entrez le chemin du fichier de payloads (défaut: payloads.txt):", default="payloads.txt").ask()
    
    payloads = load_payloads(payload_file)
    if not payloads:
        print(Fore.RED + "Aucun payloads chargés. Le programme se termine.")
        return
    
    # Créer un ensemble pour stocker les résultats uniques
    results = set()
    
    # Test initial du domaine
    if test_payload(target_url, payloads[0]):  # Assurez-vous de tester avec un payload qui est typiquement vulnérable
        results.add((target_url, payloads[0]))
    
    # Crawler le site si c'est un domaine
    if urlparse(target_url).netloc:
        crawl(target_url, set(), payloads, results)
    
    # Sauvegarder les résultats
    output_file = questionary.select(
        "Choisissez le format de sortie:",
        choices=["Texte (.txt)", "CSV (.csv)", "JSON (.json)"]
    ).ask()

    if output_file == "Texte (.txt)":
        save_results(results)
    elif output_file == "CSV (.csv)":
        save_results_csv(results)
    elif output_file == "JSON (.json)":
        save_results_json(results)
    
    # Afficher un résultat vulnérable de manière stylisée
    display_vulnerable_result(results)

if __name__ == "__main__":
    main()
