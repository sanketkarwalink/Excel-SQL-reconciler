# Security

## Overview
This application implements security measures to protect your data and API keys.

## Data Security
- **No Data Storage**: Files are processed in memory only, never saved to disk
- **Session Only**: All data is automatically deleted when you close the browser
- **API Key Protection**: Your OpenAI API key is stored locally in `.env` file only

## File Upload Security
- **File Type Validation**: Only CSV and Excel files are accepted
- **Size Limits**: Maximum file size is 100MB
- **Content Scanning**: Basic validation to prevent malicious files

## API Security
- **Secure Connection**: All API calls use HTTPS encryption
- **Rate Limiting**: Prevents excessive API usage
- **Key Validation**: API key format is validated before use

## Privacy
- **No Personal Data Stored**: Financial data is only processed, never stored
- **Local Processing**: All reconciliation happens on your device
- **Memory Cleanup**: Data is automatically cleared from memory after processing

## Best Practices
1. **Keep API Key Secret**: Never share your OpenAI API key
2. **Use Strong Passwords**: If deploying to cloud, use strong authentication
3. **Regular Updates**: Keep dependencies updated for security patches

## Security Issues
If you find a security issue, please email: sanketkarwa.inbox@gmail.com
