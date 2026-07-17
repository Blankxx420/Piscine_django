from local_lib import path

def main():
    target_dir = path.Path("test_dir")
    target_file = target_dir / "test_file.txt"

    if not target_dir.exists():
        target_dir.mkdir()
        print(f"Directory '{target_dir}' created")

    content_to_write = "Hello 42! This file was manipulated with path.py."
    target_file.write_text(content_to_write)
    print(f"Writing '{target_file}' done")

    content_read = target_file.read_text()
    print("\n--- Content of the file ---")
    print(content_read)
    print("-----------------------------\n")


if __name__ == "__main__":
    main()