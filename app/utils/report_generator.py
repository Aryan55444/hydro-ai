from fpdf import FPDF
from datetime import datetime
import os
from typing import Dict, List, Optional, Union

def create_prediction_content(prediction_data: Dict) -> str:
    """Generate formatted prediction content for the report.
    
    Args:
        prediction_data: Dictionary containing prediction results and statistics
        
    Returns:
        Formatted string with prediction details
    """
    if not all(key in prediction_data for key in ['target_column', 'prediction', 'stats', 'percentile']):
        raise ValueError("Missing required keys in prediction_data")
        
    content = [
        f"Prediction for {prediction_data['target_column']}:",
        f"- Predicted Value: {float(prediction_data['prediction']):.4f}",
        "\nDataset Statistics:",
        f"- Minimum: {float(prediction_data['stats']['min']):.4f}",
        f"- 25th Percentile: {float(prediction_data['stats']['25%']):.4f}",
        f"- Median: {float(prediction_data['stats']['50%']):.4f}",
        f"- 75th Percentile: {float(prediction_data['stats']['75%']):.4f}",
        f"- Maximum: {float(prediction_data['stats']['max']):.4f}",
        f"\nPercentile Rank: {float(prediction_data['percentile']):.1f}%"
    ]
    
    if 'features' in prediction_data and prediction_data['features']:
        content.append("\nFeature Values Used:")
        for feature, value in prediction_data['features'].items():
            content.append(f"- {feature}: {value}")
    
    return "\n".join(content)

def generate_pdf(
    sections: List[Dict[str, str]], 
    title: str = "Water Quality Report", 
    output_path: Optional[str] = None
) -> str:
    """Generate a PDF report with the given sections.
    
    Args:
        sections: List of dictionaries with 'title' and 'content' keys
        title: Report title
        output_path: Path to save the PDF (default: auto-generated filename)
        
    Returns:
        Path to the generated PDF file
    """
    if not sections:
        raise ValueError("No sections provided for the report")
        
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_title(title)
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, title, 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font('Arial', 'I', 10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
    pdf.ln(10)
    
    for section in sections:
        if not all(key in section for key in ['title', 'content']):
            continue
            
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, section['title'], 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font('Arial', '', 12)
        pdf.multi_cell(0, 10, str(section['content']))
        pdf.ln(8)
    
    if output_path is None:
        output_path = os.path.join(
            os.getcwd(),
            f"water_quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    else:
        output_path = os.path.abspath(output_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        pdf.output(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to generate PDF: {str(e)}")

def generate_prediction_report(
    prediction_data: Dict, 
    analysis_text: str = "", 
    output_path: Optional[str] = None
) -> str:
    """Generate a water quality prediction report in PDF format.
    
    Args:
        prediction_data: Dictionary containing prediction results and statistics
        analysis_text: Optional analysis text to include in the report
        output_path: Path to save the report (default: auto-generated filename)
        
    Returns:
        Path to the generated PDF file
        
    Raises:
        ValueError: If prediction_data is missing required fields
        RuntimeError: If PDF generation fails
    """
    if not prediction_data:
        raise ValueError("No prediction data provided")
    
    sections = []
    
    try:
        prediction_content = create_prediction_content(prediction_data)
        sections.append({
            'title': 'Prediction Results',
            'content': prediction_content
        })
        
        if analysis_text and str(analysis_text).strip():
            sections.append({
                'title': 'Analysis',
                'content': str(analysis_text).strip()
            })
        
        return generate_pdf(
            sections, 
            title="Water Quality Prediction Report",
            output_path=output_path
        )
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate prediction report: {str(e)}")
