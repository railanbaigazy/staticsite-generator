import os
import shutil
import logging

def copy_directory_contents(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        logging.error(f"Source directory '{source_dir}' does not exist.")
        return

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        dest_item = os.path.join(dest_dir, item)
        
        if os.path.isdir(source_item):
            copy_directory_contents(source_item, dest_item)
        elif os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
            logging.info(f"Copied file: {source_item} -> {dest_item}")
        else:
            logging.warning(f"Ignoring item: {source_item}")

def main():
    source_dir = "static"
    dest_dir = "public"
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        logging.info(f"Deleted contents of {dest_dir}")
    
    copy_directory_contents(source_dir, dest_dir)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
