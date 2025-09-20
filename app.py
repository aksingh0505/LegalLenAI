from flask import Flask, render_template, request, jsonify
import json
import logging
import re
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load sample legal data + rules with error handling
def load_data():
    """Load legal data from JSON file with error handling."""
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("data.json file not found")
        return {"explanations": {}, "risky_keywords": [], "sample_rental_agreement": ""}
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in data.json: {e}")
        return {"explanations": {}, "risky_keywords": [], "sample_rental_agreement": ""}
    except Exception as e:
        logger.error(f"Error loading data.json: {e}")
        return {"explanations": {}, "risky_keywords": [], "sample_rental_agreement": ""}

data = load_data()

def validate_text_input(text: str, max_length: int = 10000) -> bool:
    """Validate text input for length and content."""
    if not text or not isinstance(text, str):
        return False
    if len(text.strip()) == 0:
        return False
    if len(text) > max_length:
        return False
    return True

def sanitize_input(text: str) -> str:
    """Basic input sanitization to prevent XSS."""
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

@app.route("/")
def home():
    return render_template("index.html", sample_agreement=data.get("sample_rental_agreement", ""))

@app.route("/summarize", methods=["POST"])
def summarize():
    """Summarize rental agreement document."""
    try:
        text = request.form.get("doc_text", "")
        
        # Validate input
        if not validate_text_input(text):
            return jsonify({"error": "Invalid or empty document provided."}), 400
        
        # Sanitize input
        text = sanitize_input(text)
        
        # Enhanced summarization algorithm
        sentences = text.split('.')
        important_sentences = []
        
        # Look for key legal terms and extract relevant sentences
        key_terms = ['rent', 'deposit', 'termination', 'penalty', 'notice', 'utilities', 'maintenance']
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # Skip very short sentences
                for term in key_terms:
                    if term.lower() in sentence.lower():
                        important_sentences.append(sentence)
                        break
        
        # If no key terms found, take first few sentences
        if not important_sentences:
            important_sentences = [s.strip() for s in sentences[:3] if len(s.strip()) > 10]
        
        # Create summary
        if important_sentences:
            summary = "Key points from the document:\n\n" + ".\n".join(important_sentences[:5])
            if len(important_sentences) > 5:
                summary += "\n\n[Additional clauses present in full document]"
        else:
            summary = "Document summary: " + " ".join(text.split()[:30]) + "..."
        
        word_count = len(text.split())
        summary_word_count = len(summary.split())
        
        return jsonify({
            "summary": summary,
            "original_word_count": word_count,
            "summary_word_count": summary_word_count
        })
        
    except Exception as e:
        logger.error(f"Error in summarize: {e}")
        return jsonify({"error": "An error occurred while processing the document."}), 500

@app.route("/explain", methods=["POST"])
def explain():
    """Explain a specific clause or legal term."""
    try:
        clause = request.form.get("clause", "")
        
        # Validate input
        if not validate_text_input(clause, max_length=100):
            return jsonify({"error": "Invalid clause provided."}), 400
        
        # Sanitize input
        clause = sanitize_input(clause).lower()
        
        if not clause:
            return jsonify({"error": "No clause provided."}), 400
        
        # Enhanced clause matching with fuzzy search
        explanations = data.get("explanations", {})
        found_explanations = []
        
        # Exact match first
        for key, explanation_data in explanations.items():
            if key.lower() == clause:
                # Handle both old string format and new object format
                if isinstance(explanation_data, dict):
                    explanation_text = explanation_data.get("definition", "")
                    additional_info = {
                        "importance": explanation_data.get("importance", ""),
                        "category": explanation_data.get("category", ""),
                        "typical_amount": explanation_data.get("typical_amount", ""),
                        "refund_conditions": explanation_data.get("refund_conditions", ""),
                        "typical_penalty": explanation_data.get("typical_penalty", ""),
                        "notice_period": explanation_data.get("notice_period", ""),
                        "penalties": explanation_data.get("penalties", "")
                    }
                else:
                    explanation_text = explanation_data
                    additional_info = {}
                
                return jsonify({
                    "explanation": explanation_text,
                    "source": "local",
                    "match_type": "exact",
                    "clause": key,
                    "additional_info": additional_info
                })
        
        # Partial match
        for key, explanation_data in explanations.items():
            if key.lower() in clause or clause in key.lower():
                if isinstance(explanation_data, dict):
                    meaning = explanation_data.get("definition", "")
                else:
                    meaning = explanation_data
                found_explanations.append({"key": key, "meaning": meaning})
        
        # Word-based matching
        if not found_explanations:
            clause_words = clause.split()
            for key, explanation_data in explanations.items():
                key_words = key.lower().split()
                if any(word in key_words for word in clause_words if len(word) > 2):
                    if isinstance(explanation_data, dict):
                        meaning = explanation_data.get("definition", "")
                    else:
                        meaning = explanation_data
                    found_explanations.append({"key": key, "meaning": meaning})
        
        if found_explanations:
            # Return the best match
            best_match = found_explanations[0]
            return jsonify({
                "explanation": best_match["meaning"],
                "source": "local",
                "match_type": "partial",
                "clause": best_match["key"],
                "suggestions": [f["key"] for f in found_explanations[1:3]]  # Additional suggestions
            })
        
        return jsonify({
            "explanation": "No explanation found in local database. Try searching for terms like 'security deposit', 'rent escalation', or 'termination clause'.",
            "source": "none",
            "suggestions": list(explanations.keys())[:5]  # Show available terms
        })
        
    except Exception as e:
        logger.error(f"Error in explain: {e}")
        return jsonify({"error": "An error occurred while processing the clause."}), 500

@app.route("/risks", methods=["POST"])
def risks():
    """Analyze document for potential risks and issues."""
    try:
        text = request.form.get("doc_text", "")
        
        # Validate input
        if not validate_text_input(text):
            return jsonify({"error": "Invalid or empty document provided."}), 400
        
        # Sanitize input
        text = sanitize_input(text).lower()
        
        # Enhanced risk analysis with categorization using data.json structure
        risk_categories_data = data.get("risk_categories", {})
        risk_categories = {}
        for category, info in risk_categories_data.items():
            risk_categories[category] = info.get("keywords", [])
        
        risks_found = []
        risk_summary = {"financial": 0, "legal": 0, "operational": 0, "property": 0, "restrictions": 0}
        
        for category, keywords in risk_categories.items():
            category_risks = []
            for keyword in keywords:
                if keyword in text:
                    # Get explanation data
                    explanation_data = data.get("explanations", {}).get(keyword, {})
                    if isinstance(explanation_data, dict):
                        description = explanation_data.get("definition", "Risk identified")
                        importance = explanation_data.get("importance", "MEDIUM")
                        severity = "HIGH" if importance == "HIGH" else "MEDIUM" if importance == "MEDIUM" else "LOW"
                    else:
                        description = explanation_data if explanation_data else "Risk identified"
                        severity = "HIGH" if keyword in ["eviction", "indemnity", "rent escalation"] else "MEDIUM"
                    
                    category_risks.append({
                        "keyword": keyword,
                        "severity": severity,
                        "description": description,
                        "importance": importance if isinstance(explanation_data, dict) else "MEDIUM"
                    })
                    risk_summary[category] += 1
            
            if category_risks:
                category_info = risk_categories_data.get(category, {})
                risks_found.append({
                    "category": category.title(),
                    "count": len(category_risks),
                    "description": category_info.get("description", ""),
                    "severity": category_info.get("severity", "MEDIUM"),
                    "risks": category_risks
                })
        
        # Calculate overall risk score
        total_risks = sum(risk_summary.values())
        risk_score = "LOW" if total_risks < 3 else "MEDIUM" if total_risks < 7 else "HIGH"
        
        # Check for missing important clauses using data.json
        important_clauses = data.get("important_clauses", ["rent due date", "security deposit", "notice period", "termination clause"])
        missing_clauses = [clause for clause in important_clauses if clause not in text]
        
        response_data = {
            "risk_score": risk_score,
            "total_risks": total_risks,
            "risk_categories": risks_found,
            "risk_summary": risk_summary,
            "missing_clauses": missing_clauses,
            "source": "local"
        }
        
        if not risks_found:
            response_data["message"] = "No major risks found in local database."
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error in risks: {e}")
        return jsonify({"error": "An error occurred while analyzing risks."}), 500

@app.route("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "data_loaded": bool(data.get("explanations")),
        "explanations_count": len(data.get("explanations", {})),
        "risky_keywords_count": len(data.get("risky_keywords", []))
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info("Starting LegalLenAI application...")
    logger.info(f"Data loaded: {len(data.get('explanations', {}))} explanations, {len(data.get('risky_keywords', []))} risk keywords")
    app.run(host="0.0.0.0", port=5000, debug=True)
