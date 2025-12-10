import google.generativeai as genai
from django.conf import settings
import json
import logging
import os

logger = logging.getLogger(__name__)

class ComplaintAnalyzer:
    def __init__(self):
        # Try to get API key from settings first, then from environment
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not self.api_key:
            self.api_key = os.getenv("GEMINI_API_KEY")
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
            logger.warning("Gemini API key not configured")

    def analyze_complaint(self, subject, description, complaint_type):
        """
        Analyze complaint content and return priority level and analysis
        """
        if not self.model:
            return {
                'priority': 'medium',
                'analysis': 'AI analysis not available - API key not configured',
                'reasoning': 'Default priority assigned'
            }

        try:
            # Create prompt for analysis
            prompt = f"""
            Analyze this complaint and assign a priority level (urgent, high, medium, low) based on the content.
            
            Complaint Details:
            Subject: {subject}
            Type: {complaint_type}
            Description: {description}
            
            Please analyze the urgency and impact of this complaint and provide:
            1. Priority level (urgent/high/medium/low)
            2. Brief reasoning for the priority
            3. Key factors that influenced the decision
            
            Consider factors like:
            - Safety concerns
            - Academic impact
            - Infrastructure issues
            - Administrative matters
            - Time sensitivity
            - Number of people affected
            
            Respond in JSON format:
            {{
                "priority": "urgent/high/medium/low",
                "reasoning": "brief explanation",
                "key_factors": ["factor1", "factor2", "factor3"],
                "recommended_action": "suggested next steps"
            }}
            """

            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            try:
                # Try to extract JSON from the response
                response_text = response.text
                # Find JSON in the response
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    # Fallback if JSON parsing fails
                    analysis = {
                        'priority': 'medium',
                        'reasoning': 'AI analysis completed but parsing failed',
                        'key_factors': ['Content analysis performed'],
                        'recommended_action': 'Review complaint manually'
                    }
                
                return {
                    'priority': analysis.get('priority', 'medium'),
                    'analysis': response_text,
                    'reasoning': analysis.get('reasoning', 'AI analysis performed'),
                    'key_factors': analysis.get('key_factors', []),
                    'recommended_action': analysis.get('recommended_action', 'Standard processing')
                }
                
            except json.JSONDecodeError:
                # If JSON parsing fails, extract priority from text
                response_text = response.text.lower()
                priority = 'medium'  # default
                
                if 'urgent' in response_text:
                    priority = 'urgent'
                elif 'high' in response_text:
                    priority = 'high'
                elif 'low' in response_text:
                    priority = 'low'
                
                return {
                    'priority': priority,
                    'analysis': response.text,
                    'reasoning': 'Priority extracted from AI response',
                    'key_factors': ['AI analysis performed'],
                    'recommended_action': 'Review complaint manually'
                }
                
        except Exception as e:
            logger.error(f"Error analyzing complaint: {str(e)}")
            return {
                'priority': 'medium',
                'analysis': f'Error in AI analysis: {str(e)}',
                'reasoning': 'Default priority due to analysis error',
                'key_factors': ['Analysis error'],
                'recommended_action': 'Manual review required'
            }

    def get_priority_color(self, priority):
        """
        Get color class for priority display
        """
        color_map = {
            'urgent': 'danger',
            'high': 'warning',
            'medium': 'info',
            'low': 'success'
        }
        return color_map.get(priority, 'secondary')

    def get_priority_icon(self, priority):
        """
        Get Bootstrap icon for priority
        """
        icon_map = {
            'urgent': 'bi-exclamation-triangle-fill',
            'high': 'bi-exclamation-circle',
            'medium': 'bi-info-circle',
            'low': 'bi-check-circle'
        }
        return icon_map.get(priority, 'bi-question-circle') 