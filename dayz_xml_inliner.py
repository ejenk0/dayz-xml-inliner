import xml.etree.ElementTree as ET
from os import name as os_name
from os.path import abspath, dirname, join, exists, samefile
from contextlib import redirect_stdout
from pathlib import PureWindowsPath


def main(args):
    if args.benchmark:
        from timeit import default_timer as timer

        process_start = timer()

    input_path = abspath(args.input)
    input_dir = dirname(input_path)
    output_path = abspath(args.output)

    # Check the file paths are valid
    if not exists(input_path):
        print(f"Input file does not exist: {input_path}")
        return 1
    if not exists(dirname(output_path)):
        print(f"Output directory does not exist: {dirname(output_path)}")
        return 1
    if exists(output_path):
        if args.force:
            print(f"Output file already exists: {output_path}. It will be overwritten.")
        else:
            if samefile(input_path, output_path):
                print(
                    "Input and output files are the same. You probably didn't want that..."
                )
                return 1
            print(f"Output file already exists: {output_path}. Use -f to overwrite.")
            return 1

    # Parse the input XML file
    with open(input_path, "r") as f:
        if args.verbose:
            print(f"Parsing input file: {input_path}")
        tree = ET.parse(f)
        if args.verbose:
            print(f"DONE: Parsing input file: {input_path}")
        if args.benchmark:
            input_parse_done = timer()
            print(f"Finished parsing input: {(input_parse_done - process_start):.2f}s")

    if args.verbose:
        print("Finding include tags in input file")
    root = tree.getroot()
    include_tags = tree.findall("include")
    include_tag_count = len(include_tags)
    if args.verbose:
        print(f"DONE: Found {include_tag_count} include tags in input file")
    if args.benchmark:
        include_tags_done = timer()
        print(
            f"Finished finding include tags: {(include_tags_done - input_parse_done):.2f}s"
        )

    if args.verbose:
        print("Inlining included files")
        report_frequency = max(include_tag_count // 10, 1)
        freq_percent = report_frequency / include_tag_count * 100
        count = 0
        if args.benchmark:
            last_report = timer()
    # Replace the include tags with the contents of the included files
    for include_tag in include_tags:
        # Convert the path to a platform-specific path
        if os_name == "posix":
            path = join(input_dir, PureWindowsPath(include_tag.text).as_posix())
        else:
            path = join(input_dir, include_tag.text)

        root.append(ET.parse(path).getroot())
        root.remove(include_tag)

        if args.verbose:
            count += 1
            if count % report_frequency == 0:
                if not args.benchmark:
                    print(
                        f"  ({((count / include_tag_count) * 100):.1f}%) Processed {count} of {include_tag_count} include tags."
                    )
                else:
                    now = timer()
                    print(
                        f"  ({((count / include_tag_count) * 100):.1f}%) Processed {count} of {include_tag_count} include tags. Last {freq_percent:.1f}% took {(now - last_report):.2f}s"
                    )
                    last_report = now
    if args.verbose:
        print(f"DONE: Inlined {include_tag_count} included files")
    if args.benchmark:
        inlining_done = timer()
        print(
            f"Finished inlining included files: {(inlining_done - include_tags_done):.2f}s"
        )

    if args.verbose:
        print(f"Writing output file: {output_path}")
    # Format the XML nicely
    ET.indent(root)

    # Output the XML to a file
    with open(output_path, "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)

    if args.benchmark:
        output_done = timer()

    if args.verbose:
        with open(output_path, "r") as f:
            print(
                f"DONE: Writing output file: {output_path}. {len(f.readlines())} lines written."
            )
    if args.benchmark:
        print(f"Finished writing output: {(output_done - inlining_done):.2f}s")
        print(f"Total time: {(output_done - process_start):.2f}s")

    return 0


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        prog="python3 dayz_xml_inliner.py",
        description="Parse an XML file with include tags and emit a new XML file with the included files inlined.",
    )
    parser.add_argument("input", help="The input XML file")
    parser.add_argument("output", help="The output XML file")
    parser.add_argument(
        "-f",
        "--force",
        dest="force",
        help="Overwrite the output file if it already exists",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="Print verbose output",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--silent",
        dest="silent",
        help="Suppress all output. WARN: The program fail silently.",
        action="store_true",
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        dest="benchmark",
        help="Run the program in benchmark mode.",
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.silent:
        with redirect_stdout(None):
            exit_code = main(args)
    else:
        exit_code = main(args)
    exit(exit_code)
