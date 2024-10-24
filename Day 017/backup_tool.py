import os
import shutil
import zipfile
import time
from datetime import datetime
from contextlib import contextmanager
import logging


class BackupLogger:
    def __init__(self, log_file):
        self.log_file = log_file

    def __enter__(self):
        self.logger = logging.getLogger("BackupTool")
        self.logger.setLevel(logging.INFO)

        # Create file handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Remove all handlers
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        if exc_type is not None:
            return False  # Propagate exception
        return True


@contextmanager
def change_dir(destination):
    """Context manager for changing the current working directory."""
    current_dir = os.getcwd()
    try:
        os.chdir(destination)
        yield
    finally:
        os.chdir(current_dir)


class BackupTool:
    def __init__(self, source_dir, backup_dir):
        self.source_dir = os.path.abspath(source_dir)
        self.backup_dir = os.path.abspath(backup_dir)
        self.log_file = os.path.join(self.backup_dir, "backup.log")

        # Create backup directory if it doesn't exist
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup_name(self):
        """Create a unique name for the backup file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}.zip"

    def verify_backup(self, backup_path):
        """Verify the integrity of the backup file."""
        try:
            with zipfile.ZipFile(backup_path, "r") as zip_file:
                # Test zip file integrity
                zip_test_result = zip_file.testzip()
                if zip_test_result is not None:
                    raise zipfile.BadZipFile(
                        f"Corrupted file found in zip: {zip_test_result}"
                    )
                return True
        except (zipfile.BadZipFile, Exception) as e:
            logging.error(f"Backup verification failed: {str(e)}")
            return False

    @contextmanager
    def create_backup_zip(self, backup_path):
        """Context manager for creating a zip backup file."""
        try:
            zip_file = zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED)
            yield zip_file
        finally:
            zip_file.close()

    def perform_backup(self):
        """Perform the backup operation."""
        backup_name = self.create_backup_name()
        backup_path = os.path.join(self.backup_dir, backup_name)

        with BackupLogger(self.log_file) as logger:
            try:
                logger.info(f"Starting backup from {self.source_dir}")

                # Create the backup zip file
                with self.create_backup_zip(backup_path) as zip_file:
                    with change_dir(self.source_dir):
                        for root, dirs, files in os.walk("."):
                            for file in files:
                                file_path = os.path.join(root, file)
                                if not file_path.startswith(
                                    "./.git"
                                ):  # Skip .git directory
                                    logger.info(f"Adding file: {file_path}")
                                    zip_file.write(file_path)

                # Verify backup
                if self.verify_backup(backup_path):
                    logger.info(f"Backup completed successfully: {backup_name}")
                    self.cleanup_old_backups()
                else:
                    logger.error("Backup verification failed")
                    os.remove(backup_path)

            except Exception as e:
                logger.error(f"Backup failed: {str(e)}")
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                raise

    def cleanup_old_backups(self, keep_last=5):
        """Clean up old backup files, keeping only the specified number of recent backups."""
        with BackupLogger(self.log_file) as logger:
            try:
                backups = [
                    f
                    for f in os.listdir(self.backup_dir)
                    if f.startswith("backup_") and f.endswith(".zip")
                ]
                backups.sort(reverse=True)

                for old_backup in backups[keep_last:]:
                    backup_path = os.path.join(self.backup_dir, old_backup)
                    os.remove(backup_path)
                    logger.info(f"Removed old backup: {old_backup}")

            except Exception as e:
                logger.error(f"Cleanup failed: {str(e)}")


def main():
    print("Automated File Backup Tool")
    print("=========================")

    while True:
        print("\n1. Perform Backup")
        print("2. View Backup Log")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            source_dir = input("Enter source directory path: ")
            backup_dir = input("Enter backup directory path: ")

            if not os.path.exists(source_dir):
                print("Source directory does not exist!")
                continue

            try:
                backup_tool = BackupTool(source_dir, backup_dir)
                backup_tool.perform_backup()
            except Exception as e:
                print(f"Backup failed: {str(e)}")

        elif choice == "2":
            backup_dir = input("Enter backup directory path: ")
            log_file = os.path.join(backup_dir, "backup.log")

            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    print("\nBackup Log:")
                    print("===========")
                    print(f.read())
            else:
                print("Log file not found!")

        elif choice == "3":
            print("Thank you for using the Automated File Backup Tool!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
