import requests
import base64
import json
import sys

def test_image_api(image_path, api_url="http://localhost:8001"):
    """Test image upload to API"""
    
    print(f"Testing image: {image_path}")
    
    # Read and encode image
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode()
        print(f"✅ Image loaded: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Failed to load image: {e}")
        return
    
    # Prepare request
    payload = {
        "fileName": image_path,
        "fileType": "image",
        "fileBase64": image_base64
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "sk_track2_987654321"
    }
    
    # Send request
    print(f"📤 Sending request to {api_url}/api/document-analyze")
    try:
        response = requests.post(
            f"{api_url}/api/document-analyze",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"\nSummary: {result.get('summary', 'N/A')[:200]}")
            print(f"\nEntities: {json.dumps(result.get('entities', {}), indent=2)}")
            print(f"\nSentiment: {result.get('sentiment', 'N/A')}")
        else:
            print(f"❌ Failed: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {api_url}. Is the API running?")
        print("   Start API with: uvicorn src.api:app --reload --host 0.0.0.0 --port 8001")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Test with sample3.jpg
    test_image_api("sample3.jpg")