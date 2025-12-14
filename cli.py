#!/usr/bin/env python3
"""
Command-line interface for AI Paraphraser
Usage: python cli.py "Your text here" [--num 5] [--style creative]
"""

import argparse
import sys
from paraphraser import AIParaphraser


def main():
    parser = argparse.ArgumentParser(
        description='AI Paraphraser - Generate multiple diverse paraphrases',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py "Hello world"
  python cli.py "The cat sat on the mat" --num 7
  python cli.py "Machine learning rocks" --style creative
  python cli.py "AI is amazing" --num 5 --temperature 2.0
  python cli.py "Your text" --output paraphrases.txt

Styles:
  conservative  - Subtle changes, close to original
  balanced      - Moderate variations (default)
  creative      - More diverse paraphrases  
  diverse       - Maximum diversity
        """
    )
    
    parser.add_argument(
        'text',
        nargs='?',
        help='Text to paraphrase (or use --file)'
    )
    
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=5,
        help='Number of paraphrases to generate (default: 5)'
    )
    
    parser.add_argument(
        '-s', '--style',
        choices=['conservative', 'balanced', 'creative', 'diverse'],
        default='balanced',
        help='Paraphrasing style (default: balanced)'
    )
    
    parser.add_argument(
        '-t', '--temperature',
        type=float,
        help='Temperature for generation (0.5-2.5, overrides style)'
    )
    
    parser.add_argument(
        '-d', '--diversity',
        type=float,
        help='Diversity penalty (0.5-2.0, overrides style)'
    )
    
    parser.add_argument(
        '-m', '--model',
        choices=['t5-small', 't5-base', 't5-large'],
        default='t5-base',
        help='Model to use (default: t5-base)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file to save results'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Read input text from file'
    )
    
    parser.add_argument(
        '--no-numbering',
        action='store_true',
        help='Do not number the paraphrases'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Minimal output (no loading messages)'
    )
    
    args = parser.parse_args()
    
    # Get input text
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)
    
    if not text:
        print("Error: No text provided", file=sys.stderr)
        sys.exit(1)
    
    # Style presets
    style_params = {
        'conservative': {'temperature': 0.7, 'diversity_penalty': 0.5},
        'balanced': {'temperature': 1.2, 'diversity_penalty': 1.0},
        'creative': {'temperature': 1.8, 'diversity_penalty': 1.5},
        'diverse': {'temperature': 2.0, 'diversity_penalty': 2.0},
    }
    
    # Get parameters
    params = style_params[args.style].copy()
    
    # Override with command-line args if provided
    if args.temperature is not None:
        params['temperature'] = args.temperature
    if args.diversity is not None:
        params['diversity_penalty'] = args.diversity
    
    # Load model
    if not args.quiet:
        print(f"Loading {args.model} model...", file=sys.stderr)
    
    try:
        paraphraser = AIParaphraser(model_name=args.model)
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not args.quiet:
        print(f"Generating {args.num} paraphrases...\n", file=sys.stderr)
    
    # Generate paraphrases
    try:
        paraphrases = paraphraser.paraphrase(
            text,
            num_paraphrases=args.num,
            **params
        )
    except Exception as e:
        print(f"Error generating paraphrases: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Format output
    output_lines = []
    
    if not args.quiet:
        output_lines.append(f"Original: {text}\n")
    
    for i, para in enumerate(paraphrases, 1):
        if args.no_numbering:
            output_lines.append(para)
        else:
            output_lines.append(f"{i}. {para}")
    
    output_text = '\n'.join(output_lines)
    
    # Save or print
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_text)
            if not args.quiet:
                print(f"\nSaved to {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error saving file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
