import pandas as pd
import requests
import base64

class MedicalDataProcessor:
    @staticmethod
    def load_data():
        """Load PubMedQA dataset and prepare documents and questions dataframes."""

        tmp_data = pd.read_json("medical_data.json").T

        # some labels have been defined as "maybe", only keep the yes/no answers
        tmp_data = tmp_data[tmp_data.final_decision.isin(["yes", "no"])]
        documents = pd.DataFrame(
            {"abstract": tmp_data.apply(lambda row: " ".join(row.CONTEXTS + [row.LONG_ANSWER]), axis=1),
             "year": tmp_data.YEAR})
        questions = pd.DataFrame({"question": tmp_data.QUESTION,
                                  "year": tmp_data.YEAR,
                                  "gold_label": tmp_data.final_decision,
                                  "gold_context": tmp_data.LONG_ANSWER,
                                  "gold_document_id": documents.index})

        return documents, questions

class GithubDataProcessor:
    @staticmethod
    def load_data(owner: str, repo: str, path: str = "") -> pd.DataFrame:
        """Load .md files from a GitHub repo directory."""
        headers = {"Accept": "application/vnd.github.v3+json"}
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}".rstrip("/")
        resp = requests.get(api_url, headers=headers)
        resp.raise_for_status()
        items = resp.json()

        md_rows = []
        for item in items:
            if item.get("type") != "file":
                continue
            name = item.get("name", "")
            if not name.lower().endswith(".md"):
                continue

            download_url = item.get("download_url")
            content = ""
            if download_url:
                r = requests.get(download_url, headers=headers)
                r.raise_for_status()
                content = r.text
            else:
                # fallback: use the API-provided base64 content if available
                api_item = requests.get(item["url"], headers=headers)
                api_item.raise_for_status()
                body = api_item.json()
                if body.get("content"):
                    content = base64.b64decode(body["content"]).decode(body.get("encoding", "utf-8"))

            md_rows.append({
                "filename": name,
                "content": content
            })

        return pd.DataFrame(md_rows)
