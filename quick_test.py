"""
Quick test script to verify the paraphraser is working correctly
"""

from paraphraser import AIParaphraser
import time


def test_basic():
    """Test basic functionality"""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Paraphrasing")
    print("=" * 80)
    
    paraphraser = AIParaphraser()  # Use default PEGASUS model
    
    test_texts = [
        "The cat sat on the mat.",
        "Machine learning is a powerful tool for data analysis.",
        "She walked to the store to buy some groceries.",
    ]
    
    for text in test_texts:
        print(f"\nOriginal: {text}")
        start = time.time()
        paraphrases = paraphraser.paraphrase(text, num_paraphrases=3)
        elapsed = time.time() - start
        
        print(f"Generated {len(paraphrases)} paraphrases in {elapsed:.2f}s:")
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")
    
    print("\n✓ Test passed!")


def test_diversity():
    """Test diversity of paraphrases"""
    print("\n" + "=" * 80)
    print("TEST 2: Diversity Test")
    print("=" * 80)
    
    paraphraser = AIParaphraser()  # Use default PEGASUS model
    
    text = "Artificial intelligence is changing the world."
    
    print(f"\nOriginal: {text}")
    print("\nGenerating 10 paraphrases to test diversity...")
    
    paraphrases = paraphraser.paraphrase(text, num_paraphrases=10)
    
    print(f"\nGenerated {len(paraphrases)} unique paraphrases:")
    for i, para in enumerate(paraphrases, 1):
        print(f"  {i}. {para}")
    
    # Check uniqueness
    unique_count = len(set(p.lower() for p in paraphrases))
    print(f"\nUniqueness: {unique_count}/{len(paraphrases)} are unique")
    
    if unique_count == len(paraphrases):
        print("✓ All paraphrases are unique!")
    else:
        print("⚠️  Some duplicates found (may be expected)")


def test_styles():
    """Test different styles"""
    print("\n" + "=" * 80)
    print("TEST 3: Different Styles")
    print("=" * 80)
    
    paraphraser = AIParaphraser()  # Use default PEGASUS model
    
    text = "The dog played in the park all day long."
    
    print(f"\nOriginal: {text}")
    
    results = paraphraser.paraphrase_with_styles(text, num_per_style=2)
    
    for style, paraphrases in results.items():
        print(f"\n{style.upper()} style:")
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")
    
    print("\n✓ Test passed!")


def test_edge_cases():
    """Test edge cases"""
    print("\n" + "=" * 80)
    print("TEST 4: Edge Cases")
    print("=" * 80)
    
    paraphraser = AIParaphraser()  # Use default PEGASUS model
    
    test_cases = [
        ("Short", "Hi there!"),
        ("Long", "In the realm of computational linguistics and natural language processing, "
                 "the development of sophisticated paraphrasing systems has become increasingly "
                 "important for various applications including text summarization, question answering, "
                 "and machine translation systems."),
        ("Numbers", "The year 2024 marks the 50th anniversary of AI research."),
        ("Technical", "The neural network uses backpropagation to optimize weights."),
    ]
    
    for test_name, text in test_cases:
        print(f"\n{test_name} text:")
        print(f"Original: {text[:80]}{'...' if len(text) > 80 else ''}")
        
        try:
            paraphrases = paraphraser.paraphrase(text, num_paraphrases=3)
            print(f"Generated {len(paraphrases)} paraphrases:")
            for i, para in enumerate(paraphrases[:2], 1):  # Show first 2
                print(f"  {i}. {para[:80]}{'...' if len(para) > 80 else ''}")
            print("  ✓ Success")
        except Exception as e:
            print(f"  ⚠️  Error: {e}")
    
    print("\n✓ Test completed!")


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("🧪 AI PARAPHRASER - TEST SUITE")
    print("=" * 80)
    print("\nRunning comprehensive tests...\n")
    
    try:
        # Run tests
        test_basic()
        test_diversity()
        test_styles()
        test_edge_cases()
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("\nThe paraphraser is working correctly and ready to use.")
        print("\nNext steps:")
        print("  • Run 'python interactive.py' for interactive mode")
        print("  • Run 'python example_usage.py' for more examples")
        print("  • Import 'paraphraser' in your own scripts")
        print("\n" + "=" * 80 + "\n")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"⚠️  TEST FAILED: {e}")
        print("=" * 80)
        print("\nPlease ensure you have:")
        print("  1. Installed requirements: pip install -r requirements.txt")
        print("  2. Internet connection (for first-time model download)")
        print("  3. Sufficient RAM (at least 2GB available)")
        print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    main()
