from flask import Blueprint, jsonify, request
from .services.interpret import interpret_text
from .services.search import search_clauses
from .services.assemble import assemble_draft
from .services.validate import validate_draft
from .services.simplify import simplify_text
from .services.export import export_docx_bytes, export_pdf_bytes


api_bp = Blueprint("api", __name__)


@api_bp.post("/interpret")
def api_interpret():
    payload = request.get_json(force=True) or {}
    text = payload.get("text", "")
    result = interpret_text(text)
    return jsonify(result)


@api_bp.post("/clauses/search")
def api_search_clauses():
    payload = request.get_json(force=True) or {}
    query = payload.get("query", "")
    doc_type = payload.get("doc_type")
    jurisdiction = payload.get("jurisdiction")
    top_k = int(payload.get("top_k", 20))
    results = search_clauses(query, doc_type, jurisdiction, top_k=top_k)
    return jsonify({"results": results})


@api_bp.post("/draft/assemble")
def api_assemble():
    payload = request.get_json(force=True) or {}
    template = payload.get("template", {})
    fields = payload.get("fields", {})
    clauses = payload.get("clauses", [])
    draft_text = assemble_draft(template, fields, clauses)
    return jsonify({"draft": draft_text})


@api_bp.post("/draft/validate")
def api_validate():
    payload = request.get_json(force=True) or {}
    doc_type = payload.get("doc_type")
    jurisdiction = payload.get("jurisdiction")
    draft_text = payload.get("draft", "")
    issues = validate_draft(doc_type, jurisdiction, draft_text)
    return jsonify({"issues": issues})


@api_bp.post("/draft/simplify")
def api_simplify():
    payload = request.get_json(force=True) or {}
    draft_text = payload.get("draft", "")
    simplified = simplify_text(draft_text)
    return jsonify({"simplified": simplified})


@api_bp.post("/export/docx")
def api_export_docx():
    payload = request.get_json(force=True) or {}
    draft_text = payload.get("draft", "")
    filename = payload.get("filename", "document.docx")
    data = export_docx_bytes(draft_text)
    return (data, 200, {
        "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "Content-Disposition": f"attachment; filename={filename}"
    })


@api_bp.post("/export/pdf")
def api_export_pdf():
    payload = request.get_json(force=True) or {}
    draft_text = payload.get("draft", "")
    filename = payload.get("filename", "document.pdf")
    data = export_pdf_bytes(draft_text)
    return (data, 200, {
        "Content-Type": "application/pdf",
        "Content-Disposition": f"attachment; filename={filename}"
    })

