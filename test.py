import requests
import json

def test_api():
    url = "https://web-production-a5e714.up.railway.app/aianalyst/"
    
    files = {
        'questions': ('question.txt', open('question.txt', 'rb'), 'text/plain'),
        'csv': ('test_data.csv', open('test_data.csv', 'rb'), 'text/csv')
    }
    
    response = requests.post(url, files=files)
    
    if response.status_code == 200:
        try:
            # First decode (API may wrap JSON inside a string)
            raw = response.json()
            if isinstance(raw, str):
                raw_str = raw.strip()
                # Remove markdown fences if present
                if raw_str.startswith("```"):
                    raw_str = raw_str.strip("`")
                    raw_str = raw_str.replace("json\n", "", 1).strip()
                result = json.loads(raw_str)
            else:
                result = raw
        except Exception as e:
            print("❌ Failed to parse JSON:", e)
            print("Raw text:", response.text[:300])
            return

        print("Parsed response:", json.dumps(result, indent=2))

        # Validate structure
        assert isinstance(result, dict), "Response should be a JSON object"
        assert "answers" in result, "Response should contain 'answers' key"

        answers = result["answers"]

        # Assertions
        assert answers.get("row_count_age_gt_30") == 150, \
            "row_count_age_gt_30 should equal 150"
        
        assert "titanic" in str(answers.get("most_expensive_movie", "")).lower(), \
            "most_expensive_movie should mention Titanic"
        
        assert abs(float(answers.get("correlation_coefficient", 0)) - 0.485782) <= 0.001, \
            "correlation_coefficient should be ~0.485782"
        
        assert "scatterplot" in str(answers.get("scatterplot_description", "")).lower(), \
            "scatterplot_description should describe a scatterplot"
        
        print("✅ All tests passed")

    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_api()
