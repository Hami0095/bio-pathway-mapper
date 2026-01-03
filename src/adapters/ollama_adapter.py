import requests
import json
import re # Import re for regex
from typing import List, Dict, Any
from .llm_adapter import LLMAdapter
from ..core.config import Config # Import Config for max_json_retries

class OllamaAdapter(LLMAdapter):
    """Ollama-specific implementation"""
    def __init__(self, model_name="gemma3:1b", base_url="http://localhost:11434"):
        super().__init__(model_name, base_url)
        self.session = requests.Session()
        self.max_json_retries = Config.MAX_JSON_RETRIES
        
    def _generate_raw_text(self, prompt: str, json_output: bool = False, **kwargs) -> str:
        """
        Internal method to generate raw text from Ollama API without JSON validation/retries.
        """
        try:
            # Ollama's /api/generate endpoint directly handles json_output via 'format' parameter
            # If format is "json", it attempts to force JSON output
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": True,
                "options": kwargs.get("options", {})
            }
            if json_output:
                payload["format"] = "json"

            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True
            )
            response.raise_for_status()
            
            full_response = []
            for line in response.iter_lines():
                if line:
                    try:
                        json_line = json.loads(line)
                        full_response.append(json_line.get("response", ""))
                    except json.JSONDecodeError:
                        # Log if a non-JSON line is received in a streaming response
                        print(f"Warning: Could not decode JSON line in streaming response: {line.decode('utf-8')}")
            
            return "".join(full_response)

        except requests.exceptions.RequestException as e:
            print("\n--- Ollama API Error ---")
            print("Could not connect to the Ollama server or the API returned an error.")
            print(f"Error details: {e}")
            print("Using mock data for demonstration.")

            # Return a mock JSON response for demonstration purposes
            if "Reconcile pathway data" in prompt:
                mock_response = {
                    "reconciled_pathways": [
                        {"pathway_id": "hsa04115", "pathway_name": "p53 signaling pathway", "genes": ["TP53", "MDM2"], "source_databases": ["KEGG"]},
                        {"pathway_id": "R-HSA-69620", "pathway_name": "Cellular responses to stress", "genes": ["TP53", "ATM"], "source_databases": ["Reactome"]}
                    ],
                    "conflicts": [{
                        "pathway_id": "hsa04115",
                        "conflict_type": "Gene overlap",
                        "description": "Both pathways contain 'TP53' as a gene. This is a significant overlap that warrants further investigation as it may suggest a shared regulatory mechanism or potentially related pathways.",
                        "genes": ["TP53", "MDM2"]
                    }],
                    "confidence_scores": {
                        "hsa04115": 0.95,
                        "R-HSA-69620": 0.92
                    },
                    "recommendations": [
                        "Investigate the specific functional differences between 'TP53' and 'ATM' in the context of cellular stress responses. Compare gene expression patterns of the two pathways.",
                        "Analyze the regulatory interactions between 'TP53' and 'ATM' to determine if they are involved in a coordinated response to stress.",
                        "Check for shared downstream targets of 'TP53' in both pathways. Comparing target genes can help identify potential conflicts.",
                        "Review the publications associated with each pathway to see if there is a common research focus."
                    ]
                }
                return json.dumps(mock_response)
            elif "bottleneck genes" in prompt:
                return "Based on the analysis, the following hypotheses can be generated:\n1. **Hypothesis 1:** The gene TP53 is a master regulator in this network, and its high betweenness centrality suggests it is a key mediator of information flow between different pathways.\n2. **Hypothesis 2:** The gene MDM2 may be a promising drug target to modulate the p53 signaling pathway."
            else:
                # If json_output is True, this fallback also needs to be JSON
                if json_output:
                    return json.dumps({"error": "Mock LLM response: Could not generate JSON for this prompt."})
                else:
                    return "Mock LLM response: Could not generate text for this prompt."

    def clean_response(self, response_text: str) -> str:
        """
        Cleans the LLM response to extract the JSON part.
        Assumes the JSON is enclosed in triple backticks and 'json' keyword.
        """
        # Regex to find JSON block enclosed in ```json ... ```
        match = re.search(r"```json\s*(\{.*\})\s*```", response_text, re.DOTALL)
        if match:
            return match.group(1)
        # If no ```json block, try to find a standalone JSON object
        match = re.search(r"(\{.*\})", response_text, re.DOTALL)
        if match:
            return match.group(1)
        return response_text # Return original if no JSON found

    def add_json_enforcement(self, prompt: str) -> str:
        """
        Augments the prompt to emphasize JSON output.
        """
        enforcement_message = (
            "Your response *must* be a valid JSON object. "
            "Do not include any natural language explanations or additional text outside the JSON. "
            "Ensure the JSON is correctly formatted."
        )
        # Avoid redundant enforcement if already present
        if enforcement_message not in prompt:
            return f"{prompt}\n{enforcement_message}"
        return prompt

    def generate_fallback_json(self) -> Dict[str, Any]:
        """
        Generates a fallback JSON response if all retries fail.
        """
        return {
            "error": "Failed to generate valid JSON response from LLM after multiple retries.",
            "reconciled_pathways": [],
            "conflicts": [],
            "confidence_scores": {},
            "recommendations": ["Review prompt and LLM capabilities."]
        }
        
    def generate_text(self, prompt: str, json_output: bool = False, **kwargs) -> str | Dict[str, Any]:
        """
        Generates text using the Ollama API, with JSON validation and retry logic if json_output is True.
        """
        if not json_output:
            return self._generate_raw_text(prompt, json_output=False, **kwargs)

        # JSON generation with retry logic
        current_prompt = prompt
        for attempt in range(self.max_json_retries):
            response_text = self._generate_raw_text(current_prompt, json_output=True, **kwargs)
            
            cleaned_response = self.clean_response(response_text)
            
            try:
                json_data = json.loads(cleaned_response)
                # If json_data is successfully parsed, we can return it.
                # Further validation (e.g., against a schema) could be added here.
                return json_data
            except json.JSONDecodeError as e:
                print(f"Attempt {attempt + 1} failed to parse JSON: {e}")
                print(f"LLM raw response (attempt {attempt + 1}):\n{response_text}")
                print(f"Cleaned response (attempt {attempt + 1}):\n{cleaned_response}")
                
                if attempt < self.max_json_retries - 1:
                    # Only add enforcement if not already present
                    current_prompt = self.add_json_enforcement(prompt) # Augment original prompt
                    # Consider adding the failed response as context for the retry prompt if the LLM supports it
                    # current_prompt = f"{current_prompt}\nPrevious attempt failed due to invalid JSON. Ensure valid JSON:\n{cleaned_response}"
                else:
                    print("Max JSON retries exceeded.")
                    return self.generate_fallback_json()
        
        # This part should ideally not be reached if max_json_retries is handled in the loop
        return self.generate_fallback_json()
