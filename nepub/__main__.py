import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('novel_id', help='novel id', type=str)
    parser.add_argument('-o', '--output', metavar='<file>',
                        help='output file name', type=str, default='default.epub')
    args = parser.parse_args()
    convert_narou_to_epub(args.novel_id, args.output)


def convert_narou_to_epub(novel_id: str, output: str):
    print(f'novel_id: {novel_id}, output: {output}')


if __name__ == '__main__':
    main()
