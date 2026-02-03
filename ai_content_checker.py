import re
import math
from collections import Counter

class AIContentChecker:
    def __init__(self):
        # Common AI buzzwords and phrases
        self.ai_phrases = [
            "delve", "tapestry", "testament", "landscape", "realm",
            "highly motivated professional", "strong problem-solving skills", 
            "proven track record", "dynamic environment", "foster innovation",
            "spearheaded", "leveraged", "orchestrated", "meticulous attention to detail",
            "unwavering commitment", "paramount importance"
        ]

    def _calculate_perplexity(self, text):
        """
        Calculates a heuristic perplexity score based on common bigrams/trigrams.
        True perplexity requires a language model, but this is a statistical proxy.
        Low variation/high predictability = Low Perplexity (Likely AI).
        """
        words = text.split()
        if not words:
            return 0
        
        unique_words = len(set(words))
        total_words = len(words)
        
        # TTR (Type-Token Ratio) - AI tends to reuse words less randomly than humans in short bursts,
        # but in long form, it can differ. Low TTR can imply repetitive/simple text.
        ttr = unique_words / total_words if total_words > 0 else 0
        
        # Heuristic: Lower TTR *might* indicate more formulaic text, 
        # but for this "Perplexity" proxy, we'll invert it to map to "Entropy".
        # Higher Entropy = Human.
        return ttr * 100

    def _calculate_burstiness(self, text):
        """
        Calculates burstiness based on sentence length standard deviation.
        AI text often has uniform sentence lengths (Low Burstiness).
        Humans vary short and long sentences (High Burstiness).
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0
        
        lengths = [len(s.split()) for s in sentences]
        mean_len = sum(lengths) / len(lengths)
        
        # Standard Deviation
        variance = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
        std_dev = math.sqrt(variance)
        
        # Normalize: Higher Std Dev = More Burstiness = More Likely Human
        # Score 0-100
        burstiness_score = min(std_dev * 5, 100)
        return burstiness_score

    def _check_repetition_and_phrases(self, text):
        """
        Checks for overused AI phrases and repetitive patterns.
        """
        text_lower = text.lower()
        phrase_count = 0
        for phrase in self.ai_phrases:
            if phrase in text_lower:
                phrase_count += 1
        
        # Normalize: More phrases = Higher AI likelihood
        # Cap at 10 phrases for max score contribution
        phrase_score = min(phrase_count * 10, 100)
        return phrase_score

    def analyze(self, text):
        if not text:
            return {"ai_probability": 0, "verdict": "Unknown", "details": {}}
        
        # 1. Burstiness (Low = AI)
        burstiness = self._calculate_burstiness(text)
        # Invert for AI score: Low burstiness -> High AI Probability
        ai_burstiness = max(0, 100 - burstiness)
        
        # 2. Perplexity Proxy (Low complexity = AI)
        perplexity_proxy = self._calculate_perplexity(text)
        # Invert: Low complexity -> High AI Probability
        ai_perplexity = max(0, 100 - (perplexity_proxy * 1.5)) # Scale factor
        
        # 3. Phrase Detection (High = AI)
        ai_phrasing = self._check_repetition_and_phrases(text)
        
        # Weighted Average
        # Burstiness: 40%, Phrasing: 40%, Perplexity: 20%
        ai_probability = (ai_burstiness * 0.4) + (ai_phrasing * 0.4) + (ai_perplexity * 0.2)
        ai_probability = min(max(ai_probability, 0), 100)
        
        if ai_probability > 70:
            verdict = "Likely AI-generated"
        elif ai_probability > 40:
            verdict = "Mixed / Unclear"
        else:
            verdict = "Likely Human"
            
        return {
            "ai_probability": round(ai_probability, 2),
            "verdict": verdict,
            "breakdown": {
                "burstiness_score": round(burstiness, 2), # Show raw human score
                "perplexity_score": round(perplexity_proxy, 2), # Show raw human score
                "ai_phrases_detected": ai_phrasing / 10 # approximate count
            }
        }
