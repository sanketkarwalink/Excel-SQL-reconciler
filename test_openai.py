#!/usr/bin/env python3
"""
OpenAI API Test for Excel-to-SQL Reconciler
"""

import sys
import os
sys.path.append('src')

def test_openai_connection():
    print("🔑 Testing OpenAI API Connection...")
    print("-" * 40)
    
    # Get API key
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Set environment variable
    os.environ['OPENAI_API_KEY'] = api_key
    
    try:
        from openai import OpenAI
        print("✅ OpenAI library imported successfully")
        
        # Test connection
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client created")
        
        # Test simple API call
        print("🤖 Testing API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Reply with just 'API test successful'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        if "successful" in result.lower():
            print("🎉 OpenAI API is working correctly!")
            return True
        else:
            print("⚠️  API responded but with unexpected content")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        
        # Common error messages and solutions
        error_str = str(e).lower()
        if "authentication" in error_str or "api key" in error_str:
            print("\n💡 Solution: Check your API key")
            print("   - Make sure it starts with 'sk-'")
            print("   - Verify it's copied correctly (no extra spaces)")
            print("   - Check if the key is still valid at https://platform.openai.com")
        elif "quota" in error_str or "billing" in error_str:
            print("\n💡 Solution: Check your OpenAI billing")
            print("   - Add payment method at https://platform.openai.com/account/billing")
            print("   - Check usage limits")
        elif "rate limit" in error_str:
            print("\n💡 Solution: Rate limit exceeded")
            print("   - Wait a moment and try again")
            print("   - Check your rate limits")
        else:
            print(f"\n💡 General OpenAI error. Full error: {e}")
            
        return False

def test_reconciler_with_api():
    print("\n🔍 Testing Reconciler with OpenAI...")
    print("-" * 40)
    
    try:
        from utils.reconciliation import send_to_openai
        import pandas as pd
        
        # Load sample data
        df_excel = pd.read_csv('src/data/gl_excel.csv').head(5)  # Small sample
        df_sql = pd.read_csv('src/data/gl_sql.csv').head(5)
        
        print(f"✅ Sample data loaded: {len(df_excel)} Excel rows, {len(df_sql)} SQL rows")
        
        # Test AI analysis
        print("🤖 Testing AI-powered reconciliation...")
        result = send_to_openai(df_excel, df_sql)
        
        if result and not any("error" in str(item).lower() for item in result):
            print("✅ AI reconciliation successful!")
            print(f"📊 Result: {len(result)} items returned")
            return True
        else:
            print("❌ AI reconciliation failed")
            print(f"Result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Reconciler test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🔑 OPENAI API TROUBLESHOOTING TOOL")
    print("=" * 50)
    
    # Test 1: Basic API connection
    api_works = test_openai_connection()
    
    if api_works:
        # Test 2: Reconciler integration
        reconciler_works = test_reconciler_with_api()
        
        if reconciler_works:
            print("\n🎉 SUCCESS: Everything is working!")
            print("✅ Your API key is valid")
            print("✅ OpenAI integration is functional") 
            print("✅ Ready to use in Streamlit app")
        else:
            print("\n⚠️  API works but reconciler has issues")
    else:
        print("\n❌ Fix the API key issue first, then try again")
    
    print("\n" + "=" * 50)
