import requests
import yaml
from deepdiff import DeepDiff
from pprint import pprint

# --- Configuration ---
CLOUDBEES_URL = "https://CONTROLLER_URL/ha-rolling-upgrade-test-1"
CLOUDBEES_USER = "USERNAME"
CLOUDBEES_TOKEN = "API_TOKEN"
GITHUB_BUNDLE_URL = "https://raw.githubusercontent.com/timhosey/cbci-casc-bundles/refs/heads/main/child-1/jenkins.yaml"

def get_cloudbees_casc():
    api_url = f"{CLOUDBEES_URL}/core-casc-export/jenkins.yaml"  # This endpoint may vary!
    resp = requests.get(api_url, auth=(CLOUDBEES_USER, CLOUDBEES_TOKEN))
    resp.raise_for_status()
    # You may need to parse the response depending on your instance config!
    # If it returns YAML directly:
    return yaml.safe_load(resp.text)

def get_github_casc():
    resp = requests.get(GITHUB_BUNDLE_URL)
    resp.raise_for_status()
    return yaml.safe_load(resp.text)

def main():
    print("Fetching CasC from CloudBees CI...")
    cb_casc = get_cloudbees_casc()
    print("Fetching CasC from GitHub...")
    gh_casc = get_github_casc()

    print("Diffing configurations...")
    diff = DeepDiff(cb_casc, gh_casc, ignore_order=True)
    # Store the raw diff for later use
    raw_diff = diff
    if diff:
        print("Differences found (pretty-printed):")
        pprint(diff, width=120)
    else:
        print("No differences found.")

if __name__ == "__main__":
    main()