import os
from google import genai

def main():
    print("--- AI Email Assistant Active ---")
    
    # Grab the API key from the environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # A sample long email thread to test our AI
    sample_email = (
        "Hi Team, I wanted to follow up on the launch timeline. We are currently "
        "waiting on the design assets from marketing. If we don't get them by Tuesday, "
        "the deployment will be delayed to Friday. Let me know if anyone can ping Sarah "
        "to speed things up. Thanks, Dave."
    )
    
    if not api_key:
        print("\n[Status]: Running in OFFLINE mock mode.")
        print("💡 Tip: To unlock real AI power, pass your GEMINI_API_KEY into Docker!")
        print(f"\nAnalyzing Email: {sample_email[:60]}...")
        print("[Mock Summary]: Email mentions a potential launch delay due to missing marketing assets.")
    else:
        print("\n[Status]: GEMINI_API_KEY detected! Connecting to Google Gen AI...")
        
        # Initialize the official client
        client = genai.Client(api_key=api_key)
        
        try:
            print("\nAsking Gemini to summarize the email thread...")
            # Call the standard gemini-2.5-flash model
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Summarize this email in one clear bullet point highlighting the main action item: {sample_email}"
            )
            print("\n--- Gemini AI Response ---")
            print(response.text)
            print("--------------------------")
            
        except Exception as e:
            print(f"\n[Error]: Failed to communicate with Gemini API. Details: {e}")

if __name__ == "__main__":
    main()