import requests
import pandas as pd




def read_transcripts(transcript_file):

    microRNA_target = pd.read_csv(transcript_file, sep='\t', header=None)
    microRNA_target.columns = ["transcript", "binding", "sequence", "source", "mirna", "probability"]
    transcript_list = microRNA_target["transcript"]
    genes = get_gene_names(transcript_list)


def get_gene_name_from_transcript(transcript_id):
    """
    Retrieve the gene name corresponding to a given transcript ID.

    Args:
        transcript_id (str): A transcript ID in Ensembl or RefSeq format.

    Returns:
        str: The gene name corresponding to the given transcript ID, or 'Unknown' if no gene information was found.
    """
    # Check if the transcript ID is in Ensembl format
    if transcript_id.startswith('ENST'):
        ensembl_transcript_id = transcript_id
    else:
        # Convert the transcript ID to Ensembl format using the Ensembl REST API
        id_url = 'https://rest.ensembl.org/lookup/id'
        id_params = {'id': transcript_id, 'content-type': 'application/json', 'expand': '1'}
        id_response = requests.get(id_url, params=id_params)

        if id_response.ok:
            ensembl_transcript_id = id_response.json().get('transcript')
        else:
            # Return 'Unknown' if the transcript ID cannot be converted to Ensembl format
            return 'Unknown'

    # Retrieve the gene information using the Ensembl REST API
    gene_url = f'https://rest.ensembl.org/lookup/id/{ensembl_transcript_id}?content-type=application/json;expand=1'
    gene_response = requests.get(gene_url)

    if gene_response.ok:
        gene_name = gene_response.json().get('display_name')
    else:
        gene_name = 'Unknown'

    return gene_name


def get_gene_names(transcript_ids):
    """
    Retrieve the gene names corresponding to a list of transcript IDs using the Ensembl REST API batch endpoint.

    Args:
        transcript_ids (list): A list of transcript IDs in Ensembl or RefSeq format.

    Returns:
        dict: A dictionary mapping each input transcript ID to its corresponding gene name, or 'Unknown' if no gene information was found.
    """
    # Convert the transcript IDs to Ensembl format using the Ensembl REST API batch endpoint
    batch_url = 'https://rest.ensembl.org/batch'
    batch_params = {'content-type': 'application/json'}
    batch_data = {'ids': transcript_ids, 'expand': 1}
    batch_response = requests.post(batch_url, headers=batch_params, json=batch_data)

    # Map each transcript ID to its corresponding gene name
    gene_names = {}
    if batch_response.ok:
        batch_results = batch_response.json()
        for result in batch_results:
            transcript_id = result.get('id')
            if 'error' in result:
                gene_names[transcript_id] = 'Unknown'
            else:
                gene_name = result.get('transcript').get('display_name')
                gene_names[transcript_id] = gene_name
    else:
        # Return 'Unknown' for all transcript IDs if the batch retrieval fails
        gene_names = {transcript_id: 'Unknown' for transcript_id in transcript_ids}

    return gene_names

def convert_refseq_2_ensembl(transcripts):
    base_url = 'https://rest.ensembl.org'
    # Set the endpoint for retrieving xrefs by gene symbol
    endpoint = '/xrefs/symbol'
    # Create a list of request objects for each transcript
    requests_list = [{'method': 'GET', 'endpoint': f'{endpoint}/RefSeq_mRNA/{t}?content-type=application/json'} for t in
                     transcripts]

    # Send a POST request to the Ensembl REST API batch endpoint with the list of requests
    batch_response = requests.post(f'{base_url}/batch', headers={'Content-Type': 'application/json'},
                                   json=requests_list)
    # Extract the Ensembl IDs from the batch response
    ensembl_ids = {t: r['response'][0]['id'] for t, r in zip(transcripts, batch_response.json())}
    return ensembl_ids

def get_gene_names_i(transcript_ids):
    batch_size = 100
    batched_ids = [transcript_ids[i:i+batch_size] for i in range(0, len(transcript_ids), batch_size)]
    gene_names = []
    for batch in batched_ids:
        batch_url = "https://rest.ensembl.org/batch/lookup/id"
        batch_params = {"Content-Type": "application/json", "Accept": "application/json"}
        batch_data = {"ids": batch, "expand": ["transcript"]}
        batch_response = requests.post(batch_url, headers=batch_params, json=batch_data)
        batch_response.raise_for_status()
        batch_json = batch_response.json()
        for result in batch_json:
            if "Transcript" in result:
                transcript = result["Transcript"]
                if "gene" in transcript:
                    gene_name = transcript["gene"]["stable_id"]
                    gene_names.append(gene_name)
                else:
                    gene_names.append(None)
            else:
                gene_names.append(None)
    return gene_names

def get_gene_names_i(transcript_ids):
    batch_size = 100
    batched_ids = [transcript_ids[i:i+batch_size] for i in range(0, len(transcript_ids), batch_size)]
    gene_names = []
    for batch in batched_ids:
        batch_url = "https://rest.ensembl.org/batch/lookup/id"
        batch_params = {"Content-Type": "application/json", "Accept": "application/json"}
        batch_data = {"ids": batch, "expand": ["transcript"]}
        batch_response = requests.post(batch_url, headers=batch_params, json=batch_data)
        batch_response.raise_for_status()
        batch_json = batch_response.json()
        for result in batch_json:
            if "Transcript" in result:
                transcript = result["Transcript"]
                if "gene" in transcript:
                    gene_name = transcript["gene"]["stable_id"]
                    gene_names.append(gene_name)
                else:
                    gene_names.append(None)
            else:
                gene_names.append(None)
    return gene_names