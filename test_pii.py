from services.pii_service import scan_and_redact

test_cases = [
"""Hello, my name is Sezal and I am working on an AI Smart Text Analyzer project.

My email is sezal@example.com and my phone number is +919876543210.

My PAN card is ABCDE1234F and my Aadhaar number is 1234 5678 9012.

My date of birth is 12/05/2005 and my bank account number is 123456789012.

My credit card number is 4111 1111 1111 1111.

For the application, my API key is AbC123xYz987Secret and my access token is AbCdEf1234567890.

My password is MyPassword123.

The project uses Azure AI Language for sentiment analysis and extracts key phrases and named entities. I recently built the AI text analyzer using Python and Streamlit. The model was trained in 2025 using 10000 records.

The PAN card verification feature is implemented, and the application has an API key management feature.

Please analyze the text and provide useful feedback."""
]



for i, text in enumerate(test_cases, 1):

    result = scan_and_redact(text)

    print("=" * 70)
    print(f"TEST {i}")
    print("Original :", text)
    print("Redacted :", result["redacted_text"])
    print("Detected :", result["pii_detected"])
    print("Sources  :", result["detection_sources"])

    for entity in result["entities"]:
        print(
            f"  - {entity['category']} | "
            f"{entity['confidence']:.0%} | "
            f"{entity['source']}"
        )