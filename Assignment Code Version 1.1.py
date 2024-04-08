import os
import tarfile
from tqdm import tqdm
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Function to read citation network dataset
def read_citation_network(file_path):
    citations = {}
    with open(file_path, 'r') as file:
        for line in file:
            source, target = line.strip().split('\t')
            if source not in citations:
                citations[source] = []
            citations[source].append(target)
    return citations

# Function to read abstracts dataset
def read_abstracts_dataset(abstracts_path):
    abstracts = {}
    for folder in os.listdir(abstracts_path):
        folder_path = os.path.join(abstracts_path, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.abs'):
                    paper_id = file.split('.')[0]
                    with open(os.path.join(folder_path, file), 'r', encoding='latin1') as f:
                        content = f.read().strip()
                        abstracts[paper_id] = content
    return abstracts

# Function to calculate cosine similarity between two vectors
def calculate_cosine_similarity(vec1, vec2):
    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]

# Function to embed text using Sci-BERT model
def embed_text(text):
    return model.encode(text)

# Load Sci-BERT model
model = SentenceTransformer('allenai/scibert_scivocab_uncased')

# Paths to datasets
citation_network_file = 'cit-HepTh.txt'
abstracts_path = 'cit-HepTh-abstracts.tar.gz'

# Read citation network dataset
citation_network = read_citation_network(citation_network_file)

# Read abstracts dataset
abstracts = read_abstracts_dataset(abstracts_path)

# Paper IDs for which similarity scores will be calculated
seed_paper_ids = ['9201001', '9203201', '119203001']

# Calculate similarity scores for seed papers
for paper_id in seed_paper_ids:
    if paper_id in citation_network:
        print(f"Seed Paper ID: {paper_id}")
        print("References:")
        for reference_id in citation_network[paper_id]:
            if reference_id in abstracts:
                seed_paper_abstract = abstracts[paper_id]
                reference_abstract = abstracts[reference_id]
                # Embed abstracts
                seed_paper_embedding = embed_text(seed_paper_abstract)
                reference_embedding = embed_text(reference_abstract)
                # Calculate cosine similarity
                similarity_score = calculate_cosine_similarity(seed_paper_embedding, reference_embedding)
                print(f"Reference Paper ID: {reference_id}, Similarity Score: {similarity_score:.4f}")
        print()
    else:
        print(f"No references found for Seed Paper ID: {paper_id}")
