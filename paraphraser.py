"""
AI Paraphraser - Generate multiple diverse paraphrases of input text
"""

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from typing import List, Dict, Optional
import re
import warnings
warnings.filterwarnings('ignore')


class AIParaphraser:
    """
    A sophisticated paraphraser that generates multiple diverse paraphrases
    using transformer models and various decoding strategies.
    """
    
    def __init__(self, model_name: str = "tuner007/pegasus_paraphrase", device: Optional[str] = None):
        """
        Initialize the paraphraser with a pre-trained model.
        
        Args:
            model_name: Name of the model to use 
                       Default: tuner007/pegasus_paraphrase (fine-tuned specifically for paraphrasing)
                       Other options: ramsrigouthamg/t5_paraphraser, t5-base
            device: Device to run on ('cuda', 'mps', or 'cpu')
        """
        print(f"Loading model: {model_name}...")
        
        # Determine device
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
        
        print(f"Using device: {self.device}")
        
        # Load model and tokenizer based on model type
        if "pegasus" in model_name.lower():
            from transformers import PegasusForConditionalGeneration, PegasusTokenizer
            self.tokenizer = PegasusTokenizer.from_pretrained(model_name)
            self.model = PegasusForConditionalGeneration.from_pretrained(model_name)
        else:
            # T5-based models
            self.tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=False)
            self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        
        self.model.to(self.device)
        self.model.eval()
        
        print("Model loaded successfully!")
    
    def paraphrase(
        self,
        text: str,
        num_paraphrases: int = 5,
        max_length: int = 512,  # Increased default from 128
        temperature: float = 1.5,
        top_k: int = 50,
        top_p: float = 0.95,
        diversity_penalty: float = 1.0,
        num_beams: int = 5,
    ) -> List[str]:
        """
        Generate multiple paraphrases using diverse sampling strategies.
        
        Args:
            text: Input text to paraphrase
            num_paraphrases: Number of different paraphrases to generate
            max_length: Maximum length of generated text
            temperature: Controls randomness (higher = more diverse)
            top_k: Top-k sampling parameter
            top_p: Nucleus sampling parameter
            diversity_penalty: Penalty for generating similar outputs
            num_beams: Number of beams for beam search
        
        Returns:
            List of paraphrased texts
        """
        # Prepare input (PEGASUS doesn't need prefix, T5 does)
        input_text = text  # PEGASUS uses text directly for paraphrasing
        
        # Tokenize input (increased max_length for longer texts)
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            max_length=1024,  # Increased from 512
            truncation=True,
            padding=True
        ).to(self.device)
        
        paraphrases = []
        
        # Generate paraphrases using diverse sampling
        with torch.no_grad():
            # Generate more outputs than requested to ensure diversity after filtering
            actual_num_to_generate = num_paraphrases * 3  # Generate 3x more
            
            # Use beam search with sampling for diversity and quality
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=actual_num_to_generate,
                num_beams=max(actual_num_to_generate, 5),
                temperature=temperature,
                do_sample=True,
                top_k=top_k,
                top_p=top_p,
                repetition_penalty=1.2,  # Penalize repetition
                no_repeat_ngram_size=3,  # Avoid repeating 3-grams
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode outputs
        for output in outputs:
            paraphrase = self.tokenizer.decode(output, skip_special_tokens=True)
            if paraphrase and paraphrase.strip():
                # Clean up the paraphrase
                paraphrase = paraphrase.strip()
                # Only add if it's different from the original
                if paraphrase.lower() != text.lower():
                    paraphrases.append(paraphrase)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_paraphrases = []
        for p in paraphrases:
            # Use normalized version for comparison
            normalized = ' '.join(p.lower().split())
            if normalized not in seen:
                seen.add(normalized)
                unique_paraphrases.append(p)
        
        # Return only the requested number
        return unique_paraphrases[:num_paraphrases]
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences, handling semicolons and periods."""
        # Split on periods, exclamation marks, question marks, and semicolons
        # But keep semicolons as part of the sentence for now
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Further split on semicolons if the resulting parts are substantial
        all_sentences = []
        for sent in sentences:
            # If sentence has semicolon, consider it as sentence boundary
            if ';' in sent:
                parts = [p.strip() for p in sent.split(';') if p.strip()]
                all_sentences.extend(parts)
            else:
                all_sentences.append(sent.strip())
        
        return [s for s in all_sentences if s and len(s) > 10]  # Filter very short fragments
    
    def paraphrase_paragraph(
        self,
        text: str,
        num_paraphrases: int = 5,
        **kwargs
    ) -> List[str]:
        """
        Paraphrase longer texts (paragraphs) by processing sentence by sentence.
        Better for multi-sentence inputs.
        
        Args:
            text: Input paragraph to paraphrase
            num_paraphrases: Number of paragraph variations to generate
            **kwargs: Additional parameters for paraphrase method
        
        Returns:
            List of paraphrased paragraphs
        """
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        if len(sentences) <= 1:
            # Single sentence, use regular paraphrase
            return self.paraphrase(text, num_paraphrases=num_paraphrases, **kwargs)
        
        # Calculate how many variations we need per sentence to get enough combinations
        # We want at least num_paraphrases * 2 to ensure enough variety
        variations_per_sentence = max(4, num_paraphrases)
        
        # Paraphrase each sentence
        sentence_variations = []
        for i, sentence in enumerate(sentences):
            print(f"Paraphrasing sentence {i+1}/{len(sentences)}...")
            variations = self.paraphrase(
                sentence, 
                num_paraphrases=variations_per_sentence,
                **kwargs
            )
            if variations:
                sentence_variations.append(variations)
            else:
                sentence_variations.append([sentence])  # Keep original if no variations
        
        # Combine sentences to create paragraph variations
        paragraph_variations = []
        import random
        
        # Generate combinations with some randomness
        attempts = 0
        max_attempts = num_paraphrases * 10  # Try up to 10x the requested amount
        
        while len(paragraph_variations) < num_paraphrases and attempts < max_attempts:
            attempts += 1
            
            # Pick a variation from each sentence
            paragraph_parts = []
            for j, variations in enumerate(sentence_variations):
                if attempts < num_paraphrases:
                    # First N attempts: cycle through systematically
                    idx = attempts % len(variations)
                else:
                    # After that: pick randomly for more diversity
                    idx = random.randint(0, len(variations) - 1)
                paragraph_parts.append(variations[idx])
            
            # Join into paragraph
            paragraph = ' '.join(paragraph_parts)
            
            # Check if it's unique (case-insensitive)
            normalized = ' '.join(paragraph.lower().split())
            if not any(normalized == ' '.join(p.lower().split()) for p in paragraph_variations):
                paragraph_variations.append(paragraph)
        
        return paragraph_variations[:num_paraphrases]
    
    def paraphrase_with_styles(
        self,
        text: str,
        num_per_style: int = 2,
        max_length: int = 128,
    ) -> Dict[str, List[str]]:
        """
        Generate paraphrases using different styles/strategies.
        
        Args:
            text: Input text to paraphrase
            num_per_style: Number of paraphrases per style
            max_length: Maximum length of generated text
        
        Returns:
            Dictionary mapping style names to lists of paraphrases
        """
        styles = {
            "conservative": {
                "temperature": 0.7,
                "top_p": 0.9,
                "diversity_penalty": 0.5,
            },
            "balanced": {
                "temperature": 1.2,
                "top_p": 0.95,
                "diversity_penalty": 1.0,
            },
            "creative": {
                "temperature": 1.8,
                "top_p": 0.98,
                "diversity_penalty": 1.5,
            },
            "diverse": {
                "temperature": 2.0,
                "top_p": 0.99,
                "diversity_penalty": 2.0,
            },
        }
        
        results = {}
        
        for style_name, params in styles.items():
            print(f"Generating {style_name} paraphrases...")
            paraphrases = self.paraphrase(
                text,
                num_paraphrases=num_per_style,
                max_length=max_length,
                **params
            )
            results[style_name] = paraphrases
        
        return results
    
    def batch_paraphrase(
        self,
        texts: List[str],
        num_paraphrases: int = 3,
        max_length: int = 128,
    ) -> Dict[str, List[str]]:
        """
        Generate paraphrases for multiple texts.
        
        Args:
            texts: List of input texts
            num_paraphrases: Number of paraphrases per text
            max_length: Maximum length of generated text
        
        Returns:
            Dictionary mapping original texts to their paraphrases
        """
        results = {}
        
        for text in texts:
            print(f"Processing: {text[:50]}...")
            paraphrases = self.paraphrase(
                text,
                num_paraphrases=num_paraphrases,
                max_length=max_length
            )
            results[text] = paraphrases
        
        return results


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("AI Paraphraser Demo")
    print("=" * 70)
    
    # Initialize paraphraser
    paraphraser = AIParaphraser(model_name="t5-base")
    
    # Example text
    text = "The quick brown fox jumps over the lazy dog."
    
    print(f"\nOriginal text: {text}")
    print("\n" + "-" * 70)
    
    # Generate paraphrases
    print("\nGenerating 7 diverse paraphrases...\n")
    paraphrases = paraphraser.paraphrase(text, num_paraphrases=7)
    
    for i, para in enumerate(paraphrases, 1):
        print(f"{i}. {para}")
    
    print("\n" + "=" * 70)
