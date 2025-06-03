#!/usr/bin/env python3
"""
AI Review Analysis Service for Rentum AI
Analyzes review responses and generates AI scores, risk assessments, and flags
"""

import json
import re
from typing import Dict, List, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIReviewAnalyzer:
    def __init__(self):
        # Define scoring weights for different categories
        self.category_weights = {
            'payment_reliability': 0.25,
            'property_maintenance': 0.15,
            'communication': 0.15,
            'lease_compliance': 0.20,
            'responsiveness': 0.10,
            'property_condition': 0.10,
            'fairness': 0.03,
            'privacy_respect': 0.02
        }
        
        # Define green and red flag keywords
        self.green_flag_keywords = {
            'payment': ['timely', 'prompt', 'regular', 'consistent', 'reliable', 'punctual'],
            'maintenance': ['clean', 'well-maintained', 'careful', 'responsible', 'tidy'],
            'communication': ['responsive', 'clear', 'polite', 'professional', 'cooperative'],
            'behavior': ['respectful', 'quiet', 'friendly', 'trustworthy', 'honest']
        }
        
        self.red_flag_keywords = {
            'payment': ['late', 'delayed', 'missed', 'defaulted', 'irregular', 'bounced'],
            'maintenance': ['damaged', 'dirty', 'neglected', 'careless', 'messy'],
            'communication': ['unresponsive', 'rude', 'aggressive', 'difficult', 'argumentative'],
            'behavior': ['noisy', 'disruptive', 'problematic', 'unreliable', 'dishonest']
        }
    
    def analyze_review_response(self, review_data: Dict) -> Dict:
        """Analyze a single review response and generate AI insights"""
        try:
            # Extract review scores
            scores = {
                'payment_reliability': review_data.get('payment_reliability', 0),
                'property_maintenance': review_data.get('property_maintenance', 0),
                'communication': review_data.get('communication', 0),
                'lease_compliance': review_data.get('lease_compliance', 0),
                'responsiveness': review_data.get('responsiveness', 0),
                'property_condition': review_data.get('property_condition', 0),
                'fairness': review_data.get('fairness', 0),
                'privacy_respect': review_data.get('privacy_respect', 0)
            }
            
            # Calculate weighted AI score (0-10 scale)
            weighted_score = 0
            total_weight = 0
            
            for category, score in scores.items():
                if score > 0 and category in self.category_weights:
                    weight = self.category_weights[category]
                    weighted_score += (score / 5.0) * 10 * weight  # Convert 1-5 to 0-10 scale
                    total_weight += weight
            
            ai_overall_score = round(weighted_score / total_weight if total_weight > 0 else 0, 1)
            
            # Analyze comments for flags
            comments = review_data.get('comments', '').lower()
            green_flags, red_flags = self._analyze_comments(comments)
            
            # Determine risk assessment
            risk_assessment = self._calculate_risk_assessment(ai_overall_score, red_flags, scores)
            
            # Generate analysis summary
            analysis_summary = self._generate_analysis_summary(
                ai_overall_score, risk_assessment, green_flags, red_flags, scores
            )
            
            return {
                'ai_overall_score': ai_overall_score,
                'ai_risk_assessment': risk_assessment,
                'ai_green_flags': green_flags,
                'ai_red_flags': red_flags,
                'ai_analysis_summary': analysis_summary,
                'category_breakdown': scores
            }
            
        except Exception as e:
            logger.error(f"Error analyzing review response: {e}")
            return {
                'ai_overall_score': 0.0,
                'ai_risk_assessment': 'high',
                'ai_green_flags': [],
                'ai_red_flags': ['Analysis failed'],
                'ai_analysis_summary': f'Error in analysis: {str(e)}',
                'category_breakdown': {}
            }
    
    def _analyze_comments(self, comments: str) -> Tuple[List[str], List[str]]:
        """Analyze comments text for green and red flags"""
        green_flags = []
        red_flags = []
        
        # Check for green flag keywords
        for category, keywords in self.green_flag_keywords.items():
            for keyword in keywords:
                if keyword in comments:
                    flag_text = f"{category.title()}: {keyword}"
                    if flag_text not in green_flags:
                        green_flags.append(flag_text)
        
        # Check for red flag keywords
        for category, keywords in self.red_flag_keywords.items():
            for keyword in keywords:
                if keyword in comments:
                    flag_text = f"{category.title()}: {keyword}"
                    if flag_text not in red_flags:
                        red_flags.append(flag_text)
        
        # Additional pattern-based analysis
        if re.search(r'never|not|didn\'t|wouldn\'t|couldn\'t', comments):
            if any(word in comments for word in ['pay', 'payment', 'rent']):
                red_flags.append("Payment: Negative payment history mentioned")
        
        if re.search(r'always|every time|consistently', comments):
            if any(word in comments for word in ['pay', 'payment', 'rent', 'time']):
                green_flags.append("Payment: Consistent positive behavior")
        
        return green_flags[:5], red_flags[:5]  # Limit to top 5 flags each
    
    def _calculate_risk_assessment(self, ai_score: float, red_flags: List[str], scores: Dict) -> str:
        """Calculate risk assessment based on AI score and flags"""
        # Base risk on AI score
        if ai_score >= 8.0:
            base_risk = 'low'
        elif ai_score >= 6.0:
            base_risk = 'medium'
        else:
            base_risk = 'high'
        
        # Adjust based on red flags
        critical_red_flags = len([flag for flag in red_flags if 'payment' in flag.lower()])
        if critical_red_flags >= 2:
            return 'high'
        elif critical_red_flags >= 1 and base_risk != 'low':
            return 'high'
        
        # Check for critical low scores
        critical_scores = ['payment_reliability', 'lease_compliance']
        low_critical_scores = sum(1 for score_name in critical_scores if scores.get(score_name, 0) <= 2)
        
        if low_critical_scores >= 2:
            return 'high'
        elif low_critical_scores >= 1 and base_risk == 'high':
            return 'high'
        
        return base_risk
    
    def _generate_analysis_summary(self, ai_score: float, risk: str, green_flags: List[str], 
                                 red_flags: List[str], scores: Dict) -> str:
        """Generate a human-readable analysis summary"""
        summary_parts = []
        
        # Overall assessment
        if ai_score >= 8.0:
            summary_parts.append("Excellent tenant/landlord with strong overall performance.")
        elif ai_score >= 6.0:
            summary_parts.append("Good tenant/landlord with satisfactory performance.")
        elif ai_score >= 4.0:
            summary_parts.append("Average tenant/landlord with some areas for improvement.")
        else:
            summary_parts.append("Below-average tenant/landlord with significant concerns.")
        
        # Risk assessment
        risk_text = {
            'low': "Low risk - highly recommended.",
            'medium': "Medium risk - proceed with standard precautions.",
            'high': "High risk - requires careful consideration and additional safeguards."
        }
        summary_parts.append(risk_text.get(risk, "Risk assessment unavailable."))
        
        # Highlight strengths
        if green_flags:
            strengths = [flag.split(': ')[1] for flag in green_flags[:3]]
            summary_parts.append(f"Key strengths: {', '.join(strengths)}.")
        
        # Highlight concerns
        if red_flags:
            concerns = [flag.split(': ')[1] for flag in red_flags[:3]]
            summary_parts.append(f"Areas of concern: {', '.join(concerns)}.")
        
        # Category-specific insights
        if scores.get('payment_reliability', 0) >= 4:
            summary_parts.append("Strong payment history.")
        elif scores.get('payment_reliability', 0) <= 2:
            summary_parts.append("Payment reliability concerns noted.")
        
        return " ".join(summary_parts)
    
    def aggregate_user_profile(self, user_reviews: List[Dict]) -> Dict:
        """Aggregate multiple reviews to create a comprehensive user profile"""
        if not user_reviews:
            return {
                'overall_ai_score': 0.0,
                'total_reviews': 0,
                'category_averages': {},
                'green_flags_summary': {},
                'red_flags_summary': {},
                'risk_trend': 'unknown'
            }
        
        # Calculate averages
        total_reviews = len(user_reviews)
        category_sums = {}
        all_green_flags = []
        all_red_flags = []
        ai_scores = []
        
        for review in user_reviews:
            # Collect AI scores
            if 'ai_overall_score' in review:
                ai_scores.append(review['ai_overall_score'])
            
            # Collect category scores
            for category in self.category_weights.keys():
                if category in review:
                    if category not in category_sums:
                        category_sums[category] = []
                    category_sums[category].append(review[category])
            
            # Collect flags
            if 'ai_green_flags' in review:
                all_green_flags.extend(review['ai_green_flags'])
            if 'ai_red_flags' in review:
                all_red_flags.extend(review['ai_red_flags'])
        
        # Calculate averages
        overall_ai_score = round(sum(ai_scores) / len(ai_scores) if ai_scores else 0, 1)
        category_averages = {
            category: round(sum(scores) / len(scores), 2) if scores else 0
            for category, scores in category_sums.items()
        }
        
        # Count flag frequencies
        green_flags_count = {}
        for flag in all_green_flags:
            green_flags_count[flag] = green_flags_count.get(flag, 0) + 1
        
        red_flags_count = {}
        for flag in all_red_flags:
            red_flags_count[flag] = red_flags_count.get(flag, 0) + 1
        
        # Determine risk trend
        if len(ai_scores) >= 3:
            recent_scores = ai_scores[-3:]
            if all(score >= 7 for score in recent_scores):
                risk_trend = 'improving'
            elif all(score <= 5 for score in recent_scores):
                risk_trend = 'declining'
            else:
                risk_trend = 'stable'
        else:
            risk_trend = 'insufficient_data'
        
        return {
            'overall_ai_score': overall_ai_score,
            'total_reviews': total_reviews,
            'category_averages': category_averages,
            'green_flags_summary': green_flags_count,
            'red_flags_summary': red_flags_count,
            'risk_trend': risk_trend
        }

# Initialize AI review analyzer instance
ai_review_analyzer = AIReviewAnalyzer() 