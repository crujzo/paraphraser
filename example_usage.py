"""
Example usage of the AI Paraphraser
"""

from paraphraser import AIParaphraser


def example_basic():
    """Basic paraphrasing example"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Paraphrasing")
    print("=" * 80)
    
    paraphraser = AIParaphraser(model_name="t5-base")
    
    text = "Machine learning is a subset of artificial intelligence that enables computers to learn from data."
    
    print(f"\nOriginal: {text}")
    print("\nParaphrases:")
    
    paraphrases = paraphraser.paraphrase(text, num_paraphrases=5)
    
    for i, para in enumerate(paraphrases, 1):
        print(f"  {i}. {para}")


def example_different_styles():
    """Generate paraphrases with different styles"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Different Paraphrasing Styles")
    print("=" * 80)
    
    paraphraser = AIParaphraser(model_name="t5-base")
    
    text = "The cat sat on the mat and watched the birds flying in the sky."
    
    print(f"\nOriginal: {text}")
    
    results = paraphraser.paraphrase_with_styles(text, num_per_style=2)
    
    for style, paraphrases in results.items():
        print(f"\n{style.upper()} style:")
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")


def example_batch_processing():
    """Process multiple texts at once"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Batch Processing")
    print("=" * 80)
    
    paraphraser = AIParaphraser(model_name="t5-base")
    
    texts = [
        "Python is a popular programming language.",
        "The weather is beautiful today.",
        "She enjoys reading books in her free time.",
    ]
    
    results = paraphraser.batch_paraphrase(texts, num_paraphrases=3)
    
    for original, paraphrases in results.items():
        print(f"\nOriginal: {original}")
        print("Paraphrases:")
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")


def example_custom_parameters():
    """Use custom parameters for fine-tuned control"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Custom Parameters")
    print("=" * 80)
    
    paraphraser = AIParaphraser(model_name="t5-base")
    
    text = "Artificial intelligence is transforming the way we live and work."
    
    print(f"\nOriginal: {text}")
    
    # Conservative (more similar to original)
    print("\nConservative paraphrases (low temperature):")
    conservative = paraphraser.paraphrase(
        text,
        num_paraphrases=3,
        temperature=0.7,
        diversity_penalty=0.5
    )
    for i, para in enumerate(conservative, 1):
        print(f"  {i}. {para}")
    
    # Creative (more diverse)
    print("\nCreative paraphrases (high temperature):")
    creative = paraphraser.paraphrase(
        text,
        num_paraphrases=3,
        temperature=2.0,
        diversity_penalty=2.0
    )
    for i, para in enumerate(creative, 1):
        print(f"  {i}. {para}")


def interactive_mode():
    """Interactive paraphrasing mode"""
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("=" * 80)
    
    paraphraser = AIParaphraser(model_name="t5-base")
    
    print("\nEnter text to paraphrase (or 'quit' to exit)")
    
    while True:
        print("\n" + "-" * 80)
        text = input("\nYour text: ").strip()
        
        if text.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not text:
            print("Please enter some text.")
            continue
        
        try:
            num = input("How many paraphrases? (default: 5): ").strip()
            num_paraphrases = int(num) if num else 5
        except ValueError:
            num_paraphrases = 5
        
        print(f"\nGenerating {num_paraphrases} paraphrases...\n")
        paraphrases = paraphraser.paraphrase(text, num_paraphrases=num_paraphrases)
        
        print("Paraphrases:")
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")


if __name__ == "__main__":
    print("\n🔄 AI Paraphraser - Example Usage\n")
    
    # Run examples
    example_basic()
    example_different_styles()
    example_batch_processing()
    example_custom_parameters()
    
    # Uncomment to try interactive mode
    # interactive_mode()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80 + "\n")
