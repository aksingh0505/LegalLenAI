# LegalLenAI - Rental Agreement Analyzer

A comprehensive web application for analyzing rental agreements using AI-powered text analysis. LegalLenAI helps tenants and landlords understand complex legal terms, identify potential risks, and get intelligent summaries of rental documents.

## 🚀 Features

### Core Functionality
- **Document Summarization**: Intelligent extraction of key points from rental agreements
- **Risk Analysis**: Comprehensive risk assessment with categorized findings
- **Clause Explanation**: Detailed explanations of legal terms with additional context
- **Interactive UI**: Modern, responsive interface with real-time analysis

### Enhanced Features
- **Risk Categorization**: Financial, Legal, Operational, Property, and Restrictions
- **Severity Levels**: HIGH, MEDIUM, LOW risk classification
- **Missing Clauses Detection**: Identifies important clauses that should be present
- **Analysis History**: Track previous analyses with timestamps
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with modern design principles
- **Icons**: Font Awesome
- **Data**: JSON-based legal knowledge base

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd LegalLenAI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
LegalLenAI/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── data.json             # Legal knowledge base
├── README.md             # Project documentation
├── static/
│   └── styles.css        # Main stylesheet
└── templates/
    └── index.html        # Main HTML template
```

## 🔧 API Endpoints

### GET /
- **Description**: Main application page
- **Response**: HTML page with rental agreement analyzer

### POST /summarize
- **Description**: Summarize rental agreement document
- **Parameters**: `doc_text` (form data)
- **Response**: JSON with summary and word counts

### POST /explain
- **Description**: Explain legal terms and clauses
- **Parameters**: `clause` (form data)
- **Response**: JSON with explanation and additional information

### POST /risks
- **Description**: Analyze document for potential risks
- **Parameters**: `doc_text` (form data)
- **Response**: JSON with categorized risk analysis

### GET /health
- **Description**: Health check endpoint
- **Response**: JSON with application status

## 📊 Data Structure

The application uses a comprehensive JSON knowledge base (`data.json`) containing:

### Explanations
- **Definition**: Clear explanation of legal terms
- **Importance**: HIGH/MEDIUM/LOW classification
- **Category**: Financial, Legal, Operational, Property, Restrictions
- **Additional Info**: Typical amounts, penalties, notice periods, etc.

### Risk Categories
- **Financial**: Security deposits, rent escalation, late payments
- **Legal**: Termination clauses, eviction, indemnity
- **Operational**: Lock-in periods, subletting, notice periods
- **Property**: Utilities, damage liability, maintenance
- **Restrictions**: Pet policies, visitor limits, usage restrictions

## 🎨 User Interface

### Main Features
- **Document Input**: Large textarea for pasting rental agreements
- **Action Buttons**: Summarize, Check Risks, Clear
- **Clause Search**: Dedicated input for legal term explanations
- **Results Display**: Formatted output with categorized information
- **History Sidebar**: Track previous analyses
- **Loading States**: Visual feedback during processing

### Design Principles
- **Modern Gradient Background**: Professional legal theme
- **Responsive Layout**: Adapts to different screen sizes
- **Intuitive Navigation**: Clear action buttons and feedback
- **Accessibility**: ARIA labels and semantic HTML
- **Visual Hierarchy**: Clear typography and spacing

## 🔍 Usage Examples

### Document Summarization
1. Paste your rental agreement text
2. Click "Summarize" button
3. View key points and word count statistics

### Risk Analysis
1. Paste your rental agreement text
2. Click "Check Risks" button
3. Review categorized risks with severity levels
4. Check for missing important clauses

### Clause Explanation
1. Enter a legal term (e.g., "security deposit")
2. Click "Explain" button
3. Get detailed explanation with additional context
4. View related terms and suggestions

## 🛡️ Security Features

- **Input Validation**: Comprehensive validation for all inputs
- **XSS Protection**: Basic input sanitization
- **Error Handling**: Graceful error handling with user feedback
- **Rate Limiting**: Built-in protection against abuse
- **Logging**: Comprehensive logging for debugging and monitoring

## 📈 Performance Optimizations

- **Efficient Text Processing**: Optimized algorithms for text analysis
- **Caching**: Data caching for improved performance
- **Responsive Design**: Optimized for various devices
- **Minimal Dependencies**: Lightweight Flask application

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' for debug mode
- `FLASK_DEBUG`: Enable/disable debug mode

### Data Customization
Modify `data.json` to:
- Add new legal terms and explanations
- Update risk categories and keywords
- Modify important clauses list
- Adjust legal requirements

## 🐛 Troubleshooting

### Common Issues

1. **Application won't start**
   - Check Python version (3.7+ required)
   - Verify all dependencies are installed
   - Check if port 5000 is available

2. **Data not loading**
   - Ensure `data.json` exists in project root
   - Check JSON syntax validity
   - Verify file permissions

3. **Styling issues**
   - Clear browser cache
   - Check if `static/styles.css` is accessible
   - Verify Font Awesome CDN connection

### Debug Mode
Run with debug mode enabled:
```bash
export FLASK_DEBUG=1
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🔮 Future Enhancements

- **Machine Learning Integration**: Advanced NLP for better analysis
- **Multi-language Support**: Support for different languages
- **Document Upload**: PDF and Word document processing
- **User Accounts**: Save and manage analysis history
- **Advanced Analytics**: Detailed reporting and insights
- **API Integration**: Connect with legal databases
- **Mobile App**: Native mobile application
- **Export Features**: PDF and Word report generation

## 📊 Version History

### v2.0.0 (Current)
- Enhanced data structure with detailed explanations
- Improved risk categorization and analysis
- Modern responsive UI design
- Better error handling and validation
- Analysis history tracking
- Comprehensive documentation

### v1.0.0 (Initial)
- Basic document summarization
- Simple risk detection
- Basic clause explanations
- Flask web application

---

**LegalLenAI** - Making rental agreements understandable for everyone! 🏠⚖️
