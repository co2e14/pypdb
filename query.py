from typing import List, Dict, Generator
import solrq
import requests


def form_solr_query(resolution_low: int = 0, resolution_high: int = 4) -> solrq.Q:
    """
    Form the solr query to the PDBe, specifying the desired resolution range, structure type and experimental method.

    @param resolution_low: Lower bound of the desired resolution.
    @param resolution_high: Upper bound of the desired resolution.
    @return: Solr query object.
    """
    return solrq.Q(
        status="REL",
        experimental_method="X-ray diffraction",
        experiment_data_available="y",
        resolution=solrq.Range(resolution_low, resolution_high),
        molecule_type="Protein",
        seq_30_cluster_number=solrq.Range(solrq.ANY, solrq.ANY),
    )


def make_request(url: str, data: dict) -> List[Dict[str, str | float]]:
    """
    Make a POST request to the PDBe API with the solr query.

    @param url: URL to make request to (PDBe API).
    @param data: The request dictionary.
    @return: A dictionary containing the PDBe response
    @raise RuntimeError: If the request fails in any way.
    """
    response = requests.post(url, data=data, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"Request failed with status code {response.status_code}")

    try:
        json = response.json()
    except ValueError:
        raise RuntimeError("JSON response is not valid JSON")

    response_key = "response"
    if response_key not in json:
        raise RuntimeError("Response key is not in JSON")

    docs_key = "docs"
    if docs_key not in json[response_key]:
        raise RuntimeError("Document key is not in JSON->Response")

    return json["response"]["docs"]

if __name__ == "__main__":
    run = form_solr_query()
    