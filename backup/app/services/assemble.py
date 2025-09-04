from typing import Dict, List
from jinja2 import Template


DEFAULT_TEMPLATE = {
    "body_template": (
        "{{ title }}\n\n"
        "This Agreement is made effective {{ effective_date }} between {{ party_a_name }} and {{ party_b_name }}.\n\n"
        "{% for section in sections %}{{ section }}\n\n{% endfor %}"
    )
}


def render_clause(body: str, fields: Dict) -> str:
    return Template(body).render(**fields)


def assemble_draft(template: Dict, fields: Dict, clauses: List[Dict]) -> str:
    tpl = template.get("body_template") or DEFAULT_TEMPLATE["body_template"]
    rendered_sections = [render_clause(c.get("body", ""), fields) for c in clauses]
    title = fields.get("title", "Agreement")
    return Template(tpl).render(sections=rendered_sections, title=title, **fields)

