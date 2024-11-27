import spacy
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

def summarize_text(text: str) -> dict:
    """
    Summarizes the text and extracts important points and keywords.
    
    Parameters:
        text (str): The input text to be summarized.
        
    Returns:
        dict: A dictionary containing 'summary', 'important_points', and 'keywords'.
    """
    try:
        # Check if text is too short
        if not text or len(text.strip()) < 10:
            return {
                'summary': "Text too short to summarize.",
                'important_points': ["Text too short to extract key points."],
                'keywords': ["No keywords available"]
            }

        # Generate summary using the summarization pipeline
        summary_result = summarizer(text, max_length=150, min_length=30, do_sample=False)
        summary = summary_result[0]['summary_text']

        # Extract key points
        important_points = extract_important_points(text)
        if not important_points:
            important_points = ["No key points identified."]

        # Extract keywords
        keywords = extract_keywords(text)
        if not keywords:
            keywords = ["No keywords identified."]

        return {
            'summary': summary,
            'important_points': important_points,
            'keywords': keywords
        }

    except Exception as e:
        print(f"Error in summarize_text: {e}")
        return {
            'summary': "Error generating summary.",
            'important_points': ["Error extracting key points."],
            'keywords': ["Error extracting keywords."]
        }

def extract_important_points(text: str) -> list:
    """
    Extract important points from the text using NLP techniques.
    
    Parameters:
        text (str): The input text.
        
    Returns:
        list: A list of important points.
    """
    try:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Process with SpaCy
        doc = nlp(text)
        
        important_points = []
        
        # Split long sentences into smaller chunks
        for sent in sentences:
            # Skip very short sentences
            if len(sent.split()) < 5:
                continue
                
            # If sentence is too long, break it at conjunctions or punctuation
            if len(sent.split()) > 20:
                sent_doc = nlp(sent)
                chunks = []
                current_chunk = []
                
                for token in sent_doc:
                    current_chunk.append(token.text)
                    # Break at conjunctions or punctuation
                    if (token.pos_ == 'CCONJ' or 
                        token.dep_ == 'cc' or 
                        token.text in ['.', ';', '!']):
                        if len(current_chunk) > 5:  # Only keep meaningful chunks
                            chunks.append(' '.join(current_chunk))
                        current_chunk = []
                
                # Add any remaining chunk
                if len(current_chunk) > 5:
                    chunks.append(' '.join(current_chunk))
                
                # Add chunks as separate points
                for chunk in chunks:
                    if chunk not in important_points:
                        important_points.append(chunk.strip())
            else:
                # Add shorter sentences directly
                if sent not in important_points:
                    important_points.append(sent.strip())
        
        # Filter and clean the points
        cleaned_points = []
        for point in important_points:
            # Clean up the point
            cleaned = point.strip()
            # Remove points that are too similar to existing ones
            if cleaned and not any(
                similar_text(cleaned, existing) for existing in cleaned_points
            ):
                cleaned_points.append(cleaned)
        
        # Sort by length and relevance (shorter, more focused points first)
        sorted_points = sorted(
            cleaned_points,
            key=lambda x: (len(x.split()) > 30, len(x.split()))
        )
        
        # Return top 5 most relevant points
        return sorted_points[:5]

    except Exception as e:
        print(f"Error in extract_important_points: {e}")
        return ["Error extracting key points."]

def extract_keywords(text: str) -> list:
    """
    Extract keywords from the text using NLP techniques.
    
    Parameters:
        text (str): The input text.
        
    Returns:
        list: A list of keywords.
    """
    try:
        # Process with SpaCy
        doc = nlp(text)
        
        # Extract named entities and important noun phrases
        entities = [ent.text.lower() for ent in doc.ents]
        noun_phrases = [chunk.text.lower() for chunk in doc.noun_chunks 
                       if len(chunk.text.split()) <= 3]  # Limit to phrases of 3 words or less
        
        # Extract additional keywords using TF-IDF
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words 
                        if word not in stop_words 
                        and word.isalnum() 
                        and len(word) > 2]
        
        if not filtered_words:
            return entities[:10] if entities else ["No keywords identified."]

        # Create document for TF-IDF
        document = ' '.join(filtered_words)
        
        # Apply TF-IDF
        vectorizer = TfidfVectorizer(max_features=15)
        tfidf_matrix = vectorizer.fit_transform([document])
        
        # Get feature names and their scores
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf_matrix.toarray()[0]
        
        # Combine all potential keywords
        all_keywords = set(entities + noun_phrases + list(feature_names))
        
        # Filter and sort keywords
        keywords = [kw for kw in all_keywords 
                   if len(kw.split()) <= 3  # Limit to 3 words
                   and len(kw) > 2  # Minimum length
                   and not kw.isnumeric()]  # Remove pure numbers
        
        # Sort keywords by length and complexity
        sorted_keywords = sorted(keywords, 
                               key=lambda x: (len(x.split()), len(x)))[:10]
        
        return sorted_keywords if sorted_keywords else ["No keywords identified."]

    except Exception as e:
        print(f"Error in extract_keywords: {e}")
        return ["Error extracting keywords."]

def similar_text(text1: str, text2: str) -> bool:
    """Helper function to check if two pieces of text are very similar"""
    # Convert to sets of words for comparison
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate similarity ratio
    intersection = len(words1.intersection(words2))
    shorter_len = min(len(words1), len(words2))
    
    if shorter_len == 0:
        return False
    
    similarity = intersection / shorter_len
    return similarity > 0.7  # 70% similarity threshold

if __name__ == "__main__":
    # Test the functions
    sample_text = """
    Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction 
    between computers and humans through natural language. The ultimate objective of NLP is to enable 
    computers to understand, interpret, and generate human languages in a way that is valuable. 
    This involves several tasks such as text summarization, translation, sentiment analysis, and more.
    """
    
    result = summarize_text(sample_text)
    print("\nSummary:")
    print(result['summary'])
    print("\nKey Points:")
    for point in result['important_points']:
        print(f"• {point}")
    print("\nKeywords:")
    print(", ".join(result['keywords']))