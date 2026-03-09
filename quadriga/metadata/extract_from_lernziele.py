"""Extract learning objectives with metadata from Lernziele.md files."""

from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import Any
from .utils import get_repo_root, save_yaml_file, get_file_path, load_yaml_file, iter_toc_files

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


DEFAULT_COMPETENCY = "nicht anwendbar"
DEFAULT_BLOOM = "nicht anwendbar"
DEFAULT_DATA_FLOW = "nicht anwendbar"


def normalize_whitespace(text: str) -> str:
    """Normalize repeated whitespace and newlines to single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def parse_metadata_comment(comment: str) -> dict[str, str]:
    """Parse 'competency: X | bloom: Y' from the inner text of an HTML comment."""
    metadata = {}

    for part in comment.split('|'):
        part = part.strip()
        if ':' not in part:
            continue
        key, value = part.split(':', 1)
        key = key.strip().lower().replace(' ', '-')
        value = value.strip()
        if not value:
            continue
        if key == 'bloom':
            metadata['blooms-category'] = value
        elif key == 'competency':
            metadata[key] = value
            metadata['data-flow'] = derive_data_flow(value)
    
    return metadata


def validate_objective_metadata(objective_data: dict[str, Any]) -> list[str]:
    """Fill in missing competency/bloom/data-flow defaults and return names of missing fields."""
    missing_fields = []
    
    if not objective_data.get('competency'):
        missing_fields.append('competency')
        objective_data['competency'] = DEFAULT_COMPETENCY
        objective_data['data-flow'] = DEFAULT_DATA_FLOW
    
    if not objective_data.get('blooms-category'):
        missing_fields.append('blooms-category')
        objective_data['blooms-category'] = DEFAULT_BLOOM
    
    return missing_fields


def derive_data_flow(competency: str) -> str:
    """Derive data-flow value from competency string."""
    competency_normalized = normalize_whitespace(competency)

    if competency_normalized == "Orientierungswissen":
        return "übergreifend"

    if competency_normalized.startswith("1."):
        return "1 Planung"

    if competency_normalized.startswith("2."):
        return "2 Erhebung und Aufbereitung"

    if competency_normalized.startswith("3."):
        return "3 Management"

    if competency_normalized.startswith("4."):
        return "4 Analyse"

    if competency_normalized.startswith("5."):
        return "5 Publikation und Nachnutzung"

    return DEFAULT_DATA_FLOW


def extract_admonition_blocks(
    content: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Extract learning-objective blocks and validation issues from Markdown content."""
    blocks = []
    validation_issues = []
    
    # Pattern to match admonition blocks with their content
    admonition_pattern = r'```\{admonition\}\s+(.+?)\n((?::[^\n]+\n)*)((?:(?!```).)+)```'
    
    matches = re.finditer(admonition_pattern, content, re.DOTALL | re.MULTILINE)
    
    for match in matches:
        title_line = match.group(1).strip()
        body = match.group(3).strip()
        
        # Parse title - extract text and reference
        title_match = re.match(r'\[(.+?)\]\((.+?)\)(\s*\(\*(.+?)\*\))?', title_line)
        
        if not title_match:
            logger.warning("Could not parse admonition title: %s", title_line)
            continue
        
        section_title = title_match.group(1)

        # Learning goal
        learning_goal_match = re.search(
            r'<!--\s*learning-goal:\s*(.+?)\s*-->',
            body,
            re.DOTALL,
        )
        if learning_goal_match:
            learning_goal = normalize_whitespace(learning_goal_match.group(1))
        else:
            learning_goal = "TODO"
            validation_issues.append({
                'section': section_title,
                'missing_fields': ['learning-goal']
            })

        # Chapter — use the first <!-- START: ChapterName --> tag in the admonition body.
        chapter = None
        start_match = re.search(r'<!--\s*START:\s*(.+?)\s*-->', body)
        if start_match:
            chapter = start_match.group(1).strip()

        # Strip all START/END markers before parsing objectives
        body_cleaned = re.sub(r'<!--\s*START:\s*.+?\s*-->\s*', '', body)
        body_cleaned = re.sub(r'\s*<!--\s*END:\s*.+?\s*-->', '', body_cleaned)

        # Parse numbered objectives with optional inline metadata comment
        objectives = []
        objective_pattern = r'\d+\.\s+(.+?)(?:\n\s*<!--\s*(.+?)\s*-->)?(?=\n\d+\.|\n\n|$)'

        for obj_match in re.finditer(objective_pattern, body_cleaned, re.DOTALL):
            objective_text = normalize_whitespace(obj_match.group(1))
            metadata_comment = obj_match.group(2)

            objective_data = {'learning-objective': objective_text}
            if metadata_comment:
                objective_data.update(parse_metadata_comment(metadata_comment))

            missing_fields = validate_objective_metadata(objective_data)
            if missing_fields:
                validation_issues.append({
                    'section': section_title,
                    'objective': objective_text,
                    'missing_fields': missing_fields
                })

            objectives.append(objective_data)
        
        if not objectives:
            continue

        block_data: dict[str, Any] = {
            'learning-goal': learning_goal,
            'objectives': objectives,
        }

        if chapter:
            block_data['chapter'] = chapter
        else:
            logger.warning(
                "No chapter specified for section '%s'. "
                "Add '<!-- START: ChapterName -->' after the line :class: lernziele, dropdown.",
                section_title,
            )
            validation_issues.append({
                'section': section_title,
                'missing_fields': ['chapter'],
            })

        blocks.append(block_data)

    return blocks, validation_issues


def extract_from_lernziele_file(
    md_file_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Read a Lernziele.md file and return (blocks, validation_issues)."""
    try:
        content = md_file_path.read_text(encoding="utf-8")
        blocks, issues = extract_admonition_blocks(content)
        logger.info("Extracted %d admonition blocks from %s", len(blocks), md_file_path.name)
        return blocks, issues
    except FileNotFoundError:
        logger.error("File not found: %s", md_file_path)
        return [], []
    except Exception:
        logger.exception("Error reading file: %s", md_file_path)
        return [], []


def generate_validation_report(
    validation_issues: list[dict[str, Any]],
    output_path: Path,
) -> None:
    """Write a human-readable validation report to output_path."""
    if not validation_issues:
        report = "✅ All learning objectives have complete metadata!\n"
    else:
        report = f"⚠️ Found {len(validation_issues)} issues with missing metadata:\n\n"
        for i, issue in enumerate(validation_issues, 1):
            report += f"{i}. Section: {issue['section']}\n"
            if 'objective' in issue:
                report += f"   Objective: {issue['objective'][:60]}...\n"
            report += f"   Missing: {', '.join(issue['missing_fields'])}\n\n"
        report += "\nHow to fix:\n"
        report += "  competency/bloom   → <!-- competency: X | bloom: Y --> after the objective\n"
        report += "  learning-goal      → <!-- learning-goal: ... --> inside the admonition block\n"
        report += "  chapter            → <!-- START: ChapterName --> before the learning goal\n"

    output_path.write_text(report, encoding="utf-8")
    logger.info("Validation report saved to %s", output_path)


def merge_learning_objectives_into_metadata() -> bool:
    """Extract learning objectives from Lernziele.md and merge into metadata.yml."""
    try:
        repo_root = get_repo_root()

        toc_data = load_yaml_file(get_file_path("_toc.yml", repo_root))

        md_file = None
        for file_str in iter_toc_files(toc_data or {}):
            p = Path(file_str)
            if re.search(r'lernziel|learning.?objective', p.stem, re.IGNORECASE):
                if p.suffix not in [".md", ".ipynb"]:
                    p = p.with_suffix(".md")
                full_path = get_file_path(p, repo_root)
                if full_path.exists():
                    md_file = full_path
                    break

        if md_file is None:
            logger.warning("No Lernziele file found in _toc.yml")
            return True

        sections, validation_issues = extract_from_lernziele_file(md_file)

        # Handle validation report
        report_path = repo_root / "learning-objectives-validation.txt"
        if validation_issues:
            generate_validation_report(validation_issues, report_path)
            logger.warning(
                "⚠️ Found %d objectives with missing metadata. "
                "See learning-objectives-validation.txt for details.",
                len(validation_issues),
            )
        else:
            logger.info("✅ All learning objectives have complete metadata")
            if report_path.exists():
                report_path.unlink()
                logger.info("Removed old validation report (no issues found)")

        if not sections:
            logger.warning("No learning objectives extracted")
            return True

        metadata_path = get_file_path("metadata.yml", repo_root)
        metadata = load_yaml_file(metadata_path)

        if not metadata or not isinstance(metadata, dict):
            logger.error("Could not load metadata.yml")
            return False

        chapter_objectives: dict[str, list] = {}
        chapter_learning_goals: dict[str, str] = {}
        for section in sections:
            chapter = section.get('chapter')
            if not chapter:
                continue
            chapter_objectives.setdefault(chapter, []).extend(section['objectives'])
            learning_goal = section.get('learning-goal')
            if learning_goal:
                if chapter in chapter_learning_goals and chapter_learning_goals[chapter] != learning_goal:
                    logger.warning(
                        "Multiple learning goals found for chapter '%s'. Using first one.",
                        chapter,
                    )
                else:
                    chapter_learning_goals[chapter] = learning_goal

        for chapter in metadata.get("chapters", []):
            if not isinstance(chapter, dict):
                continue
            chapter_title = chapter.get("title", "")
            if chapter_title not in chapter_objectives:
                logger.warning(
                    "No section found for chapter '%s' in lernziele.md. Skipping.",
                    chapter_title,
                )
                continue
            chapter["learning-goal"] = chapter_learning_goals.get(chapter_title, "TODO")
            chapter["learning-objectives"] = chapter_objectives[chapter_title]

        if save_yaml_file(metadata_path, metadata):
            logger.info("Successfully merged learning objectives into metadata.yml")
            return True

        logger.error("Failed to save updated metadata.yml")
        return False

    except Exception:
        logger.exception("Error merging learning objectives")
        return False


if __name__ == "__main__":
    success = merge_learning_objectives_into_metadata()
    exit(0 if success else 1)