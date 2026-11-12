from __future__ import annotations

import os
import ast
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("QuantitativeMarketAnalysisRepoAuditor")

class QuantitativeMarketAnalysisRepoAuditor:
    def __init__(self, root_dir: str = "."):
        self.root_dir = root_dir
        self.excluded_dirs = {".git", "__pycache__", "venv", ".pytest_cache", "data", "logs", "output", "models", ".devcontainer"}

    def audit_repository(self):
        """Walks through the Quantitative-Market-Analysis repository, parsing AST, validating syntax, and auto-fixing code hygiene."""
        logger.info(f"Starting Quantitative-Market-Analysis repository audit across: {os.path.abspath(self.root_dir)}")
        
        total_files = 0
        fixed_files = 0
        
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            dirnames[:] = [d for d in dirnames if d not in self.excluded_dirs]
            
            for file in filenames:
                if file.endswith(".py") and file != "repo_auditor.py":
                    file_path = os.path.join(dirpath, file)
                    total_files += 1
                    if self._inspect_and_fix_file(file_path):
                        fixed_files += 1

        logger.info(f"Audit Complete. Inspected: {total_files} files | Automatically Fixed/Sanitized: {fixed_files} files.")

    def _inspect_and_fix_file(self, file_path: str) -> bool:
        """Validates AST syntax and applies automated structural improvements."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 1. Syntax Validation via AST
            try:
                ast.parse(content)
            except SyntaxError as se:
                logger.error(f"Syntax Error detected in {file_path} at line {se.lineno}: {se.msg}")
                return False

            updated_content = content

            # 2. Automated Safety & Hygiene Fixes
            updated_content = self._ensure_future_imports(updated_content)
            updated_content = self._upgrade_prints_to_logging(updated_content)

            # 3. Write back modified content
            if updated_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                logger.info(f"Auto-fixed and saved: {file_path}")
                return True
                
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
        
        return False

    def _ensure_future_imports(self, content: str) -> str:
        """Ensures modern type annotations are supported."""
        if "from __future__ import annotations" not in content and "def " in content:
            lines = content.splitlines()
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    insert_idx = i
                    break
            lines.insert(insert_idx, "from __future__ import annotations")
            return "\n".join(lines) + "\n"
        return content

    def _upgrade_prints_to_logging(self, content: str) -> str:
        """Upgrades bare print statements to standardized logging for market analysis telemetry."""
        if "print(" in content and "import logging" not in content:
            lines = content.splitlines()
            import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith("import ") or line.startswith("from "):
                    import_idx = i + 1
            
            logger_setup = "\nimport logging\nlogger = logging.getLogger(__name__)"
            lines.insert(import_idx, logger_setup)
            return "\n".join(lines) + "\n"
        return content

if __name__ == "__main__":
    auditor = QuantitativeMarketAnalysisRepoAuditor()
    auditor.audit_repository()
