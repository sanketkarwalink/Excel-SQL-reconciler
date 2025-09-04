# 🔑 OpenAI API Key Setup Guide

## 🚨 **TROUBLESHOOTING YOUR API KEY ISSUE**

### **Quick Fix Steps:**

1. **Refresh the Streamlit app**: http://localhost:8501
2. **In the sidebar, you should now see:**
   - ✅ API Key Set! (when you enter your key)
   - 🔑 Key: sk-proj... (masked version)
   - 🧪 Test API Key button

3. **Enter your API key and click "🧪 Test API Key"**
   - If it shows "🎉 API Key is working!" → You're good to go!
   - If it shows an error → See solutions below

### **Common API Key Problems & Solutions:**

#### ❌ **"Authentication failed"**
**Solutions:**
- Make sure your key starts with `sk-`
- Check for extra spaces before/after the key
- Verify the key at https://platform.openai.com/api-keys

#### ❌ **"You exceeded your current quota"**
**Solutions:**
- Add a payment method: https://platform.openai.com/account/billing
- Check your usage: https://platform.openai.com/usage
- Make sure you have credits/billing set up

#### ❌ **"Rate limit exceeded"**
**Solutions:**
- Wait 1-2 minutes and try again
- You're making requests too quickly

#### ❌ **"API key not found"**
**Solutions:**
- The key might be invalid or expired
- Generate a new key at https://platform.openai.com/api-keys

### **How to Get an OpenAI API Key:**

1. **Go to**: https://platform.openai.com
2. **Sign up/Log in** to your OpenAI account
3. **Navigate to**: API Keys section
4. **Click**: "Create new secret key"
5. **Copy** the key (starts with `sk-`)
6. **Paste** it into the Streamlit sidebar

### **Free Tier Limits:**
- **New accounts**: Usually get $5 free credits
- **Rate limits**: ~3 requests per minute
- **Model access**: GPT-4o-mini should be available

### **Cost for Testing:**
- **GPT-4o-mini**: ~$0.15 per 1M tokens
- **Your test**: Should cost less than $0.01
- **50k row analysis**: Should cost ~$0.05-0.10

### **Alternative: Test Without API Key**
The reconciler still works without AI! It will:
- ✅ Process your 50k row datasets
- ✅ Perform statistical analysis
- ✅ Detect basic discrepancies
- ✅ Generate reconciliation reports
- ❌ Skip AI-powered detailed analysis

### **What the AI Adds:**
- **Detailed reasons** for each discrepancy
- **Categorized mismatch types** 
- **Professional explanations**
- **JSON-formatted results**

---

## 🧪 **Test Your Setup:**

1. **Basic Test**: `python test_openai.py`
2. **Web App**: Visit http://localhost:8501
3. **Use "🧪 Test API Key" button in sidebar**
4. **Try reconciliation with sample data**

If you're still having issues, the improved error messages in the app will tell you exactly what's wrong!
