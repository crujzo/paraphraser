"""
Interactive Paraphraser - Chat-style interface for paraphrasing
"""

from paraphraser import AIParaphraser
import sys


def print_header():
    """Print welcome header"""
    print("\n" + "=" * 80)
    print("🔄  AI PARAPHRASER - Interactive Mode")
    print("=" * 80)
    print("\nGenerate multiple diverse paraphrases of any text!")
    print("Commands: 'quit' or 'exit' to leave, 'help' for options")
    print("=" * 80 + "\n")


def print_help():
    """Print help information"""
    print("\n" + "-" * 80)
    print("HELP - Available Options")
    print("-" * 80)
    print("• Just type your text and press Enter to paraphrase")
    print("• Specify number of paraphrases when prompted (default: 5)")
    print("• Type 'quit' or 'exit' to leave")
    print("• Type 'settings' to change default parameters")
    print("• Type 'styles' to see different paraphrasing styles")
    print("-" * 80 + "\n")


def show_styles(paraphraser, text):
    """Show different paraphrasing styles"""
    print("\n" + "-" * 80)
    print("Showing different styles for your text...")
    print("-" * 80)
    
    styles_config = {
        "Conservative": {"temperature": 0.7, "diversity_penalty": 0.5},
        "Balanced": {"temperature": 1.2, "diversity_penalty": 1.0},
        "Creative": {"temperature": 1.8, "diversity_penalty": 1.5},
        "Diverse": {"temperature": 2.0, "diversity_penalty": 2.0},
    }
    
    for style_name, params in styles_config.items():
        print(f"\n{style_name} Style:")
        paraphrases = paraphraser.paraphrase(
            text,
            num_paraphrases=2,
            **params
        )
        for i, para in enumerate(paraphrases, 1):
            print(f"  {i}. {para}")
    
    print("\n" + "-" * 80)


def main():
    """Main interactive loop"""
    print_header()
    
    # Initialize paraphraser
    print("Loading AI model (this may take a moment)...\n")
    try:
        paraphraser = AIParaphraser(model_name="t5-base")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("\nTrying smaller model (t5-small)...")
        try:
            paraphraser = AIParaphraser(model_name="t5-small")
        except Exception as e:
            print(f"Error: {e}")
            print("\nPlease ensure you have installed the requirements:")
            print("  pip install -r requirements.txt")
            sys.exit(1)
    
    print("\n✓ Model loaded! Ready to paraphrase.\n")
    
    # Default settings
    default_num_paraphrases = 5
    default_temperature = 1.5
    default_diversity = 1.0
    
    while True:
        print("-" * 80)
        
        # Get input text
        text = input("\nEnter text to paraphrase (or 'quit'/'help'): ").strip()
        
        # Handle commands
        if text.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using AI Paraphraser! Goodbye!\n")
            break
        
        if text.lower() == 'help':
            print_help()
            continue
        
        if not text:
            print("⚠️  Please enter some text.")
            continue
        
        # Ask for number of paraphrases
        try:
            num_input = input(f"How many paraphrases? (default: {default_num_paraphrases}): ").strip()
            num_paraphrases = int(num_input) if num_input else default_num_paraphrases
            
            if num_paraphrases < 1:
                print("⚠️  Number must be at least 1. Using default.")
                num_paraphrases = default_num_paraphrases
            elif num_paraphrases > 20:
                print("⚠️  That's a lot! Limiting to 20 paraphrases.")
                num_paraphrases = 20
        except ValueError:
            print(f"⚠️  Invalid number. Using default ({default_num_paraphrases}).")
            num_paraphrases = default_num_paraphrases
        
        # Ask if they want to see different styles
        style_input = input("See different styles? (y/N): ").strip().lower()
        
        if style_input in ['y', 'yes']:
            show_styles(paraphraser, text)
            continue
        
        # Generate paraphrases
        print(f"\n⏳ Generating {num_paraphrases} paraphrases...\n")
        
        try:
            paraphrases = paraphraser.paraphrase(
                text,
                num_paraphrases=num_paraphrases,
                temperature=default_temperature,
                diversity_penalty=default_diversity
            )
            
            # Display results
            print("✓ Paraphrases:\n")
            print(f"  Original: {text}\n")
            
            if paraphrases:
                for i, para in enumerate(paraphrases, 1):
                    print(f"  {i}. {para}")
            else:
                print("  ⚠️  No paraphrases generated. Try adjusting parameters or a different text.")
            
            print()
            
            # Ask if they want to save
            save = input("Save these paraphrases to a file? (y/N): ").strip().lower()
            if save in ['y', 'yes']:
                filename = input("Enter filename (default: paraphrases.txt): ").strip()
                if not filename:
                    filename = "paraphrases.txt"
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Original: {text}\n\n")
                        f.write("Paraphrases:\n")
                        for i, para in enumerate(paraphrases, 1):
                            f.write(f"{i}. {para}\n")
                    print(f"✓ Saved to {filename}")
                except Exception as e:
                    print(f"⚠️  Error saving file: {e}")
        
        except Exception as e:
            print(f"⚠️  Error generating paraphrases: {e}")
            print("Please try again with different text or settings.")
        
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
        sys.exit(0)
