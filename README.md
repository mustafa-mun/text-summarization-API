# Translate and Summarize API

The Translate and Summarize API allows you to summarize content, whether it's in the form of raw text, URL, or file, and offers the additional option to translate the content before summarization. With flexible options for extractive and abstractive summarization methods, as well as seamless translation capabilities.

## Key Features

- `Summarize content`: Generate summaries of text-based content.
- `Choose summarization methods`: Benefit from extractive or abstractive summarization methods based on your specific requirements.
- `Seamlessly translate content`: Optionally translate the content before the summarization process, allowing for analysis in different languages.
- `Support for various content types`: Summarize text, URLs, or files, enabling versatility in data sources and use cases.

## Summarizing Content Extractive

To summarize content extractive, make a POST request to the /summarizeExtractive endpoint, providing the content in the request body. You can specify the content as raw text, a URL, or a file.

Example request body:

```json
{
  "content": "Enter your content here"
}
```
Optionally, you can include additional parameters in the request body:
a

- `sentences` (optional): Specify the number of sentences of the summarized text.
- `to_language` (optional): Specify the language to translate the content before summarization (e.g., "fr" for French).

### Response

The API will respond with a JSON object containing the summarized content and text language:

```json
{
  "summary": "This is the summarized content."
  "language": "Text language"
}
```

## Examples
Here are some examples demonstrating how to use the Translate and Summarize API in different scenarios.

### Example 1: Summarize raw text and translate to german
```bash
POST /summarizeExtractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "Enter your content here"
  "to_language": "de"
}
```

### Example 2: Summarize url
```bash
POST /summarizeExtractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "https://www.example.com"
}
```

### Example 3: Summarize file and specify the summarization length 
```bash
POST /summarizeExtractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "file.txt"
  "sentences": 4
}
```

## Summarizing Content Abstractive

To summarize content abstractive, make a POST request to the /summarizeAbstractive endpoint, providing the content in the request body. You can specify the content as raw text, a URL, or a file.

Example request body:

```json
{
  "content": "Enter your content here"
}
```
Optionally, you can include additional parameters in the request body:
a
- `min_length` (optional): Specify the minimum length of the summary (e.g., 10).
- `max_length` (optional): Specify the maximum length of the summary (e.g., 100).
- `to_language` (optional): Specify the language to translate the content before summarization (e.g., "fr" for French).

### Response

The API will respond with a JSON object containing the summarized content and text language:

```json
{
  "summary": "This is the summarized content."
  "language": "Text language"
}
```

## Examples
Here are some examples demonstrating how to use the Translate and Summarize API in different scenarios.

### Example 1: Summarize raw text and translate to german
```bash
POST /summarizeAbstractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "Enter your content here"
  "to_language": "de"
}
```

### Example 2: Summarize url
```bash
POST /summarizeAbstractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "https://www.example.com"
}
```

### Example 3: Summarize file and specify the summarization length 
```bash
POST /summarizeAbstractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "file.txt"
  "min_length": 150
  "max_length": 200
}
```

## Get Supported Languages for Translation

To get supported languages for translation, make a `GET` request to the /getSupportedLanguages endpoint


## Translate Content

To translate content, make a POST request to the /translate endpoint, providing the content in the request body. You can specify the content as raw text, a URL, or a file.

Example request body:

```json
{
  "content": "Enter your content here"
  "target": "fr"
}
```

### Response

The API will respond with a JSON object containing the summarized content and text language:

```json
{
  "translation": "This is the translated content."
  "from_language": "Text language"
  "to_language": "Target language"
}
```

## Examples
Here are some examples demonstrating how to use the Translate and Summarize API in different scenarios.

### Example 1: Translate raw text and translate to german
```bash
POST /translate
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "Enter your content here"
  "target": "de"
}
```

### Example 2: Translate url
```bash
POST /summarizeExtractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "https://www.example.com"
  "target": "tk"
}
```

### Example 3: Translate file 
```bash
POST /summarizeExtractive
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "content": "file.txt"
  "sentences": 4
}
```


