
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

def extract_content(response):
    """
    Simulates the extraction logic to be implemented in pipeline.py
    """
    content = response
    
    # 1. If it's a list (Gemini format), extract text
    if isinstance(content, list) and len(content) > 0:
        if isinstance(content[0], dict) and 'text' in content[0]:
            content = content[0]['text']
            
    # 2. If it's a string, try to parse as JSON
    if isinstance(content, str):
        content = content.strip()
        # Heuristic: if it looks like a JSON object or list
        if (content.startswith('{') and content.endswith('}')) or \
           (content.startswith('[') and content.endswith(']')):
            try:
                parsed = json.loads(content)
                
                # Case A: List of objects (common in some agent outputs)
                if isinstance(parsed, list) and len(parsed) > 0:
                    if isinstance(parsed[0], dict):
                        # Try common keys
                        for key in ['text', 'content', 'markdown', 'response']:
                            if key in parsed[0]:
                                return parsed[0][key]
                    elif isinstance(parsed[0], str):
                        return parsed[0]
                        
                # Case B: Single object
                elif isinstance(parsed, dict):
                     # Try common keys
                    for key in ['text', 'content', 'markdown', 'response']:
                        if key in parsed:
                            return parsed[key]
                            
            except json.JSONDecodeError:
                pass
                
    return content

def test_extraction():
    print("Testing extraction logic...")
    
    # Case 1: Pure Markdown
    md = "# Title\nContent"
    assert extract_content(md) == md, "Failed Case 1: Pure Markdown"
    print("✓ Case 1: Pure Markdown passed")
    
    # Case 2: JSON List with dict (Current issue)
    json_list = '[{"text": "# Title\\nContent"}]'
    assert extract_content(json_list) == "# Title\nContent", "Failed Case 2: JSON List"
    print("✓ Case 2: JSON List passed")
    
    # Case 3: JSON Object (Potential issue)
    json_obj = '{"text": "# Title\\nContent"}'
    assert extract_content(json_obj) == "# Title\nContent", "Failed Case 3: JSON Object"
    print("✓ Case 3: JSON Object passed")
    
    # Case 4: JSON Object with 'content' key
    json_obj_content = '{"content": "# Title\\nContent"}'
    assert extract_content(json_obj_content) == "# Title\nContent", "Failed Case 4: JSON Object (content key)"
    print("✓ Case 4: JSON Object (content key) passed")

    # Case 5: Gemini artifact format (simulated)
    gemini_artifact = [{"text": "# Title\nContent"}]
    assert extract_content(gemini_artifact) == "# Title\nContent", "Failed Case 5: Gemini Artifact"
    print("✓ Case 5: Gemini Artifact passed")

if __name__ == "__main__":
    test_extraction()
