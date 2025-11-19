# fly_recombination_logic.py
import requests
import json
import os

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
DB = "gene"

BP_PER_CM = 250_000

CENTROMERE_REGIONS = {
    "2L": 0.3e6,
    "2R": 2.05e6,
    "3L": 0.86e6,
    "3R": 4.53e6,
    "X": 1.53e6
}

def fetch_gene_info(flybase_id):
    """Fetch gene info from NCBI by FlyBase ID."""
    params = {
        "db": DB,
        "term": f"{flybase_id}[Synonym] AND Drosophila melanogaster[Organism]",
        "retmode": "json"
    }
    resp = requests.get(NCBI_BASE_URL, params=params)
    resp.raise_for_status()
    search_data = resp.json()
    
    id_list = search_data.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        raise ValueError(f"No NCBI gene found for FlyBase ID {flybase_id}")
    
    gene_id = id_list[0]

    summary_params = {"db": DB, "id": gene_id, "retmode": "json"}
    summary_resp = requests.get(NCBI_SUMMARY_URL, params=summary_params)
    summary_resp.raise_for_status()
    summary_data = summary_resp.json()

    gene_data = summary_data["result"][gene_id]

    os.makedirs("ncbi_downloads", exist_ok=True)
    filepath = f"ncbi_downloads/{flybase_id}.json"
    with open(filepath, "w") as f:
        json.dump(gene_data, f, indent=4)

    chromosome = gene_data["chromosome"]
    start = int(gene_data["genomicinfo"][0]["chrstart"])
    end = int(gene_data["genomicinfo"][0]["chrstop"])
    midpoint = (start + end) / 2

    return chromosome, midpoint

def check_centromere(chromosome, position):
    arm = chromosome.upper()
    threshold = CENTROMERE_REGIONS.get(arm)
    return threshold and position <= threshold

def compute_genetic_distance(id1, id2):
    """Return a dictionary with distance, recombination rate, warnings."""
    chr1, pos1 = fetch_gene_info(id1)
    chr2, pos2 = fetch_gene_info(id2)

    result = {
        "same_chromosome": chr1 == chr2,
        "chromosomes": (chr1, chr2),
        "distance_bp": None,
        "distance_cM": None,
        "recomb_rate": None,
        "warnings": []
    }

    if chr1 != chr2:
        result["recomb_rate"] = 0.5
        return result

    if check_centromere(chr1, pos1):
        result["warnings"].append(f"{id1} is close to the centromere; recombination is near 0.")
    if check_centromere(chr2, pos2):
        result["warnings"].append(f"{id2} is close to the centromere; recombination is near 0.")

    distance_bp = abs(pos1 - pos2)
    distance_cM = distance_bp / BP_PER_CM
    recomb_rate = min(distance_cM / 100, 0.5)

    result.update({
        "distance_bp": distance_bp,
        "distance_cM": distance_cM,
        "recomb_rate": recomb_rate
    })

    return result
