from Bio import Entrez

# Set your email for Entrez API (required by NCBI)
Entrez.email = "ramzichibana31@example.com"

def download_sars_cov2_fasta(variants, years, output_dir,max_seq=100):
    """
    Download SARS-CoV-2 sequences for multiple variants and years from NCBI.
    
    Parameters:
        variants (list): List of variant names (e.g., ["Alpha", "Beta"]).
        years (list): List of years (e.g., ["2020", "2021"]).
        output_dir (str): Directory to save the FASTA files.
    """
    for variant in variants:
        for year in years:
            # Build the search query
            query = f"SARS-CoV-2[Organism] AND {variant}[All Fields] AND {year}[Collection Date]"
            print(f"Searching NCBI for: {query}")
            
            # Search the NCBI nucleotide database
            search_handle = Entrez.esearch(db="nucleotide", term=query, retmax=max_seq)  # Adjust retmax for more results
            search_results = Entrez.read(search_handle)
            search_handle.close()
            
            ids = search_results["IdList"]
            if not ids:
                print(f"No sequences found for {variant} in {year}.")
                continue
            
            print(f"Found {len(ids)} sequences for {variant} in {year}. Fetching FASTA data...")
            
            # Fetch the FASTA sequences
            fetch_handle = Entrez.efetch(db="nucleotide", id=ids, rettype="fasta", retmode="text")
            fasta_data = fetch_handle.read()
            fetch_handle.close()
            
       
            output_file = f"{output_dir}/{variant}_{year}.fasta"
            with open(output_file, "w") as file:
                file.write(fasta_data)
            
            print(f"data saved to {output_file}")

# Example usage:
variants = ["Alpha", "Beta", "Delta"]  
years = ["2020", "2021", "2022"]  
output_dir = "./Data"  # Directory to save the files (current directory)

download_sars_cov2_fasta(variants, years, output_dir)